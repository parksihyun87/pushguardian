"""LangGraph workflow definition."""

from typing import TypedDict, List, Annotated, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .config import load_config
from .git_ops import parse_changed_files
from .detectors.secrets import detect_secrets
from .detectors.files import detect_sensitive_files
from .detectors.stack_guess import guess_stacks, identify_weak_stacks
from .llm.judge import run_soft_judge
from .llm.observe import validate_observation
from .llm.research_planner import plan_next_research
from .research.gather import gather_research, merge_evidence
from .research.link_annotator import annotate_link_titles_with_llm
from .research.naver_client import search_naver
from .research.naver_filter import filter_naver_results
from .research.naver_query_generator import generate_naver_query
from .report.models import Finding, Evidence, ConflictWarning
from .report.writer import generate_report_md, save_report
import time


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

    # HITL (Human-in-the-Loop) 관련
    human_approval_needed: bool  # 사람 승인 필요 여부
    human_decision: Literal["approve", "search_naver", "skip"] | None  # 사람의 결정

    # Conflict detection (BETA)
    base_diff: str | None  # origin/main의 diff
    conflict_files: List[str]  # 양쪽에서 수정된 파일 목록
    conflict_warnings: List[ConflictWarning]  # 충돌 경고

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
    state.setdefault("human_approval_needed", False)
    state.setdefault("human_decision", None)
    state.setdefault("base_diff", None)
    state.setdefault("conflict_files", [])
    state.setdefault("conflict_warnings", [])

    # Now try to load config
    try:
        config = load_config()

        # If initial_state already has config (e.g., from web UI override), merge it
        if "config" in state and state["config"]:
            # Merge: initial_state config overrides loaded config
            existing_config = state["config"]
            for key, value in existing_config.items():
                if isinstance(value, dict) and key in config and isinstance(config[key], dict):
                    # Merge nested dicts (e.g., conflict_detection)
                    config[key] = {**config[key], **value}
                else:
                    config[key] = value

        state["config"] = config
    except Exception as e:
        state["errors"].append(f"Config load failed: {e}")
        # Check if initial_state provided config
        if "config" not in state or not state["config"]:
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


def conflict_detect_node(state: GuardianState) -> GuardianState:
    """Detect potential merge conflicts (BETA)."""
    from .git_ops import fetch_base_branch, get_base_diff, detect_overlapping_files

    config = state["config"]
    conflict_config = config.get("conflict_detection", {})

    # Check if conflict detection is enabled
    if not conflict_config.get("enabled", False):
        # Skip conflict detection
        return state

    repo_root = state.get("repo_root")
    mode = state.get("mode", "web")

    # In web mode, we need base_diff provided via special format
    # In CLI mode, we can fetch it
    if mode == "web":
        # Web mode: check if diff_text has special format
        diff_text = state["diff_text"]
        if "=== MY DIFF ===" in diff_text and "=== BASE DIFF ===" in diff_text:
            # Parse dual diff format
            parts = diff_text.split("=== BASE DIFF ===")
            my_diff_part = parts[0].replace("=== MY DIFF ===", "").strip()
            base_diff_part = parts[1].strip() if len(parts) > 1 else ""

            state["diff_text"] = my_diff_part  # Update to only my diff
            state["base_diff"] = base_diff_part
        else:
            # No base diff provided, skip
            return state
    else:
        # CLI mode: fetch base diff
        if not repo_root:
            return state

        base_branch = conflict_config.get("base_branch", "origin/main")
        auto_fetch = conflict_config.get("auto_fetch", False)

        if auto_fetch:
            fetch_base_branch(repo_root, base_branch)

        base_diff = get_base_diff(repo_root, base_branch)
        state["base_diff"] = base_diff

    # Detect overlapping files
    my_diff = state["diff_text"]
    base_diff = state.get("base_diff", "")

    if not base_diff:
        return state

    conflict_files = detect_overlapping_files(my_diff, base_diff)
    state["conflict_files"] = conflict_files

    print(f"🔍 충돌 감지: {len(conflict_files)}개 파일이 양쪽에서 수정됨")

    return state


def conflict_analyze_node(state: GuardianState) -> GuardianState:
    """Analyze conflicts using LLM (BETA)."""
    from .git_ops import parse_diff_hunks, check_line_overlap
    from .llm.conflict_analyzer import analyze_conflict

    conflict_files = state.get("conflict_files", [])
    if not conflict_files:
        return state

    my_diff = state["diff_text"]
    base_diff = state.get("base_diff", "")

    # Parse hunks for both diffs
    my_hunks = parse_diff_hunks(my_diff)
    base_hunks = parse_diff_hunks(base_diff)

    # Analyze each conflict file
    warnings = []
    for filepath in conflict_files[:5]:  # Limit to 5 files to avoid too many LLM calls
        # Extract file-specific diffs
        my_file_diff = extract_file_diff(my_diff, filepath)
        base_file_diff = extract_file_diff(base_diff, filepath)

        # Check line overlap
        line_overlap = check_line_overlap(
            my_hunks.get(filepath, []),
            base_hunks.get(filepath, [])
        )

        # Analyze with LLM
        try:
            warning = analyze_conflict(filepath, my_file_diff, base_file_diff, line_overlap)
            warnings.append(warning)
            print(f"⚠️  {filepath}: {warning.conflict_probability*100:.0f}% 충돌 위험 ({warning.conflict_type})")
        except Exception as e:
            print(f"⚠️  {filepath}: 분석 실패 - {e}")

    state["conflict_warnings"] = warnings

    return state


def extract_file_diff(full_diff: str, filepath: str) -> str:
    """Extract diff for a specific file from full diff."""
    lines = full_diff.split("\n")
    result = []
    in_file = False

    for line in lines:
        if line.startswith("diff --git") and filepath in line:
            in_file = True
            result.append(line)
        elif line.startswith("diff --git") and in_file:
            # Next file started
            break
        elif in_file:
            result.append(line)

    return "\n".join(result)


def hard_policy_check_node(state: GuardianState) -> GuardianState:
    """Check hard abort rules (secrets, sensitive files)."""
    diff_text = state["diff_text"]
    changed_files = state["changed_files"]
    config = state["config"]
    repo_root = state.get("repo_root")

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

        # Scan history for when this issue first appeared (only in CLI mode)
        if repo_root and state.get("mode") == "cli":
            from .git_ops import scan_history_for_first_appearance
            import subprocess

            max_commits = config.get("history_scan_commits", 5)

            # Try to scan git history for when files were added
            file_findings_count = len([f for f in hard_findings if f.kind == "file"])

            if file_findings_count > 0:
                # For file findings, check when the file was added to git
                for finding in hard_findings:
                    if finding.kind == "file":
                        # Extract filename from detail "File: .env"
                        filename = finding.detail.replace("File: ", "").strip()

                        # Check git log for this file
                        cmd = ["git", "log", f"-{max_commits}", "--oneline", "--", filename]
                        result = subprocess.run(
                            cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
                        )

                        if result.returncode == 0 and result.stdout.strip():
                            commits = result.stdout.strip().split('\n')
                            first_commit = commits[-1].split()[0]  # Get oldest commit SHA

                            state["history_hint"] = {
                                "first_seen_commit": first_commit,
                                "message": f"⚠️ The file '{filename}' was added {len(commits)} commit(s) ago (scanned last {max_commits} commits).",
                                "scanned_commits": max_commits
                            }
                            break  # Only need one
                        else:
                            # File is being added in this commit
                            state["history_hint"] = {
                                "message": f"The file '{filename}' is being added in this commit (new addition).",
                                "scanned_commits": 0
                            }
                            break
            else:
                # For secret findings, try to extract the actual secret line
                added_lines = []
                for finding in hard_findings:
                    if finding.kind == "secret" and finding.detail:
                        # Extract line from detail
                        lines = [line.strip() for line in finding.detail.split('\n') if line.strip() and not line.startswith('Found')]
                        added_lines.extend(lines[:3])  # Top 3 lines per finding

                if added_lines:
                    first_commit = scan_history_for_first_appearance(repo_root, added_lines, max_commits)

                    if first_commit:
                        state["history_hint"] = {
                            "first_seen_commit": first_commit[:8],
                            "message": f"⚠️ This secret was first introduced approximately {max_commits} commits ago.",
                            "scanned_commits": max_commits
                        }
                    else:
                        state["history_hint"] = {
                            "message": f"This secret appears to be new (not found in the last {max_commits} commits).",
                            "scanned_commits": max_commits
                        }

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

    # LLM으로 링크 요약을 한국어 짧은 제목으로 보강 (최대 8개)
    try:
        annotate_link_titles_with_llm(state["evidence"], max_items=8)
    except Exception as e:
        state["errors"].append(f"Link annotation failed: {e}")

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

    # 2회 연구 완료 후 한글 자료 부족 시 HITL 트리거
    if recheck_count >= 1:  # tavily(0) + serper(1) = 2회 완료
        # LLM observation에서 한글 자료 부족 여부 확인
        korean_content_sufficient = observation.get("korean_content_sufficient", True)

        # LLM이 한글 자료가 부족하다고 판단하면 HITL 트리거
        if not korean_content_sufficient:
            state["human_approval_needed"] = True
            print(f"🔍 한글 자료 부족 감지: HITL 트리거 (총 링크: {len(evidence.principle_links) + len(evidence.example_links)}개)")

    return state


def human_approval_node(state: GuardianState) -> GuardianState:
    """사람의 승인을 기다리는 노드 (interrupt 발생)."""
    # 이 노드는 interrupt를 통해 사람의 입력을 기다림
    # Streamlit에서 graph.get_state()로 현재 상태를 확인하고
    # graph.update_state()로 human_decision을 설정한 후
    # graph.stream()을 다시 호출하여 진행

    # 여기서는 아무것도 하지 않고, 단지 interrupt 지점 역할만 함
    print("⏸️  사람의 승인 대기 중... (human_approval_node)")
    return state


def research_naver_node(state: GuardianState) -> GuardianState:
    """네이버 검색 API로 한글 자료 추가 수집."""
    all_findings = state["hard_findings"] + state["soft_findings"]
    weak_stack_touched = state["weak_stack_touched"]
    learning_points = state.get("learning_points", [])
    evidence = state["evidence"]

    # 보안 이슈와 약점 스택이 모두 있으면 두 번 검색
    search_tasks = []

    # 1. 보안 이슈 검색
    if all_findings:
        first_finding = all_findings[0]
        query_security = generate_naver_query(
            finding_title=first_finding.title,
            finding_detail=first_finding.detail,
            finding_kind=first_finding.kind
        )
        search_tasks.append({
            "query": query_security,
            "mode": "security",
            "finding_title": first_finding.title,
            "finding_detail": first_finding.detail,
            "type": "보안"
        })

    # 2. 약점 스택 튜토리얼 검색
    if weak_stack_touched and learning_points:
        query_tutorial = f"{weak_stack_touched[0]} 튜토리얼"
        concepts = ", ".join([lp.get("concept", "") for lp in learning_points[:3]])
        search_tasks.append({
            "query": query_tutorial,
            "mode": "tutorial",
            "finding_title": weak_stack_touched[0],
            "finding_detail": f"기본 개념: {concepts}",
            "type": "튜토리얼"
        })

    # 둘 다 없으면 기본 검색
    if not search_tasks:
        search_tasks.append({
            "query": "웹 보안 모범 사례",
            "mode": "security",
            "finding_title": "웹 보안",
            "finding_detail": "일반 보안 모범 사례",
            "type": "기본"
        })

    # 각 검색 작업 실행
    all_filtered_results = []
    for task in search_tasks:
        query = task["query"]
        mode = task["mode"]
        search_type = task["type"]

        print(f"🔍 네이버 검색 시작 ({search_type}): {query}")

        # 네이버 검색 실행
        start_time = time.time()
        results = search_naver(query, max_results=10)
        latency_ms = (time.time() - start_time) * 1000

        print(f"🔍 네이버 검색 완료 ({search_type}): {len(results)}개 결과")

        # LLM으로 결과 필터링
        if results:
            filtered_results = filter_naver_results(
                results=results,
                finding_title=task["finding_title"],
                finding_detail=task["finding_detail"],
                mode=mode
            )
            print(f"🤖 LLM 필터링 ({search_type}): {len(results)}개 → {len(filtered_results)}개 선별")

            # 검색 메타데이터에 모드 표시 추가
            for result in filtered_results:
                result["_search_mode"] = mode  # 나중에 구분하기 위해

            all_filtered_results.extend(filtered_results)
        else:
            print(f"⚠️ 검색 결과 없음 ({search_type})")

        # 메타데이터 업데이트
        evidence.tools_used.append("naver")
        evidence.search_queries.append(query)
        evidence.search_latencies.append(latency_ms)
        evidence.notes += f"\n\n* 네이버 검색 완료 ({search_type}): {len(results)}개 결과 수집 ({latency_ms:.0f}ms)"

    # 통합된 필터링 결과를 Evidence에 추가
    filtered_results = all_filtered_results

    for result in filtered_results:
        url = result.get("url", "")
        title = result.get("title", "")
        llm_reason = result.get("llm_reason", "")
        search_mode = result.get("_search_mode", "security")  # 어떤 모드로 검색했는지

        if url:
            # 원칙 링크와 예시 링크 구분
            if "github" in url.lower() or "stackoverflow" in url.lower():
                evidence.example_links.append(url)
            else:
                evidence.principle_links.append(url)

            # 메타데이터에 추가 (모드별로 구분)
            if "github" in url.lower() or "stackoverflow" in url.lower():
                evidence.example_link_infos.append({
                    "url": url,
                    "summary_ko": f"{title} - {llm_reason}" if llm_reason else title,
                    "role": "example",
                    "source": "naver_ko"
                })
            else:
                # 보안 모드면 principle_link_infos에 추가
                # 튜토리얼 모드면 example_link_infos에 추가 (학습 자료)
                if search_mode == "security":
                    evidence.principle_link_infos.append({
                        "url": url,
                        "summary_ko": f"{title} - {llm_reason}" if llm_reason else title,
                        "role": "principle",
                        "source": "naver_ko"
                    })
                else:  # tutorial mode
                    evidence.example_link_infos.append({
                        "url": url,
                        "summary_ko": f"{title} - {llm_reason}" if llm_reason else title,
                        "role": "example",
                        "source": "naver_ko"
                    })

    # 중복 제거
    evidence.principle_links = list(set(evidence.principle_links))
    evidence.example_links = list(set(evidence.example_links))

    print(f"✅ 네이버 검색 완료: 총 {len(all_filtered_results)}개 자료 선별")
    print(f"📊 최종 링크 수 - 원칙: {len(evidence.principle_links)}, 예시: {len(evidence.example_links)}")
    print(f"📊 메타데이터 링크 수 - 원칙: {len(evidence.principle_link_infos)}, 예시: {len(evidence.example_link_infos)}")

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


def should_recheck(state: GuardianState) -> Literal["serper", "human_approval", "write_report"]:
    """LLM 플래너가 결정한 다음 액션으로 라우팅."""
    plan = state.get("research_plan", {})
    next_action = plan.get("next_action", "done")
    current_recheck = state["recheck_count"]

    # Force stop after max iterations (safety limit)
    # recheck_count: 0 (tavily), 1 (serper), max is 1
    if current_recheck >= 1:
        # 2회 완료 후 HITL 체크
        if state.get("human_approval_needed"):
            return "human_approval"
        return "write_report"

    # LLM이 선택한 액션에 따라 라우팅
    if next_action == "search_serper" and current_recheck == 0:
        return "serper"
    else:  # "done" or unknown
        return "write_report"


def after_human_approval(state: GuardianState) -> Literal["naver", "write_report"]:
    """사람의 결정에 따라 라우팅."""
    decision = state.get("human_decision")

    if decision == "search_naver":
        return "naver"
    else:  # "approve" or "skip"
        return "write_report"


def should_analyze_conflicts(state: GuardianState) -> Literal["analyze", "skip"]:
    """충돌 파일이 있으면 분석, 없으면 skip."""
    conflict_files = state.get("conflict_files", [])
    if conflict_files:
        return "analyze"
    return "skip"


# Build the graph
def build_graph(checkpointer=None) -> StateGraph:
    """Build the LangGraph workflow with optional checkpointer for HITL."""
    workflow = StateGraph(GuardianState)

    # Add nodes
    workflow.add_node("load_config", load_config_node)
    workflow.add_node("scope_classify", scope_classify_node)
    workflow.add_node("conflict_detect", conflict_detect_node)  # NEW: Conflict detection
    workflow.add_node("conflict_analyze", conflict_analyze_node)  # NEW: Conflict analysis
    workflow.add_node("hard_policy_check", hard_policy_check_node)
    workflow.add_node("soft_llm_judge", soft_llm_judge_node)
    workflow.add_node("research_tavily", research_tavily_node)
    workflow.add_node("research_serper", research_serper_node)
    workflow.add_node("observation_validate", observation_validate_node)
    workflow.add_node("human_approval", human_approval_node)
    workflow.add_node("research_naver", research_naver_node)
    workflow.add_node("write_report", write_report_node)
    workflow.add_node("persist_report", persist_report_node)

    # Define edges
    workflow.set_entry_point("load_config")
    workflow.add_edge("load_config", "scope_classify")
    workflow.add_edge("scope_classify", "conflict_detect")  # Conflict detection first

    # Conditional: if conflicts found, analyze them; else skip to hard policy check
    workflow.add_conditional_edges(
        "conflict_detect",
        should_analyze_conflicts,
        {
            "analyze": "conflict_analyze",
            "skip": "hard_policy_check"
        }
    )

    workflow.add_edge("conflict_analyze", "hard_policy_check")  # After conflict analysis, continue to hard policy
    workflow.add_edge("hard_policy_check", "soft_llm_judge")

    # Conditional: research or skip
    workflow.add_conditional_edges(
        "soft_llm_judge", should_do_research, {"research": "research_tavily", "write_report": "write_report"}
    )

    workflow.add_edge("research_tavily", "observation_validate")

    # Conditional: LLM decides next action (including HITL)
    workflow.add_conditional_edges(
        "observation_validate",
        should_recheck,
        {
            "serper": "research_serper",
            "human_approval": "human_approval",
            "write_report": "write_report"
        },
    )

    # After additional research, validate again (but only once more)
    workflow.add_edge("research_serper", "observation_validate")

    # HITL: 사람의 결정에 따라 네이버 검색 또는 리포트 작성
    workflow.add_conditional_edges(
        "human_approval",
        after_human_approval,
        {
            "naver": "research_naver",
            "write_report": "write_report"
        }
    )

    # 네이버 검색 후 리포트 작성
    workflow.add_edge("research_naver", "write_report")

    workflow.add_edge("write_report", "persist_report")
    workflow.add_edge("persist_report", END)

    # Compile with checkpointer if provided (for HITL)
    if checkpointer:
        return workflow.compile(checkpointer=checkpointer, interrupt_before=["human_approval"])
    else:
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


def run_guardian_stream(diff_text: str, mode: Literal["cli", "web"] = "cli", repo_root: str | None = None,
                       enable_hitl: bool = False, thread_id: str = "default"):
    """
    Run the PushGuardian workflow with streaming support.

    Args:
        diff_text: Git diff content
        mode: Execution mode (cli or web)
        repo_root: Git repository root
        enable_hitl: Enable Human-in-the-Loop (requires checkpointer)
        thread_id: Thread ID for checkpointer (used to resume interrupted workflows)

    Yields:
        Tuple of (node_name, state) for each node execution

    Usage:
        for node_name, state in run_guardian_stream(diff):
            print(f"Running: {node_name}")
    """
    import os

    # Build graph with checkpointer if HITL is enabled
    if enable_hitl:
        checkpointer = MemorySaver()
        graph = build_graph(checkpointer=checkpointer)
        config = {"configurable": {"thread_id": thread_id}}
    else:
        graph = build_graph()
        config = None

    initial_state = {
        "diff_text": diff_text,
        "mode": mode,
        "repo_root": repo_root,
    }

    # Set LangSmith trace URL if tracing is enabled
    langsmith_enabled = os.getenv("LANGCHAIN_TRACING_V2") == "true"
    if langsmith_enabled:
        project_name = os.getenv("LANGCHAIN_PROJECT", "default")
        # Link to project page with filter for recent runs
        langsmith_url = f"https://smith.langchain.com/o/default/projects/p/{project_name}"
    else:
        langsmith_url = None

    if config:
        for chunk in graph.stream(initial_state, config=config):
            # chunk is a dict like {"node_name": state}
            for node_name, state in chunk.items():
                # Add LangSmith URL to state
                if langsmith_url:
                    state["langsmith_url"] = langsmith_url

                yield node_name, state
    else:
        for chunk in graph.stream(initial_state):
            # chunk is a dict like {"node_name": state}
            for node_name, state in chunk.items():
                # Add LangSmith URL to state
                if langsmith_url:
                    state["langsmith_url"] = langsmith_url

                yield node_name, state
