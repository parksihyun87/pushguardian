"""CLI entry point for pre-push hook."""

import sys
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from .git_ops import get_diff_range, get_repo_root
from .graph import run_guardian

console = Console()


def human_decision_prompt(state: dict) -> str:
    """
    Prompt user for approval decision.

    Args:
        state: Guardian state with findings and report

    Returns:
        'allow', 'block', or 'override'
    """
    # Display report in terminal
    report_md = state["report_md"]
    decision = state["decision"]

    console.print("\n")
    console.print(Panel.fit("🛡️  PushGuardian 분석 완료", style="bold magenta"))
    console.print("\n")

    # Show markdown report
    if state["config"].get("ui", {}).get("show_markdown_in_terminal", True):
        md = Markdown(report_md)
        console.print(md)
    else:
        console.print(f"결정: {decision}")
        console.print(f"심각도: {state['severity']}")
        console.print(f"위험 점수: {state['risk_score']:.2f}")

    console.print("\n")

    # If blocked, do NOT ask for override in hook context
    # (stdin is piped, input() will fail with EOF)
    if decision == "block":
        console.print("[bold red]⛔ 심각한 이슈로 인해 푸시가 차단되었습니다.[/bold red]")
        console.print("\n[yellow]강제 진행 방법(권장하지 않음):[/yellow] 'git push --no-verify' 를 사용할 수 있습니다.")
        return "block", None

    else:
        console.print("[bold green]✅ 푸시가 허용되었습니다.[/bold green]")
        return "allow", None


def main():
    """Main CLI entry point for pre-push hook."""
    # Parse arguments from git pre-push hook
    # Format: pre-push <remote-name> <remote-url>
    # Stdin: <local-ref> <local-sha> <remote-ref> <remote-sha>

    if len(sys.argv) < 3:
        console.print("[red]에러: 잘못된 인자입니다. 이 스크립트는 git pre-push 훅에서 호출되도록 설계되었습니다.[/red]")
        sys.exit(1)

    remote_name = sys.argv[1]
    remote_url = sys.argv[2]

    # Read refs from stdin
    refs_line = sys.stdin.readline().strip()

    if not refs_line:
        console.print("[yellow]푸시할 커밋이 없습니다.[/yellow]")
        sys.exit(0)

    parts = refs_line.split()
    if len(parts) < 4:
        console.print("[red]에러: git으로부터 전달된 ref 형식이 올바르지 않습니다.[/red]")
        sys.exit(1)

    local_ref = parts[0]
    local_sha = parts[1]
    remote_ref = parts[2]
    remote_sha = parts[3]

    # remote_sha will be used by get_diff_range
    # (it handles the "0000..." case for new branches)

    try:
        repo_root = get_repo_root()
    except RuntimeError as e:
        console.print(f"[red]에러: {e}[/red]")
        sys.exit(1)

    console.print(f"[cyan]{remote_name} 으로의 푸시를 분석 중입니다...[/cyan]")

    try:
        # Get diff
        diff_text = get_diff_range(local_sha, remote_sha, repo_root)

        if not diff_text.strip():
            console.print("[yellow]변경 사항이 감지되지 않았습니다. 푸시를 허용합니다.[/yellow]")
            sys.exit(0)

        # Run guardian
        state = run_guardian(diff_text, mode="cli", repo_root=repo_root)

        # Human decision
        final_decision, override_reason = human_decision_prompt(state)

        if override_reason:
            state["override_reason"] = override_reason
            state["decision"] = "override"

            # Re-generate report with override reason
            from .report.writer import generate_report_md, save_report

            report_md = generate_report_md(
                findings=state["hard_findings"] + state["soft_findings"],
                evidence=state["evidence"],
                severity=state["severity"],
                risk_score=state["risk_score"],
                decision="override",
                override_reason=override_reason,
                history_hint=state["history_hint"],
                weak_stack_touched=state["weak_stack_touched"],
                quick_fixes=state["quick_fixes"],
            )

            # Save override report
            override_dir = state["config"].get("override_dir", ".")
            save_report(report_md, override_dir, prefix="override")

        # Show report path
        if state.get("report_path"):
            console.print(f"\n[green]📄 리포트 저장 경로:[/green] {state['report_path']}")

        # Exit based on decision
        if final_decision in ["allow", "override"]:
            console.print("\n[bold green]✅ 푸시가 허용되었습니다. 계속 진행합니다...[/bold green]\n")
            sys.exit(0)
        else:
            console.print("\n[bold red]⛔ 푸시가 차단되었습니다. 이슈를 수정한 뒤 다시 시도해 주세요.[/bold red]\n")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]분석 중 에러가 발생했습니다: {e}[/red]")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
