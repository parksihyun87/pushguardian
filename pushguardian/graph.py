"""LangGraph workflow definition."""

from typing import TypedDict, List, Annotated, Literal
from langgraph.graph import StateGraph, END
from .config import load_config
from .git_ops import parse_changed_files
from .detectors.secrets import detect_secrets
from .detectors.files import detect_sensitive_files
from .detectors.stack_guess import guess_stacks, identify_weak_stacks
from .llm.judge import run_soft_judge
from .llm.observe import validate_observation
from .llm.research_planner import plan_next_research
from .research.gather import gather_research, merge_evidence
from .report.models import Finding, Evidence
from .report.writer import generate_report_md, save_report


# State definition
class GuardianState(TypedDict):
    """State for PushGuardian workflow."""

    # Configuration
    config: dict
    repo_root: str | None

    # Input
    diff_text: str
    mode: Literal["cli", "web"]  # cli = pre-push hook, web = web demo

    # Parsed data
    changed_files: List[str]
    detected_stacks: List[str]
    weak_stack_touched: List[str]

    # Findings
    hard_findings: List[Finding]
    soft_findings: List[Finding]

    # Risk assessment
    risk_score: float
    severity: Literal["low", "medium", "high", "critical"]

    # Decision
    decision: Literal["allow", "block", "override"]
    override_reason: str | None

    # Research
    evidence: Evidence
    recheck_count: int

    # History
    history_hint: dict | None

    # Quick fixes
    quick_fixes: List[str]

    # Learning points (for weak stacks)
    learning_points: List[dict]

    # Output
    report_md: str
    report_path: str | None

    # Errors
    errors: List[str]

    #last query trace
    last_query: str | None

    #llm 플래너 출력
    research_plan: dict | None

    # LangSmith trace URL (if tracing enabled)
    langsmith_url: str | None

# Node functions
def load_config_node(state: GuardianState) -> GuardianState:
    """Load configuration."""
    # Initialize defaults FIRST (before accessing state)
    state.setdefault("changed_files", [])
    state.setdefault("detected_stacks", [])
    state.setdefault("weak_stack_touched", [])
    state.setdefault("hard_findings", [])
    state.setdefault("soft_findings", [])
    state.setdefault("risk_score", 0.0)
    state.setdefault("severity", "low")
    state.setdefault("decision", "allow")
    state.setdefault("override_reason", None)
    state.setdefault("evidence", Evidence())
    state.setdefault("recheck_count", 0)
    state.setdefault("last_query", None)
    state.setdefault("research_plan", None)
    state.setdefault("history_hint", None)
    state.setdefault("quick_fixes", [])
    state.setdefault("learning_points", [])
    state.setdefault("report_md", "")
    state.setdefault("report_path", None)
    state.setdefault("errors", [])
    state.setdefault("langsmith_url", None)

    # Now try to load config
    try:
        config = load_config()
        state["config"] = config
    except Exception as e:
        state["errors"].append(f"Config load failed: {e}")
        state["config"] = {}

    return state


def scope_classify_node(state: GuardianState) -> GuardianState:
    """Parse changed files and classify stack."""
    diff_text = state["diff_text"]

    # Parse changed files
    changed_files = parse_changed_files(diff_text)
    state["changed_files"] = changed_files

    # Guess stacks
    detected_stacks = guess_stacks(changed_files)
    state["detected_stacks"] = list(detected_stacks)

    # Identify weak stacks
    config = state["config"]
    stacks_known = config.get("stacks_known", [])
    stacks_weak = config.get("stacks_weak", [])

    weak_touched = identify_weak_stacks(detected_stacks, stacks_known, stacks_weak)
    state["weak_stack_touched"] = weak_touched

    return state


def hard_policy_check_node(state: GuardianState) -> GuardianState:
    """Check hard abort rules (secrets, sensitive files)."""
    diff_text = state["diff_text"]
    changed_files = state["changed_files"]
    config = state["config"]

    hard_abort = config.get("hard_abort", {})
    secret_patterns = hard_abort.get("secret_patterns", [])
    file_patterns = hard_abort.get("file_patterns", [])

    # Detect secrets
    secret_findings = detect_secrets(diff_text, secret_patterns)

    # Detect sensitive files
    file_findings = detect_sensitive_files(changed_files, file_patterns)

    # Merge findings
    hard_findings = secret_findings + file_findings
    state["hard_findings"] = hard_findings

    # If any hard findings, set decision to block
    if hard_findings:
        state["decision"] = "block"
        state["severity"] = "critical"
        state["risk_score"] = 1.0

    return state


def soft_llm_judge_node(state: GuardianState) -> GuardianState:
    """Run LLM-based soft checks."""
    # Skip if already blocked by hard rules
    if state["decision"] == "block":
        return state

    diff_text = state["diff_text"]
    config = state["config"]

    soft_checks = config.get("soft_checks", [])
    stacks_known = config.get("stacks_known", [])
    stacks_weak = config.get("stacks_weak", [])

    # Run judge
    result = run_soft_judge(diff_text, soft_checks, stacks_known, stacks_weak)

    state["soft_findings"] = result.get("findings", [])
    state["risk_score"] = result.get("risk_score", 0.0)
    state["severity"] = result.get("severity", "low")
    state["quick_fixes"] = result.get("quick_fixes", [])
    state["learning_points"] = result.get("learning_points", [])

    # Set decision based on severity
    if state["severity"] in ["high", "critical"]:
        state["decision"] = "block"
    elif state["severity"] == "medium":
        state["decision"] = "allow"  # Medium is warning, not block
    else:
        state["decision"] = "allow"

    return state


def research_tavily_node(state: GuardianState) -> GuardianState:
    """Gather research using Tavily (initial search)."""
    all_findings = state["hard_findings"] + state["soft_findings"]
    weak_stack_touched = state["weak_stack_touched"]
    learning_points = state.get("learning_points", [])

    # Gather research
    new_evidence = gather_research(
        all_findings,
        weak_stack_touched,
        search_engine="tavily",
        learning_points=learning_points
    )

    # Merge with existing evidence
    state["evidence"] = merge_evidence(state["evidence"], new_evidence)

    # Store query for LLM planner
    if all_findings:
        state["last_query"] = f"{all_findings[0].kind} security best practices"

    return state


def research_tavily_deep_node(state: GuardianState) -> GuardianState:
    """Deep Tavily search with LLM-refined query (not used anymore, kept for compatibility)."""
    plan = state.get("research_plan", {})
    refined_query = plan.get("refined_query", "")

    all_findings = state["hard_findings"] + state["soft_findings"]
    weak_stack_touched = state["weak_stack_touched"]

    # Increment recheck count
    state["recheck_count"] += 1

    # Use refined query if LLM provided one
    new_evidence = gather_research(
        all_findings,
        weak_stack_touched,
        search_engine="tavily",
        refined_query=refined_query
    )

    state["evidence"] = merge_evidence(state["evidence"], new_evidence)
    state["last_query"] = refined_query or state.get("last_query")

    return state


def research_serper_node(state: GuardianState) -> GuardianState:
    """Gather research using Serper (2nd attempt with refined query)."""
    plan = state.get("research_plan", {})
    refined_query = plan.get("refined_query", "")

    all_findings = state["hard_findings"] + state["soft_findings"]
    weak_stack_touched = state["weak_stack_touched"]
    learning_points = state.get("learning_points", [])

    # Increment recheck count
    state["recheck_count"] += 1

    # Gather research with refined query
    new_evidence = gather_research(
        all_findings,
        weak_stack_touched,
        search_engine="serper",
        refined_query=refined_query,
        learning_points=learning_points
    )

    # Merge with existing evidence
    state["evidence"] = merge_evidence(state["evidence"], new_evidence)
    state["last_query"] = refined_query or state.get("last_query")

    return state


def research_duckduckgo_node(state: GuardianState) -> GuardianState:
    """Gather research using DuckDuckGo (3rd attempt with refined query)."""
    plan = state.get("research_plan", {})
    refined_query = plan.get("refined_query", "")

    all_findings = state["hard_findings"] + state["soft_findings"]
    weak_stack_touched = state["weak_stack_touched"]

    # Increment recheck count
    state["recheck_count"] += 1

    # Gather research with refined query
    new_evidence = gather_research(
        all_findings,
        weak_stack_touched,
        search_engine="duckduckgo",
        refined_query=refined_query
    )

    # Merge with existing evidence
    state["evidence"] = merge_evidence(state["evidence"], new_evidence)
    state["last_query"] = refined_query or state.get("last_query")

    return state


def observation_validate_node(state: GuardianState) -> GuardianState:
    """Validate if evidence is sufficient using LLM planner."""
    all_findings = state["hard_findings"] + state["soft_findings"]
    evidence = state["evidence"]
    recheck_count = state["recheck_count"]
    last_query = state.get("last_query")

    # Step 1: LLM이 evidence 품질 평가 (observation)
    observation = validate_observation(all_findings, evidence, recheck_count)

    # Step 2: LLM이 다음 액션 계획 (planning)
    plan = plan_next_research(
        all_findings,
        evidence,
        recheck_count,
        last_query
    )

    state["research_plan"] = plan
    # Format notes with bullet points and line breaks for better readability
    state["evidence"].notes += f"\n\n* Observation: {observation.get('notes', 'N/A')}\n\n* Plan: {plan['reasoning']}"
    return state

def write_report_node(state: GuardianState) -> GuardianState:
    """Generate markdown report."""
    all_findings = state["hard_findings"] + state["soft_findings"]

    report_md = generate_report_md(
        findings=all_findings,
        evidence=state["evidence"],
        severity=state["severity"],
        risk_score=state["risk_score"],
        decision=state["decision"],
        override_reason=state["override_reason"],
        history_hint=state["history_hint"],
        weak_stack_touched=state["weak_stack_touched"],
        quick_fixes=state["quick_fixes"],
        learning_points=state.get("learning_points", []),
    )

    state["report_md"] = report_md

    return state


def persist_report_node(state: GuardianState) -> GuardianState:
    """Save report to disk (only in CLI mode)."""
    if state["mode"] == "web":
        return state  # Web mode doesn't persist to disk

    config = state["config"]
    report_dir = config.get("report_dir", ".")

    report_md = state["report_md"]

    # Save report
    try:
        report_path = save_report(report_md, report_dir)
        state["report_path"] = report_path
    except Exception as e:
        state["errors"].append(f"Failed to save report: {e}")

    return state


# Routing functions
def should_do_research(state: GuardianState) -> Literal["research", "write_report"]:
    """Decide if research is needed."""
    all_findings = state["hard_findings"] + state["soft_findings"]

    # If no findings and no weak stacks, skip research
    if not all_findings and not state["weak_stack_touched"]:
        return "write_report"

    # If severity is low and no weak stacks, skip research
    if state["severity"] == "low" and not state["weak_stack_touched"]:
        return "write_report"

    return "research"


def should_recheck(state: GuardianState) -> Literal["serper", "write_report"]:
    """LLM 플래너가 결정한 다음 액션으로 라우팅."""
    plan = state.get("research_plan", {})
    next_action = plan.get("next_action", "done")
    current_recheck = state["recheck_count"]

    # Force stop after max iterations (safety limit)
    # recheck_count: 0 (tavily), 1 (serper), max is 1
    if current_recheck >= 1:
        return "write_report"

    # LLM이 선택한 액션에 따라 라우팅
    if next_action == "search_serper" and current_recheck == 0:
        return "serper"
    else:  # "done" or unknown
        return "write_report"

# Build the graph
def build_graph() -> StateGraph:
    """Build the LangGraph workflow."""
    workflow = StateGraph(GuardianState)

    # Add nodes
    workflow.add_node("load_config", load_config_node)
    workflow.add_node("scope_classify", scope_classify_node)
    workflow.add_node("hard_policy_check", hard_policy_check_node)
    workflow.add_node("soft_llm_judge", soft_llm_judge_node)
    workflow.add_node("research_tavily", research_tavily_node)
    workflow.add_node("research_serper", research_serper_node)
    workflow.add_node("observation_validate", observation_validate_node)
    workflow.add_node("write_report", write_report_node)
    workflow.add_node("persist_report", persist_report_node)

    # Define edges
    workflow.set_entry_point("load_config")
    workflow.add_edge("load_config", "scope_classify")
    workflow.add_edge("scope_classify", "hard_policy_check")
    workflow.add_edge("hard_policy_check", "soft_llm_judge")

    # Conditional: research or skip
    workflow.add_conditional_edges(
        "soft_llm_judge", should_do_research, {"research": "research_tavily", "write_report": "write_report"}
    )

    workflow.add_edge("research_tavily", "observation_validate")

    # Conditional: LLM decides next action
    workflow.add_conditional_edges(
        "observation_validate",
        should_recheck,
        {
            "serper": "research_serper",
            "write_report": "write_report"
        },
    )

    # After additional research, validate again (but only once more)
    workflow.add_edge("research_serper", "observation_validate")

    workflow.add_edge("write_report", "persist_report")
    workflow.add_edge("persist_report", END)

    return workflow.compile()


# Main execution function
def run_guardian(diff_text: str, mode: Literal["cli", "web"] = "cli", repo_root: str | None = None) -> GuardianState:
    """
    Run the PushGuardian workflow.

    Args:
        diff_text: Git diff content
        mode: Execution mode (cli or web)
        repo_root: Git repository root (for CLI mode)

    Returns:
        Final state
    """
    graph = build_graph()

    initial_state = {
        "diff_text": diff_text,
        "mode": mode,
        "repo_root": repo_root,
    }

    final_state = graph.invoke(initial_state)

    return final_state


def run_guardian_stream(diff_text: str, mode: Literal["cli", "web"] = "cli", repo_root: str | None = None):
    """
    Run the PushGuardian workflow with streaming support.

    Yields:
        Tuple of (node_name, state) for each node execution

    Usage:
        for node_name, state in run_guardian_stream(diff):
            print(f"Running: {node_name}")
    """
    import os
    from langsmith import traceable

    graph = build_graph()

    initial_state = {
        "diff_text": diff_text,
        "mode": mode,
        "repo_root": repo_root,
    }

    # Set LangSmith project URL if tracing is enabled
    langsmith_enabled = os.getenv("LANGCHAIN_TRACING_V2") == "true"
    if langsmith_enabled:
        # Link to all projects page (since we don't have project UUID)
        langsmith_url = "https://smith.langchain.com/projects"
    else:
        langsmith_url = None

    for chunk in graph.stream(initial_state):
        # chunk is a dict like {"node_name": state}
        for node_name, state in chunk.items():
            # Add LangSmith URL to state
            if langsmith_url:
                state["langsmith_url"] = langsmith_url

            yield node_name, state
