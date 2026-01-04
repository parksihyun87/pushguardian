"""LLM-based research planner with ReAct pattern."""

import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..report.models import Finding, Evidence


PLANNER_SYSTEM_PROMPT = """You are a research planning agent using the ReAct pattern.

Your task is to observe current evidence and plan the next research action.

You should output a structured JSON response with:
- is_sufficient: boolean - whether current evidence is adequate
- missing_categories: list - what's missing (principle/example)
- next_action: "search_tavily" | "search_serper" | "refine_query" | "done"
- refined_query: string - improved search query (if needed)
- filter_domains: list - domains to exclude from results
- reasoning: string - explain your decision

Be strategic: prioritize high-quality sources (OWASP, GitHub, official docs) over generic blogs.
"""


def create_planner_prompt(
    findings: List[Finding],
    evidence: Evidence,
    recheck_count: int,
    previous_query: str | None = None,
) -> str:
    """Create research planning prompt."""
    findings_desc = "\n".join(
        [f"- [{f.severity}] {f.kind}: {f.title}" for f in findings]
    )

    return f"""Analyze the research progress and decide next action.

**Findings to research:**
{findings_desc}

**Current evidence collected:**
- Principle links ({len(evidence.principle_links)}): {evidence.principle_links[:3]}
- Example links ({len(evidence.example_links)}): {evidence.example_links[:3]}
- Notes: {evidence.notes}

**Research attempts so far:** {recheck_count}/2
**Previous query:** {previous_query or 'N/A'}

**Requirements:**
1. At least 1 high-quality principle link (OWASP, official docs, security guides)
2. At least 1 practical example link (GitHub, Stack Overflow, tutorials)
3. Links must be relevant to the findings (not spam like SK company or academic papers)

**Your decision in JSON:**
{{
    "is_sufficient": true/false,
    "missing_categories": ["principle", "example"],
    "next_action": "search_tavily|search_serper|refine_query|done",
    "refined_query": "improved search query here",
    "filter_domains": ["domain1.com", "domain2.com"],
    "reasoning": "explain your decision"
}}

Return ONLY the JSON object.
"""


def plan_next_research(
    findings: List[Finding],
    evidence: Evidence,
    recheck_count: int,
    previous_query: str | None = None,
) -> Dict[str, Any]:
    """
    Use LLM to plan next research action (ReAct pattern).

    Args:
        findings: Current findings
        evidence: Evidence gathered so far
        recheck_count: Number of research attempts
        previous_query: Last search query used

    Returns:
        Dictionary with:
        - is_sufficient: bool
        - missing_categories: list
        - next_action: str
        - refined_query: str
        - filter_domains: list
        - reasoning: str
    """
    # Quick bailout: max attempts reached (after 2nd retry)
    if recheck_count >= 2:
        return {
            "is_sufficient": True,  # Force stop
            "missing_categories": [],
            "next_action": "done",
            "refined_query": "",
            "filter_domains": [],
            "reasoning": "Max research attempts (2 retries) reached, stopping to prevent infinite loop",
        }

    # No findings = no research needed
    if not findings:
        return {
            "is_sufficient": True,
            "missing_categories": [],
            "next_action": "done",
            "refined_query": "",
            "filter_domains": [],
            "reasoning": "No findings to research",
        }

    # Use LLM to decide
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    prompt = create_planner_prompt(findings, evidence, recheck_count, previous_query)

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)

        # Validate and set defaults
        result.setdefault("is_sufficient", False)
        result.setdefault("missing_categories", [])
        result.setdefault("next_action", "done")
        result.setdefault("refined_query", "")
        result.setdefault("filter_domains", [])
        result.setdefault("reasoning", "LLM decision")

        return result

    except Exception as e:
        # Fallback to simple heuristic
        has_principle = len(evidence.principle_links) > 0
        has_example = len(evidence.example_links) > 0

        if has_principle and has_example:
            next_action = "done"
        elif recheck_count == 0:
            next_action = "search_serper"  # Try backup
        else:
            next_action = "done"

        return {
            "is_sufficient": has_principle and has_example,
            "missing_categories": (
                (["principle"] if not has_principle else [])
                + (["example"] if not has_example else [])
            ),
            "next_action": next_action,
            "refined_query": "",
            "filter_domains": [],
            "reasoning": f"Fallback heuristic (LLM failed: {e})",
        }