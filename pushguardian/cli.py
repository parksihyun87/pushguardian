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
    console.print(Panel.fit("🛡️  PushGuardian Analysis Complete", style="bold magenta"))
    console.print("\n")

    # Show markdown report
    if state["config"].get("ui", {}).get("show_markdown_in_terminal", True):
        md = Markdown(report_md)
        console.print(md)
    else:
        console.print(f"Decision: {decision}")
        console.print(f"Severity: {state['severity']}")
        console.print(f"Risk Score: {state['risk_score']:.2f}")

    console.print("\n")

    # If blocked, do NOT ask for override in hook context
    # (stdin is piped, input() will fail with EOF)
    if decision == "block":
        console.print("[bold red]⛔ Push is BLOCKED due to critical issues.[/bold red]")
        console.print("\n[yellow]To override:[/yellow] Use 'git push --no-verify' (NOT recommended)")
        return "block", None

    else:
        console.print("[bold green]✅ Push is ALLOWED.[/bold green]")
        return "allow", None


def main():
    """Main CLI entry point for pre-push hook."""
    # Parse arguments from git pre-push hook
    # Format: pre-push <remote-name> <remote-url>
    # Stdin: <local-ref> <local-sha> <remote-ref> <remote-sha>

    if len(sys.argv) < 3:
        console.print("[red]Error: Invalid arguments. This script is meant to be called by git pre-push hook.[/red]")
        sys.exit(1)

    remote_name = sys.argv[1]
    remote_url = sys.argv[2]

    # Read refs from stdin
    refs_line = sys.stdin.readline().strip()

    if not refs_line:
        console.print("[yellow]No commits to push.[/yellow]")
        sys.exit(0)

    parts = refs_line.split()
    if len(parts) < 4:
        console.print("[red]Error: Invalid ref format from git.[/red]")
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
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    console.print(f"[cyan]Analyzing push to {remote_name}...[/cyan]")

    try:
        # Get diff
        diff_text = get_diff_range(local_sha, remote_sha, repo_root)

        if not diff_text.strip():
            console.print("[yellow]No changes detected. Allowing push.[/yellow]")
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
            console.print(f"\n[green]📄 Report saved to:[/green] {state['report_path']}")

        # Exit based on decision
        if final_decision in ["allow", "override"]:
            console.print("\n[bold green]✅ Push allowed. Proceeding...[/bold green]\n")
            sys.exit(0)
        else:
            console.print("\n[bold red]⛔ Push blocked. Fix the issues and try again.[/bold red]\n")
            sys.exit(1)

    except Exception as e:
        console.print(f"[red]Error during analysis: {e}[/red]")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
