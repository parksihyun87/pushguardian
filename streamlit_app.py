"""Streamlit frontend for PushGuardian (alternative to FastAPI HTML)."""

import streamlit as st
from pushguardian.graph import run_guardian_stream

st.set_page_config(page_title="PushGuardian", page_icon="🛡️", layout="wide")

st.title("🛡️ PushGuardian - Git Diff Analyzer")
st.markdown(
    """
Analyze your git diffs for security issues and best-practice violations.
Upload a diff file or paste the diff text below.
"""
)

# Input method selection
input_method = st.radio("Input Method", ["Paste Diff Text", "Upload Diff File"])

diff_text = None

if input_method == "Paste Diff Text":
    diff_text = st.text_area(
        "Git Diff",
        height=300,
        placeholder="Paste your git diff output here...",
        help="Use: git diff HEAD~1 HEAD",
    )
elif input_method == "Upload Diff File":
    uploaded_file = st.file_uploader("Choose a diff file", type=["txt", "diff", "patch"])
    if uploaded_file:
        diff_text = uploaded_file.read().decode("utf-8")
        st.text_area("Preview", diff_text[:500] + "...", height=150)

# Node name mapping for user-friendly display
NODE_NAMES = {
    "load_config": "⚙️ Loading configuration",
    "scope_classify": "🔍 Classifying file types and stacks",
    "hard_policy_check": "🚨 Checking hard security rules",
    "soft_llm_judge": "🤖 Running LLM security analysis",
    "research_tavily": "🔎 Searching security resources (Tavily)",
    "research_serper": "🔎 Deep search with Serper",
    "observation_validate": "🧠 LLM evaluating research quality",
    "write_report": "📝 Generating report",
    "persist_report": "💾 Saving report",
}

# Analyze button
if st.button("🔍 Analyze Diff", type="primary"):
    if not diff_text or not diff_text.strip():
        st.error("Please provide a diff to analyze.")
    else:
        # Create placeholder for progress
        progress_placeholder = st.empty()
        status_container = st.container()

        try:
            state = None

            # Stream execution with progress updates
            for node_name, current_state in run_guardian_stream(diff_text, mode="web"):
                state = current_state

                # Display current node
                friendly_name = NODE_NAMES.get(node_name, f"Processing {node_name}")
                progress_placeholder.info(f"🔄 **{friendly_name}**")

            # Clear progress indicator
            progress_placeholder.empty()

            if state is None:
                st.error("Workflow did not produce a final state")
            else:

                # Display results
                col1, col2, col3 = st.columns(3)

                with col1:
                    decision_color = "🔴" if state["decision"] == "block" else "🟢"
                    st.metric("Decision", f"{decision_color} {state['decision'].upper()}")

                with col2:
                    st.metric("Severity", state["severity"].upper())

                with col3:
                    st.metric("Risk Score", f"{state['risk_score']:.2f}/1.00")

                # Findings
                all_findings = state["hard_findings"] + state["soft_findings"]

                if all_findings:
                    st.subheader("🔍 Findings")
                    for i, finding in enumerate(all_findings, 1):
                        severity_emoji = {
                            "low": "🟡",
                            "medium": "🟠",
                            "high": "🔴",
                            "critical": "🚨",
                        }.get(finding.severity, "⚪")

                        with st.expander(
                            f"{severity_emoji} [{finding.severity.upper()}] {finding.title}"
                        ):
                            st.markdown(f"**Type:** `{finding.kind}`")
                            st.markdown(f"**Confidence:** {finding.confidence:.0%}")
                            st.markdown(f"**Detail:**\n{finding.detail}")
                            st.markdown(f"**Fix Now:**\n```\n{finding.fix_now}\n```")
                else:
                    st.success("✅ No critical findings detected!")

                # Weak Stack Learning Section (separate from findings)
                if state.get("weak_stack_touched") and state.get("learning_points"):
                    st.divider()
                    st.subheader("📖 Learning: Weak Stack Detected")
                    st.warning(
                        f"⚠️ This change touches **{', '.join(state['weak_stack_touched'])}** "
                        f"which you marked as a weak stack. Here are fundamental concepts from your code:"
                    )

                    for lp in state["learning_points"]:
                        # Learning points always use 🟡 to distinguish from security findings
                        with st.expander(f"🟡 {lp.get('concept', 'Unknown Concept')}", expanded=True):
                            st.markdown(f"**Stack:** `{lp.get('stack', 'general')}`")
                            st.markdown(f"**What it means:** {lp.get('detail', 'No details available')}")

                # Full report
                st.divider()
                st.subheader("📄 Full Report")
                st.markdown(state["report_md"])

                # Developer debug info
                with st.expander("🔧 Developer Debug Info"):
                    st.markdown("### 📊 Research Summary")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Research Iterations", state["evidence"].research_iterations)
                    with col2:
                        st.metric("Principle Links", len(state["evidence"].principle_links))
                    with col3:
                        st.metric("Example Links", len(state["evidence"].example_links))

                    st.markdown("### 🔍 Search Queries Used")
                    if state["evidence"].search_queries:
                        for i, query in enumerate(state["evidence"].search_queries, 1):
                            st.code(f"{i}. {query}", language="text")
                    else:
                        st.info("No search queries recorded")

                    st.markdown("### 🛠️ Tools Used")
                    if state["evidence"].tools_used:
                        st.write(", ".join(state["evidence"].tools_used))
                    else:
                        st.info("No tools recorded")

                    st.markdown("### 🤖 LLM Observations (Agent Behavior)")
                    if state["evidence"].llm_observations:
                        for i, obs in enumerate(state["evidence"].llm_observations, 1):
                            st.markdown(f"**Observation #{i}** (Iteration {obs.get('iteration', '?')})")
                            st.json(obs)
                    else:
                        st.info("No LLM observations recorded")

                    st.markdown("### 📝 Internal Notes")
                    if state["evidence"].notes:
                        st.text_area("Research notes", state["evidence"].notes, height=150, disabled=True, key="internal_notes")
                    else:
                        st.info("No internal notes")

                # Download button
                st.download_button(
                    label="📥 Download Report (Markdown)",
                    data=state["report_md"],
                    file_name="pushguardian_report.md",
                    mime="text/markdown",
                )

        except Exception as e:
            progress_placeholder.empty()
            st.error(f"Analysis failed: {str(e)}")
            import traceback

            st.code(traceback.format_exc())

# Footer
st.markdown("---")
st.markdown("*Built with [LangGraph](https://langchain-ai.github.io/langgraph/) & Streamlit*")
