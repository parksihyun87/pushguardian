"""LLM-based soft check judge using structured output."""

import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..report.models import Finding


JUDGE_SYSTEM_PROMPT = """You are a code security and best-practice analyzer.

Your task is to analyze git diffs and identify potential issues based on soft check rules.
You should output a structured JSON response with:
- findings: List of issues found (each with kind, title, detail, confidence, severity, fix_now)
- risk_score: Overall risk score from 0.0 to 1.0
- severity: Overall severity (low/medium/high/critical)
- decision_suggestion: "allow" or "block"
- quick_fixes: List of immediate action items

Be thorough but avoid false positives. Focus on real security and architectural risks.

IMPORTANT LANGUAGE REQUIREMENT:
- All human-readable text fields in the JSON (title, detail, fix_now, quick_fixes, learning_points.detail, learning_points.concept)
  MUST be written in Korean (한국어) in a natural, professional tone.
"""


def create_judge_prompt(
    diff_text: str,
    soft_checks: List[Dict[str, str]],
    stacks_known: List[str],
    stacks_weak: List[str],
) -> str:
    """Create the judge prompt with context."""
    checks_desc = "\n".join([f"- {c['name']}: {c['description']}" for c in soft_checks])

    return f"""Analyze this git diff for potential issues.

Soft checks to evaluate:
{checks_desc}

User's stack profile:
- Known stacks: {', '.join(stacks_known)}
- Weak stacks: {', '.join(stacks_weak)}

**CRITICAL DUAL MISSION:**

1. **SECURITY FIRST (Top Priority):**
   - ALWAYS identify security vulnerabilities regardless of stack familiarity
   - Hardcoded credentials (passwords, API keys, tokens in code)
   - Security misconfigurations (running as root, open ports, insecure defaults)
   - Injection vulnerabilities (SQL, XSS, command injection)
   - Authentication/authorization issues
   - **Even in weak stacks, NEVER skip security findings!**

2. **LEARNING MODE (For Weak Stacks):**
   - If this diff touches weak stacks, ALSO extract FUNDAMENTAL concepts from the code
   - Examples by stack:
     * Docker: FROM, WORKDIR, COPY, CMD instructions, environment variables
     * React: useState, useEffect hooks, component props, JSX syntax
     * TypeScript: interface definitions, type annotations, optional properties (?)
   - Focus ONLY on basic concepts that ACTUALLY APPEAR in the diff code
   - Include learning_points even if there are security issues

**Remember:** Security issues take precedence. Learning mode supplements security analysis, doesn't replace it.

Git diff:
```
{diff_text[:3000]}
```

Provide your analysis in JSON format (remember: all human-facing text must be in Korean):
{{
    "findings": [
        {{
            "kind": "dto|dependency|permission|structure",
            "title": "Brief title",
            "detail": "Detailed explanation with file/line references",
            "confidence": 0.8,
            "severity": "medium",
            "fix_now": "1. Step one\\n2. Step two\\n3. Step three"
        }}
    ],
    "risk_score": 0.5,
    "severity": "medium",
    "decision_suggestion": "block",
    "quick_fixes": ["Action 1", "Action 2"],
    "learning_points": [
        {{
            "stack": "react",
            "concept": "useState hook",
            "detail": "Creates state variable 'user'. Returns [value, setter function] to manage component state.",
            "priority": "high"
        }},
        {{
            "stack": "react",
            "concept": "useEffect hook",
            "detail": "Runs side effects (like API calls) when component mounts or dependencies change.",
            "priority": "high"
        }},
        {{
            "stack": "typescript",
            "concept": "interface User",
            "detail": "Defines the shape of User object with required and optional properties (bio?).",
            "priority": "medium"
        }}
    ]
}}

**Note:**
- MANDATORY: Include learning_points array if ANY weak stacks are touched (even if empty findings)
- Extract 2-5 fundamental concepts that actually appear in the diff code
- Priority: "high" for core concepts, "medium" for secondary, "low" for optional
- Keep it simple - this is for beginners learning the basics
- Don't skip learning_points just because there are security issues

Return ONLY the JSON object, no other text.
"""


def run_soft_judge(
    diff_text: str,
    soft_checks: List[Dict[str, str]],
    stacks_known: List[str],
    stacks_weak: List[str],
) -> Dict[str, Any]:
    """
    Run LLM-based soft check analysis.

    Args:
        diff_text: Git diff content
        soft_checks: List of soft check definitions from config
        stacks_known: User's known stacks
        stacks_weak: User's weak stacks

    Returns:
        Dictionary with findings, risk_score, severity, etc.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    prompt = create_judge_prompt(diff_text, soft_checks, stacks_known, stacks_weak)

    messages = [
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Try to extract JSON from markdown code blocks if present
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)

        # Convert findings to Finding objects
        findings_list = []
        for f in result.get("findings", []):
            findings_list.append(
                Finding(
                    kind=f.get("kind", "structure"),
                    title=f["title"],
                    detail=f["detail"],
                    confidence=f.get("confidence", 0.7),
                    severity=f.get("severity", "medium"),
                    fix_now=f.get("fix_now", "Review and address the issue"),
                )
            )

        return {
            "findings": findings_list,
            "risk_score": result.get("risk_score", 0.5),
            "severity": result.get("severity", "medium"),
            "decision_suggestion": result.get("decision_suggestion", "allow"),
            "quick_fixes": result.get("quick_fixes", []),
            "learning_points": result.get("learning_points", []),
        }

    except Exception as e:
        # Fallback if LLM fails
        return {
            "findings": [],
            "risk_score": 0.0,
            "severity": "low",
            "decision_suggestion": "allow",
            "quick_fixes": [],
            "learning_points": [],
            "error": str(e),
        }
