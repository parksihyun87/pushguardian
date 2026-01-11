"""Install pre-push git hook."""

import sys
import os
from pathlib import Path
from rich.console import Console

console = Console()


HOOK_TEMPLATE = '''#!/usr/bin/env bash
# PushGuardian pre-push hook
# Auto-generated - do not edit manually

# Python executable path (captured during installation)
PYTHON_EXE="{python_exe}"

# Run PushGuardian CLI
"$PYTHON_EXE" -m pushguardian.cli "$@"
exit $?
'''


def install_hook():
    """Install pre-push hook in current git repository."""
    try:
        # Find .git directory
        git_dir = Path.cwd()
        while git_dir != git_dir.parent:
            if (git_dir / ".git").exists():
                break
            git_dir = git_dir.parent
        else:
            console.print("[red]에러: git 저장소 안에서 실행되지 않았습니다.[/red]")
            console.print("git 저장소 디렉터리 내부에서 이 명령을 실행해 주세요.")
            sys.exit(1)

        hooks_dir = git_dir / ".git" / "hooks"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        hook_path = hooks_dir / "pre-push"

        # Get current Python executable
        python_exe = sys.executable

        # Generate hook script
        hook_content = HOOK_TEMPLATE.format(python_exe=python_exe)

        # Write hook
        with open(hook_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(hook_content)

        # Make executable (Unix-like systems)
        if os.name != "nt":  # Not Windows
            os.chmod(hook_path, 0o755)

        console.print(f"[green]✅ pre-push 훅이 성공적으로 설치되었습니다![/green]")
        console.print(f"[cyan]훅 위치:[/cyan] {hook_path}")
        console.print(f"[cyan]Python 실행 파일:[/cyan] {python_exe}")
        console.print("\n[yellow]참고:[/yellow] 이 훅을 건너뛰려면 'git push --no-verify' 를 사용할 수 있습니다.")

    except Exception as e:
        console.print(f"[red]훅 설치 중 오류가 발생했습니다: {e}[/red]")
        sys.exit(1)


def main():
    """CLI entry point for install-hook command."""
    console.print("[bold magenta]🛡️  PushGuardian pre-push 훅 설치기[/bold magenta]\n")
    install_hook()


if __name__ == "__main__":
    main()
