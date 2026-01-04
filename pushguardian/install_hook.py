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
            console.print("[red]Error: Not in a git repository.[/red]")
            console.print("Please run this command from inside a git repository.")
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

        console.print(f"[green]✅ Pre-push hook installed successfully![/green]")
        console.print(f"[cyan]Hook location:[/cyan] {hook_path}")
        console.print(f"[cyan]Python executable:[/cyan] {python_exe}")
        console.print("\n[yellow]Note:[/yellow] You can bypass this hook with: git push --no-verify")

    except Exception as e:
        console.print(f"[red]Error installing hook: {e}[/red]")
        sys.exit(1)


def main():
    """CLI entry point for install-hook command."""
    console.print("[bold magenta]🛡️  PushGuardian Hook Installer[/bold magenta]\n")
    install_hook()


if __name__ == "__main__":
    main()
