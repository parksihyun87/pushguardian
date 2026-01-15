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

advice_ko format:
Use a Markdown list with EXACTLY 5 bullets:
- "충돌 위치: <file_path> 라인 <my_line_ranges> (내 변경), <file_path> 라인 <base_line_ranges> (<base_branch> 변경)"
- "내 변경: ..."
- "<base_branch> 변경: ..."
- "충돌 원인: ..."
- "해결: ..."
Be concrete. Use exact line ranges from the prompt. Do NOT use generic words like "their"; always say the base branch name.

merge_suggestion_ko format:
Use "권장 병합 결과:" header followed by code block showing the merged result.
Add inline comments to indicate which change is from where."""


def _format_line_ranges(ranges: list[tuple[int, int]] | None) -> str:
    """Format line ranges for display."""
    if not ranges:
        return "unknown"
    parts = []
    for start, end in ranges:
        parts.append(f"{start}-{end}" if start != end else f"{start}")
    return ", ".join(parts)


def create_conflict_prompt(
    file_path: str,
    my_changes: str,
    their_changes: str,
    line_overlap: bool,
    my_line_ranges: list[tuple[int, int]] | None = None,
    base_line_ranges: list[tuple[int, int]] | None = None,
    base_branch: str | None = None,
) -> str:
    """Create conflict analysis prompt."""
    overlap_info = "Yes" if line_overlap else "No"

    base_branch_label = base_branch or "base"
    my_ranges = _format_line_ranges(my_line_ranges)
    base_ranges = _format_line_ranges(base_line_ranges)

    return f"""File: {file_path}
Base branch: {base_branch_label}
Line overlap: {overlap_info}
My line ranges: {my_ranges}
{base_branch_label} line ranges: {base_ranges}

MY CHANGES:
```diff
{my_changes[:800]}
```

BASE BRANCH CHANGES:
```diff
{their_changes[:800]}
```

Analyze and return JSON with these fields:
- conflict_probability (0.0-1.0): Use guidelines from system prompt
- conflict_type: "routing", "config", "refactoring", "semantic_duplicate", or "unknown"
- recommendation: "keep_both", "choose_one", or "manual_merge"
- advice_ko: Korean explanation of WHY this conflicts and HOW to resolve, with concrete "my vs their" details
- merge_suggestion_ko: Start with "권장 병합 결과:" then show merged code in markdown code block

Example for routing conflict:
{{"conflict_probability": 0.85, "conflict_type": "routing", "recommendation": "keep_both", "advice_ko": "- 충돌 위치: src/routes/app.tsx 라인 42-48 (내 변경), src/routes/app.tsx 라인 44-50 (origin/main 변경)\\n- 내 변경: 라우트 배열에 /profile 경로를 추가함\\n- origin/main 변경: 라우트 배열에 /settings 경로를 추가함\\n- 충돌 원인: 같은 구간의 라우트 배열을 동시에 수정해 Git이 자동 병합하지 못함\\n- 해결: 두 라우트를 모두 포함하도록 수동 병합", "merge_suggestion_ko": "권장 병합 결과:\\n```typescript\\nconst routes = [\\n  {{{{ path: '/', component: Home }}}},\\n  {{{{ path: '/dashboard', component: Dashboard }}}},\\n  {{{{ path: '/profile', component: Profile }}}},  // 내 변경사항\\n  {{{{ path: '/settings', component: Settings }}}}  // Main 변경사항\\n];\\n```"}}

Example for config conflict:
{{"conflict_probability": 0.95, "conflict_type": "config", "recommendation": "manual_merge", "advice_ko": "- 충돌 위치: src/config/api.ts 라인 10 (내 변경), src/config/api.ts 라인 10 (origin/main 변경)\\n- 내 변경: baseUrl을 api-v2.example.com으로 변경함\\n- origin/main 변경: baseUrl을 prod.example.com으로 변경함\\n- 충돌 원인: 같은 설정 키를 서로 다른 값으로 바꿔 충돌\\n- 해결: 팀과 상의해 올바른 baseUrl 선택", "merge_suggestion_ko": "권장 병합 결과:\\n```typescript\\n// 옵션 1: 내 변경 (api-v2.example.com)\\n// 옵션 2: Main 변경 (prod.example.com)\\n// 팀과 상의하여 올바른 URL을 선택하세요\\nexport const API_CONFIG = {{{{\\n  baseUrl: '선택 필요',  // 충돌: 어느 URL을 사용할지 결정\\n  timeout: 5000,\\n}}}};\\n```"}}"""


def _extract_json_from_text(text: str) -> Dict[str, Any]:
    """Extract the first JSON object from a text blob."""
    decoder = json.JSONDecoder()
    for idx, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            obj, _ = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            return obj
    raise ValueError("No valid JSON found in response")


def _strip_code_fence(text: str) -> str:
    """Remove a top-level fenced code block wrapper if present."""
    stripped = text.strip()
    if not stripped.startswith("```"):
        return stripped
    newline_idx = stripped.find("\n")
    if newline_idx == -1:
        return ""
    inner = stripped[newline_idx + 1 :]
    fence_idx = inner.rfind("```")
    if fence_idx != -1:
        inner = inner[:fence_idx]
    return inner.strip()


def analyze_conflict(
    file_path: str,
    my_changes: str,
    their_changes: str,
    line_overlap: bool,
    my_line_ranges: list[tuple[int, int]] | None = None,
    base_line_ranges: list[tuple[int, int]] | None = None,
    base_branch: str | None = None,
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

    prompt = create_conflict_prompt(
        file_path,
        my_changes,
        their_changes,
        line_overlap,
        my_line_ranges=my_line_ranges,
        base_line_ranges=base_line_ranges,
        base_branch=base_branch,
    )

    messages = [
        SystemMessage(content=CONFLICT_ANALYZER_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content

        if isinstance(content, dict):
            result = content
        else:
            content = str(content).strip()

            # Debug: print raw response
            print(f"[DEBUG] LLM Raw Response (first 500 chars):\n{content[:500]}\n")

            if not content:
                raise ValueError("LLM returned empty response")

            original_content = content
            content = _strip_code_fence(content)

            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                try:
                    result = _extract_json_from_text(content)
                except ValueError:
                    print(f"[ERROR] Could not find JSON in response. Original:\n{original_content}")
                    raise

            print(f"[DEBUG] Extracted JSON:\n{json.dumps(result)[:500]}\n")

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
