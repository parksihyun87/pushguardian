"""Observation validator - checks if research evidence is sufficient."""

import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..report.models import Finding, Evidence


OBSERVE_SYSTEM_PROMPT = """You are a research quality validator focusing on QUALITY over QUANTITY.

Your task is to evaluate if the gathered evidence (principle and example links)
adequately support the identified security/best-practice findings.

QUALITY CRITERIA:
1. Principle links: Prefer OWASP, NIST, official docs over generic blogs/glossaries
2. Example links: Prefer GitHub repos, Stack Overflow, detailed tutorials over promotional content
3. Relevance: Links must directly address the specific finding, not just general topics
4. Practicality: Examples must show actual code/implementation, not just theory

IMPORTANT: 1-2 HIGH-QUALITY links are better than 5-10 low-quality links!

You should output a structured JSON response with:
- is_sufficient: boolean - whether evidence is adequate IN QUALITY (not just quantity)
- need_more: boolean - whether more HIGH-QUALITY research is needed
- missing_categories: list of category names still needed
- relevance_score: 0.0 to 1.0 (quality-weighted, not count-based)
- notes: Brief explanation focusing on quality assessment
"""


def create_observe_prompt(
    findings: List[Finding], evidence: Evidence, recheck_count: int
) -> str:
    """Create observation validation prompt."""
    findings_desc = "\n".join(
        [f"- [{f.severity}] {f.title}: {f.detail[:200]}" for f in findings]
    )

    return f"""Evaluate if the research evidence supports the findings (FOCUS ON QUALITY).

Findings:
{findings_desc}

Evidence gathered:
- Principle links ({len(evidence.principle_links)}): {evidence.principle_links}
- Example links ({len(evidence.example_links)}): {evidence.example_links}
- Notes: {evidence.notes}

Current research loop count: {recheck_count}/1

QUALITY REQUIREMENTS (not just count):
1. At least 1 HIGH-QUALITY principle link (OWASP, NIST, CWE, official security docs)
   - NOT glossary pages, NOT promotional content, NOT generic blogs
2. At least 1 HIGH-QUALITY example link (GitHub with actual code, detailed Stack Overflow, step-by-step tutorial)
   - NOT just links to homepage, NOT promotional articles
3. Links must DIRECTLY address the specific security issue, not just the general topic

EVALUATION STRATEGY:
- If you see Akamai/CDN glossaries, promotional pages, or generic content → "need_more": true
- If you see OWASP/NIST/CWE/GitHub code/detailed tutorials → "is_sufficient": true
- Prefer 1 excellent link over 10 mediocre links
- Max 1 retry allowed, so be realistic in evaluation

Provide your assessment in JSON format:
{{
    "is_sufficient": true/false,
    "need_more": true/false,
    "missing_categories": ["principle"/"example" if high-quality is missing],
    "relevance_score": 0.0-1.0,
    "notes": "Explain quality assessment (e.g., 'Has OWASP cheatsheet and GitHub example' or 'Only glossary pages, need authoritative sources')"
}}

Return ONLY the JSON object, no other text.
"""


def validate_observation(
    findings: List[Finding], evidence: Evidence, recheck_count: int
) -> Dict[str, Any]:
    """
    Validate if gathered evidence is sufficient.

    Args:
        findings: List of findings to validate against
        evidence: Evidence object with gathered links
        recheck_count: Current research iteration (0, 1, or 2)

    Returns:
        Dictionary with validation results
    """
    # Quick checks before LLM
    has_principle = len(evidence.principle_links) > 0
    has_example = len(evidence.example_links) > 0

    # If no findings, no validation needed
    if not findings:
        result = {
            "is_sufficient": True,
            "need_more": False,
            "missing_categories": [],
            "relevance_score": 1.0,
            "notes": "No findings to validate",
        }
        evidence.llm_observations.append(result)
        return result

    # If we've already tried once or more, force stop
    if recheck_count >= 1:
        result = {
            "is_sufficient": True,  # Force sufficient to stop loop
            "need_more": False,
            "missing_categories": [],
            "relevance_score": 0.5,
            "notes": "Max research attempts reached (1 retry done), proceeding with available evidence",
        }
        evidence.llm_observations.append(result)
        return result

    # Use LLM to validate
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    prompt = create_observe_prompt(findings, evidence, recheck_count)

    messages = [
        SystemMessage(content=OBSERVE_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Try to extract JSON
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)

        # Enforce max recheck limit - force stop after 1st retry
        if recheck_count >= 1:
            result["need_more"] = False
            result["is_sufficient"] = True

        # Store observation in evidence
        evidence.llm_observations.append({
            "iteration": recheck_count,
            "model": "gpt-4o-mini",
            **result
        })

        return result

    except Exception as e:
        # Fallback
        result = {
            "is_sufficient": has_principle and has_example or recheck_count >= 2,
            "need_more": (not has_principle or not has_example) and recheck_count < 2,
            "missing_categories": (
                (["principle"] if not has_principle else [])
                + (["example"] if not has_example else [])
            ),
            "relevance_score": 0.5,
            "notes": f"LLM validation failed: {e}",
        }
        evidence.llm_observations.append({
            "iteration": recheck_count,
            "model": "gpt-4o-mini (fallback)",
            **result
        })
        return result
