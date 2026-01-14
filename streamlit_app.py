"""Streamlit frontend for PushGuardian (alternative to FastAPI HTML)."""

import streamlit as st
from pathlib import Path
import subprocess
from pushguardian.graph import run_guardian_stream, build_graph
from pushguardian.repo_context import RepoContext
from langgraph.checkpoint.memory import MemorySaver

st.set_page_config(page_title="PushGuardian", page_icon="🛡️", layout="wide")

st.title("🛡️ PushGuardian - Git Diff 보안 분석기")
st.markdown(
    """
Git diff를 기반으로 **보안 이슈와 모범 사례 위반**을 자동으로 분석합니다.  
아래에 diff 텍스트를 붙여 넣거나 diff 파일을 업로드해 주세요.
"""
)

# Example files mapping
EXAMPLE_FILES = {
    "-- 예시를 선택하세요 --": None,
    "🚨 하드 블록 (치명적 보안 위험)": "examples/test_file/block.txt",
    "🟠 중간 위험 (LLM 소프트 판정)": "examples/test_file/soft_medium_xss.txt",
    "🟡 낮은 위험 (코드 스타일/성능)": "examples/test_file/soft_low_style.txt",
    "📖 약점 스택 (학습 모드)": "examples/test_file/weak_stack_docker.txt",
    "✅ 깨끗한 코드 (통과 예시)": "examples/test_file/pass.txt",
    "⚠️ (beta) 충돌 위험": "examples/test_file/conflict_risk.txt",
}

# Input method selection
input_method = st.radio(
    "입력 방식",
    [
        "Diff 텍스트 붙여넣기",
        "Git 레포 경로 지정 (로컬에서 커밋 분석)",
    ],
)

diff_text = None

# Example selector (only for "Diff 텍스트 붙여넣기" mode)
if input_method == "Diff 텍스트 붙여넣기":
    st.markdown("**빠른 테스트:** PushGuardian 동작을 보기 위해 예제 diff를 불러올 수 있습니다.")
    example_choice = st.selectbox(
        "예제 불러오기",
        options=list(EXAMPLE_FILES.keys()),
        help="예제를 선택하면 아래 텍스트 영역에 자동으로 로드됩니다.",
    )

    # Load example file if selected
    example_content = ""
    is_conflict_example = (example_choice == "⚠️ (beta) 충돌 위험")

    if example_choice != "-- 예시를 선택하세요 --":
        example_path = Path(EXAMPLE_FILES[example_choice])
        if example_path.exists():
            example_content = example_path.read_text(encoding="utf-8")
        else:
            st.warning(f"⚠️ 예제 파일을 찾을 수 없습니다: {example_path}")

    # Special UI for conflict example (dual diff input)
    if is_conflict_example and example_content:
        st.info("🧪 **beta 기능**: Merge Conflict 예측을 테스트합니다. 내 변경사항과 Main 브랜치 변경사항을 비교 분석합니다.")

        # Parse example file into two parts
        if "=== MY DIFF ===" in example_content and "=== BASE DIFF" in example_content:
            # Split by any BASE DIFF marker (with or without "(origin/main)")
            import re
            parts = re.split(r"=== BASE DIFF[^\n]*===", example_content)
            my_diff_example = parts[0].replace("=== MY DIFF ===", "").strip()
            base_diff_example = parts[1].strip() if len(parts) > 1 else ""
        else:
            my_diff_example = example_content
            base_diff_example = ""

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📝 내 변경사항 (My Diff)")
            my_diff = st.text_area(
                "My Diff",
                value=my_diff_example,
                height=300,
                label_visibility="collapsed"
            )
        with col2:
            st.markdown("### 🌐 Main 브랜치 변경사항")
            base_diff = st.text_area(
                "Base Diff",
                value=base_diff_example,
                height=300,
                label_visibility="collapsed"
            )

        # Combine into special format for backend
        diff_text = f"=== MY DIFF ===\n{my_diff}\n\n=== BASE DIFF ===\n{base_diff}"

        # Enable conflict detection for this analysis
        st.session_state["enable_conflict_detection"] = True
    else:
        # Normal single diff input
        diff_text = st.text_area(
            "Git Diff 내용",
            value=example_content,
            height=300,
            placeholder="여기에 git diff 출력 결과를 붙여 넣어 주세요...",
            help="예: git diff HEAD~1 HEAD",
        )
        st.session_state["enable_conflict_detection"] = False
elif input_method == "Git 레포 경로 지정 (로컬에서 커밋 분석)":
    st.info(
        "아직 원격(origin/main)으로 푸시되지 않은 커밋 범위 전체에 대한 diff를 자동으로 분석합니다. "
        "아래에 Git 레포지토리 루트 경로를 입력해 주세요."
    )

    repo_path = st.text_input(
        "Git 레포지토리 경로",
        value="",
        placeholder="예: C:/workspace/my-project 또는 . (현재 폴더)",
        help="절대 경로 또는 상대 경로를 입력하세요. '.'은 Streamlit을 실행한 폴더를 의미합니다."
    )

    base_ref = st.text_input("비교 기준 브랜치/태그 (기본: origin/main)", value="origin/main")

    if st.button("📌 미푸시 커밋 전체 diff 가져오기"):
        try:
            repo = RepoContext(repo_path)
            ahead = repo.ahead_count(base_ref=base_ref, head_ref="HEAD")
            if ahead <= 0:
                st.info("현재 브랜치는 기준 ref 보다 앞선 커밋이 없습니다. (미푸시 커밋 없음)")
                st.session_state["loaded_diff"] = None
            else:
                fetched_diff = repo.diff_last_n_commits(ahead, head_ref="HEAD")
                st.session_state["loaded_diff"] = fetched_diff
                preview = fetched_diff[:1500] + ("..." if len(fetched_diff) > 1500 else "")
                st.success(f"미푸시 커밋 {ahead}개에 대한 diff를 불러왔습니다.")
                st.text_area("Git Diff 미리보기", preview, height=300, disabled=True)
        except Exception as e:
            st.error(f"레포지토리 분석 중 오류가 발생했습니다: {e}")
            st.session_state["loaded_diff"] = None

    # Set diff_text from session state
    if "loaded_diff" in st.session_state and st.session_state["loaded_diff"]:
        diff_text = st.session_state["loaded_diff"]

# Node name mapping for user-friendly display
NODE_NAMES = {
    "load_config": "⚙️ 설정 로딩 중",
    "scope_classify": "🔍 파일 타입 및 스택 분류 중",
    "conflict_detect": "⚠️ 충돌 감지 중 (beta)",
    "conflict_analyze": "🔬 충돌 분석 중 (beta)",
    "hard_policy_check": "🚨 하드 보안 규칙 검사 중",
    "soft_llm_judge": "🤖 LLM 기반 보안 분석 중",
    "research_tavily": "🔎 Tavily로 보안 자료 검색 중",
    "research_serper": "🔎 Serper로 심화 검색 중",
    "observation_validate": "🧠 LLM이 리서치 품질 평가 중",
    "human_approval": "⏸️  사람의 승인 대기 중",
    "research_naver": "🔎 네이버로 한글 자료 검색 중",
    "write_report": "📝 리포트 생성 중",
    "persist_report": "💾 리포트 저장 중",
}

# Initialize session state for HITL
if "hitl_graph" not in st.session_state:
    st.session_state.hitl_graph = None
if "hitl_config" not in st.session_state:
    st.session_state.hitl_config = None
if "hitl_waiting" not in st.session_state:
    st.session_state.hitl_waiting = False
if "hitl_state" not in st.session_state:
    st.session_state.hitl_state = None
if "hitl_processing" not in st.session_state:
    st.session_state.hitl_processing = False
if "hitl_processing_type" not in st.session_state:
    st.session_state.hitl_processing_type = None

# HITL processing - 실제 그래프 실행
if st.session_state.hitl_processing:
    st.warning("⏸️  **한글 자료 추가 검색이 필요합니다 (HITL)**")
    st.markdown("---")

    processing_type = st.session_state.hitl_processing_type
    if processing_type == "search_naver":
        st.info("🔍 네이버 검색을 진행하고 있습니다...")
    else:
        st.info("⏭️ 현재 자료로 리포트를 작성하고 있습니다...")

    progress_placeholder = st.empty()

    graph = st.session_state.hitl_graph
    config = st.session_state.hitl_config

    try:
        # 그래프 재개
        final_state = None
        node_count = 0
        for chunk in graph.stream(None, config=config):
            for node_name, current_state in chunk.items():
                node_count += 1
                final_state = current_state
                friendly_name = NODE_NAMES.get(node_name, f"{node_name} 처리 중")
                progress_placeholder.info(f"⏳ {friendly_name} (노드 #{node_count})")

                # 디버깅: 네이버 검색 후 링크 수 확인
                if node_name == "research_naver" and "evidence" in current_state:
                    ev = current_state["evidence"]
                    print(f"[DEBUG] research_naver 완료 - 원칙: {len(ev.principle_links)}, 예시: {len(ev.example_links)}")
                elif node_name == "write_report" and "evidence" in current_state:
                    ev = current_state["evidence"]
                    print(f"[DEBUG] write_report 완료 - 원칙: {len(ev.principle_links)}, 예시: {len(ev.example_links)}")

        progress_placeholder.empty()

        if final_state:
            if processing_type == "search_naver":
                # 최종 상태의 evidence 확인
                if "evidence" in final_state:
                    ev = final_state["evidence"]
                    st.success(f"✅ 네이버 검색 완료! (총 {node_count}개 노드 실행)")
                    st.info(f"📊 업데이트된 링크: 원칙 {len(ev.principle_links)}개, 예시 {len(ev.example_links)}개")
                    print(f"[STREAMLIT] final_state 저장 전 - 원칙: {len(ev.principle_links)}, 예시: {len(ev.example_links)}")
                else:
                    st.success(f"✅ 네이버 검색 완료! (총 {node_count}개 노드 실행)")
            else:
                st.success("✅ 리포트 작성 완료!")

            # 상태 저장 전에 한번 더 확인
            print(f"[STREAMLIT] final_state를 session_state.final_result에 저장합니다")
            st.session_state.final_result = final_state
            st.session_state.hitl_processing = False
            st.session_state.hitl_processing_type = None
            st.rerun()

    except Exception as e:
        st.error(f"재개 중 오류 발생: {e}")
        import traceback
        st.code(traceback.format_exc())
        st.session_state.hitl_processing = False
        st.session_state.hitl_processing_type = None

# HITL 승인 대기 중인 경우 승인 화면 표시
elif st.session_state.hitl_waiting and st.session_state.hitl_state:
    st.warning("⏸️  **한글 자료 추가 검색이 필요합니다 (HITL)**")
    st.markdown("---")

    state = st.session_state.hitl_state
    evidence = state.get("evidence")

    st.info(f"""
    **현재 수집된 자료:**
    - 원칙 링크: {len(evidence.principle_links) if evidence else 0}개
    - 예시 링크: {len(evidence.example_links) if evidence else 0}개

    한글 자료가 부족할 수 있습니다. 네이버 검색 API로 한글 자료를 추가로 검색하시겠습니까?
    """)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔍 네이버 검색 추가", type="primary", use_container_width=True):
            # 사용자가 네이버 검색을 선택
            st.session_state.hitl_state["human_decision"] = "search_naver"
            st.session_state.hitl_waiting = False

            # 그래프 상태 업데이트
            graph = st.session_state.hitl_graph
            config = st.session_state.hitl_config
            graph.update_state(config, st.session_state.hitl_state)

            # Processing 플래그 설정하고 즉시 rerun
            st.session_state.hitl_processing = True
            st.session_state.hitl_processing_type = "search_naver"
            st.rerun()

    with col2:
        if st.button("⏭️ 건너뛰고 계속", use_container_width=True):
            # 현재 자료로 계속 진행
            st.session_state.hitl_state["human_decision"] = "skip"
            st.session_state.hitl_waiting = False

            # 그래프 상태 업데이트
            graph = st.session_state.hitl_graph
            config = st.session_state.hitl_config
            graph.update_state(config, st.session_state.hitl_state)

            # Processing 플래그 설정하고 즉시 rerun
            st.session_state.hitl_processing = True
            st.session_state.hitl_processing_type = "skip"
            st.rerun()

# Analyze button
elif st.button("🔍 Diff 분석하기", type="primary"):
    if not diff_text or not diff_text.strip():
        st.error("분석할 diff 내용을 입력하거나 업로드해 주세요.")
    else:
        # Reset HITL state
        st.session_state.hitl_waiting = False
        st.session_state.hitl_state = None
        if "final_result" in st.session_state:
            del st.session_state.final_result

        # Create placeholder for progress
        progress_placeholder = st.empty()
        status_container = st.container()

        try:
            state = None

            # Build graph with HITL support
            checkpointer = MemorySaver()
            thread_id = "web_session_1"
            config = {"configurable": {"thread_id": thread_id}}

            graph = build_graph(checkpointer=checkpointer)
            st.session_state.hitl_graph = graph
            st.session_state.hitl_config = config

            initial_state = {
                "diff_text": diff_text,
                "mode": "web",
                "repo_root": None,
            }

            # Enable conflict detection if flag is set
            if st.session_state.get("enable_conflict_detection", False):
                initial_state["config"] = {
                    "conflict_detection": {
                        "enabled": True,
                        "base_branch": "origin/main",
                        "auto_fetch": False
                    }
                }

            # Stream execution with progress updates
            interrupted = False
            for chunk in graph.stream(initial_state, config=config):
                for node_name, current_state in chunk.items():
                    state = current_state

                    # Display current node
                    friendly_name = NODE_NAMES.get(node_name, f"{node_name} 처리 중")
                    progress_placeholder.info(f"⏳ 분석 중... {friendly_name}")

                    # Check if we hit human_approval node
                    if node_name == "human_approval" or current_state.get("human_approval_needed"):
                        # 인터럽트 발생: HITL 필요
                        st.session_state.hitl_waiting = True
                        st.session_state.hitl_state = current_state
                        interrupted = True
                        break

                if interrupted:
                    break

            # Clear progress indicator
            progress_placeholder.empty()

            if interrupted:
                # HITL 대기 상태로 전환 - 페이지 새로고침
                st.rerun()
            elif state is None:
                st.error("Workflow did not produce a final state")
            else:
                # 정상 완료 - 결과 표시
                st.session_state.final_result = state
                st.rerun()

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"분석에 실패했습니다: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# 결과 표시 (final_result가 있을 때)
if "final_result" in st.session_state and st.session_state.final_result:
    state = st.session_state.final_result

    # LangSmith URL이 없으면 다시 생성 (HITL 재개 후에는 없을 수 있음)
    if "langsmith_url" not in state or not state["langsmith_url"]:
        import os
        langsmith_enabled = os.getenv("LANGCHAIN_TRACING_V2") == "true"
        if langsmith_enabled:
            project_name = os.getenv("LANGCHAIN_PROJECT", "default")
            state["langsmith_url"] = f"https://smith.langchain.com/o/default/projects/p/{project_name}"

    # 디버깅: 현재 표시되는 상태의 링크 개수 확인
    if "evidence" in state:
        ev = state["evidence"]
        print(f"[STREAMLIT DISPLAY] 화면에 표시 중 - 원칙: {len(ev.principle_links)}, 예시: {len(ev.example_links)}")

    # Display results
    col1, col2, col3 = st.columns(3)

    with col1:
        decision_color = "🔴" if state["decision"] == "block" else "🟢"
        decision_ko = {
            "allow": "허용",
            "block": "차단",
            "override": "오버라이드"
        }.get(state["decision"].lower(), state["decision"].upper())
        st.metric("결정", f"{decision_color} {decision_ko}")

    with col2:
        severity_ko = {
            "low": "낮음",
            "medium": "중간",
            "high": "높음",
            "critical": "심각"
        }.get(state["severity"].lower(), state["severity"].upper())
        st.metric("심각도", severity_ko)

    with col3:
        st.metric("위험 점수", f"{state['risk_score']:.2f}/1.00")

    # Findings
    all_findings = state["hard_findings"] + state["soft_findings"]

    if all_findings:
        st.subheader("🔍 발견된 이슈")
        for i, finding in enumerate(all_findings, 1):
            severity_emoji = {
                "low": "🟡",
                "medium": "🟠",
                "high": "🔴",
                "critical": "🚨",
            }.get(finding.severity, "⚪")

            finding_severity_ko = {
                "low": "낮음",
                "medium": "중간",
                "high": "높음",
                "critical": "심각"
            }.get(finding.severity.lower(), finding.severity.upper())

            with st.expander(
                f"{severity_emoji} [{finding_severity_ko}] {finding.title}"
            ):
                st.markdown(f"**유형:** `{finding.kind}`")
                st.markdown(f"**신뢰도:** {finding.confidence:.0%}")
                st.markdown(f"**상세 설명:**\n{finding.detail}")
                st.markdown(f"**즉시 수정 가이드:**\n```\n{finding.fix_now}\n```")
    else:
        st.success("✅ 치명적인 보안 이슈가 감지되지 않았습니다!")

    # Conflict Warnings Section (beta)
    conflict_warnings = state.get("conflict_warnings", [])
    if conflict_warnings:
        st.divider()
        st.subheader("⚠️ 병합 충돌 예측 (beta)")
        st.info(
            f"🔍 {len(conflict_warnings)}개 파일에서 병합 충돌 가능성이 감지되었습니다. "
            "내 변경사항과 base branch 변경사항이 겹칩니다."
        )

        for i, warning in enumerate(conflict_warnings, 1):
            # Conflict type emoji mapping
            conflict_emoji = {
                "routing": "🔀",
                "config": "⚙️",
                "refactoring": "🔧",
                "semantic_duplicate": "📋",
                "unknown": "❓"
            }.get(warning.conflict_type, "⚠️")

            # Conflict probability display
            prob = warning.conflict_probability
            prob_display = f"{prob:.0%}"
            prob_badge = "🔴" if prob >= 0.7 else "🟠" if prob >= 0.4 else "🟡"

            # Recommendation mapping
            recommendation_ko = {
                "keep_both": "양쪽 모두 유지",
                "choose_one": "하나 선택",
                "manual_merge": "수동 병합 필요"
            }.get(warning.recommendation, warning.recommendation)

            with st.expander(
                f"{conflict_emoji} {warning.file_path} - {prob_badge} {prob_display}",
                expanded=(i == 1)  # First one expanded
            ):
                st.markdown(f"**충돌 유형:** `{warning.conflict_type}`")
                st.markdown(f"**충돌 확률:** {prob_display}")
                st.markdown(f"**권장 조치:** {recommendation_ko}")
                st.markdown(f"**라인 겹침:** {'예' if warning.line_overlap else '아니오'}")
                st.markdown(f"\n**분석:**\n{warning.advice_ko}")

                # Merge suggestion
                st.markdown("---")
                st.markdown("### 💡 권장 병합 방법")
                st.markdown(warning.merge_suggestion_ko)

    # Weak Stack Learning Section (separate from findings)
    if state.get("weak_stack_touched") and state.get("learning_points"):
        st.divider()
        st.subheader("📖 학습: 약점 스택 감지됨")
        st.warning(
            f"⚠️ 이 변경사항은 사용자가 약점 스택으로 지정한 **{', '.join(state['weak_stack_touched'])}** "
            f"영역을 포함하고 있습니다. 아래는 해당 코드와 관련된 기본 개념들입니다:"
        )

        for lp in state["learning_points"]:
            # Learning points always use 🟡 to distinguish from security findings
            with st.expander(f"🟡 {lp.get('concept', '알 수 없는 개념')}", expanded=True):
                st.markdown(f"**스택:** `{lp.get('stack', 'general')}`")
                st.markdown(f"**의미:** {lp.get('detail', '상세 설명이 없습니다.')}")

    # Full report
    st.divider()
    st.subheader("📄 전체 리포트")
    st.markdown(state["report_md"])

    # Developer debug info
    with st.expander("🔧 개발자용 디버그 정보"):
        # LangSmith Trace Link (if available)
        if state.get("langsmith_url"):
            st.markdown("### 🔗 LangSmith 디버깅 (개인용)")
            st.info("⚠️ LangSmith에서 상세 LangGraph 실행 로그를 확인할 수 있습니다. 본인 LangSmith 계정으로 로그인되어 있어야 합니다.")
            st.markdown(f"🔍 [LangSmith 프로젝트 보기]({state['langsmith_url']})")
            st.caption("프로젝트 페이지에서 최근 실행 기록을 확인하세요. 가장 최신 trace가 방금 실행된 분석입니다.")
            st.divider()

        st.markdown("### 📊 리서치 요약")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("리서치 반복 횟수", state["evidence"].research_iterations)
        with col2:
            st.metric("원리 문서 링크 수", len(state["evidence"].principle_links))
        with col3:
            st.metric("예제 링크 수", len(state["evidence"].example_links))

        # 실제 링크 목록 표시
        st.markdown("### 🔗 수집된 링크")

        if state["evidence"].principle_links:
            st.markdown("**📚 원칙 링크 (Principle Links):**")
            for i, link in enumerate(state["evidence"].principle_links, 1):
                st.markdown(f"{i}. {link}")
        else:
            st.info("원칙 링크가 없습니다.")

        st.markdown("")  # 간격

        if state["evidence"].example_links:
            st.markdown("**💡 예시 링크 (Example Links):**")
            for i, link in enumerate(state["evidence"].example_links, 1):
                st.markdown(f"{i}. {link}")
        else:
            st.info("예시 링크가 없습니다.")

        st.markdown("### 🔍 사용된 검색 쿼리")
        if state["evidence"].search_queries:
            for i, query in enumerate(state["evidence"].search_queries, 1):
                st.code(f"{i}. {query}", language="text")
        else:
            st.info("기록된 검색 쿼리가 없습니다.")

        st.markdown("### 🛠️ 사용된 도구")
        if state["evidence"].tools_used:
            st.write(", ".join(state["evidence"].tools_used))
        else:
            st.info("기록된 도구가 없습니다.")

        st.markdown("### 🤖 LLM Observation (에이전트 동작 로그)")
        if state["evidence"].llm_observations:
            for i, obs in enumerate(state["evidence"].llm_observations, 1):
                st.markdown(f"**Observation #{i}** (Iteration {obs.get('iteration', '?')})")
                st.json(obs)
        else:
            st.info("기록된 LLM Observation이 없습니다.")

        st.markdown("### 📝 내부 노트 (에이전트 ReAct 사고 과정)")
        if state["evidence"].notes:
            st.text_area("리서치 노트", state["evidence"].notes, height=150, disabled=True, key="internal_notes")
        else:
            st.info("내부 노트가 없습니다.")

    # Download button
    st.download_button(
        label="📥 리포트 다운로드 (Markdown)",
        data=state["report_md"],
        file_name="pushguardian_report.md",
        mime="text/markdown",
    )

# Footer
st.markdown("---")
st.markdown("*[LangGraph](https://langchain-ai.github.io/langgraph/) & Streamlit으로 제작됨*")
