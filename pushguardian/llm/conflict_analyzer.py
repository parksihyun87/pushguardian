"""LLM-based merge conflict analyzer."""

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ..report.models import ConflictWarning


CONFLICT_ANALYZER_SYSTEM_PROMPT = """You are a git merge conflict expert. Analyze two changes and predict merge conflicts.

CRITICAL: Respond with ONLY valid JSON. No explanations before or after.

Conflict types:
- "routing": Both add routes/imports at same location → 0.8-0.9 probability (git will conflict)
- "config": Same setting changed to different values → 0.9-1.0 probability (definite conflict)
- "refactoring": Same logic changed differently → 0.9-1.0 probability (manual merge required)
- "semantic_duplicate": Same meaning, different code → 0.6-0.8 probability
- "unknown": Cannot classify → use line overlap to decide

Probability guidelines:
- Line overlap + same location edit = HIGH (0.7-1.0)
- Line overlap + different semantics = MEDIUM-HIGH (0.6-0.8)
- No line overlap = LOW (0.1-0.3)

Recommendations:
- "keep_both": Keep both (routing if no semantic conflict)
- "choose_one": Pick one (duplicates)
- "manual_merge": Manual merge (config/refactoring/high-risk conflicts)

merge_suggestion_ko format:
Use "권장 병합 결과:" header followed by code block showing the merged result.
Add inline comments to indicate which change is from where."""


def create_conflict_prompt(
    file_path: str,
    my_changes: str,
    their_changes: str,
    line_overlap: bool
) -> str:
    """Create conflict analysis prompt."""
    overlap_info = "Yes" if line_overlap else "No"

    return f"""File: {file_path}
Line overlap: {overlap_info}

MY CHANGES:
```diff
{my_changes[:800]}
```

THEIR CHANGES:
```diff
{their_changes[:800]}
```

Analyze and return JSON with these fields:
- conflict_probability (0.0-1.0): Use guidelines from system prompt
- conflict_type: "routing", "config", "refactoring", "semantic_duplicate", or "unknown"
- recommendation: "keep_both", "choose_one", or "manual_merge"
- advice_ko: Korean explanation of WHY this conflicts and HOW to resolve
- merge_suggestion_ko: Start with "권장 병합 결과:" then show merged code in markdown code block

Example for routing conflict:
{{"conflict_probability": 0.85, "conflict_type": "routing", "recommendation": "keep_both", "advice_ko": "양쪽 모두 같은 위치(Dashboard 다음)에 새로운 라우트를 추가하고 있어 Git 충돌이 발생합니다. 두 라우트 모두 유효하므로 수동으로 양쪽을 모두 포함시켜야 합니다.", "merge_suggestion_ko": "권장 병합 결과:\\n```typescript\\nconst routes = [\\n  {{{{ path: '/', component: Home }}}},\\n  {{{{ path: '/dashboard', component: Dashboard }}}},\\n  {{{{ path: '/profile', component: Profile }}}},  // 내 변경사항\\n  {{{{ path: '/settings', component: Settings }}}}  // Main 변경사항\\n];\\n```"}}

Example for config conflict:
{{"conflict_probability": 0.95, "conflict_type": "config", "recommendation": "manual_merge", "advice_ko": "양쪽이 같은 baseUrl 설정을 서로 다른 값으로 변경했습니다. 어느 URL이 올바른지 확인한 후 선택해야 합니다.", "merge_suggestion_ko": "권장 병합 결과:\\n```typescript\\n// 옵션 1: 내 변경 (api-v2.example.com)\\n// 옵션 2: Main 변경 (prod.example.com)\\n// 팀과 상의하여 올바른 URL을 선택하세요\\nexport const API_CONFIG = {{{{\\n  baseUrl: '선택 필요',  // 충돌: 어느 URL을 사용할지 결정\\n  timeout: 5000,\\n}}}};\\n```"}}"""


def analyze_conflict(
    file_path: str,
    my_changes: str,
    their_changes: str,
    line_overlap: bool
) -> ConflictWarning:
    """
    Analyze potential merge conflict using LLM.

    Args:
        file_path: File with potential conflict
        my_changes: My branch's diff for this file
        their_changes: Base branch's diff for this file
        line_overlap: Whether line ranges overlap

    Returns:
        ConflictWarning with analysis results
    """
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        model_kwargs={"response_format": {"type": "json_object"}}
    )

    prompt = create_conflict_prompt(file_path, my_changes, their_changes, line_overlap)

    messages = [
        SystemMessage(content=CONFLICT_ANALYZER_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Debug: print raw response
        print(f"[DEBUG] LLM Raw Response (first 500 chars):\n{content[:500]}\n")

        if not content:
            raise ValueError("LLM returned empty response")

        # Extract JSON - try multiple methods
        original_content = content

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # If content looks like it starts with explanation, try to find JSON object
        if not content.startswith("{"):
            # Try to find JSON object in the response
            import re
            json_match = re.search(r'\{[^{}]*"conflict_probability"[^{}]*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)
            else:
                print(f"[ERROR] Could not find JSON in response. Original:\n{original_content}")
                raise ValueError("No valid JSON found in response")

        print(f"[DEBUG] Extracted JSON:\n{content[:500]}\n")
        result = json.loads(content)

        return ConflictWarning(
            file_path=file_path,
            conflict_probability=result.get("conflict_probability", 0.5),
            conflict_type=result.get("conflict_type", "unknown"),
            recommendation=result.get("recommendation", "manual_merge"),
            advice_ko=result.get("advice_ko", "충돌 가능성이 있습니다. 수동으로 확인이 필요합니다."),
            merge_suggestion_ko=result.get("merge_suggestion_ko", "수동 병합이 필요합니다."),
            my_changes=my_changes[:500],  # Truncate for storage
            their_changes=their_changes[:500],
            line_overlap=line_overlap,
        )

    except Exception as e:
        # Fallback: simple heuristic
        if line_overlap:
            probability = 0.7
            advice = "같은 라인을 수정하여 충돌 가능성이 높습니다. 수동 병합이 필요할 수 있습니다."
        else:
            probability = 0.3
            advice = "다른 라인을 수정하여 자동 병합될 가능성이 높습니다."

        return ConflictWarning(
            file_path=file_path,
            conflict_probability=probability,
            conflict_type="unknown",
            recommendation="manual_merge" if line_overlap else "keep_both",
            advice_ko=f"{advice} (LLM 분석 실패: {str(e)})",
            merge_suggestion_ko="LLM 분석에 실패하여 병합 제안을 생성할 수 없습니다. 수동으로 확인해주세요.",
            my_changes=my_changes[:500],
            their_changes=their_changes[:500],
            line_overlap=line_overlap,
        )
