"""LLM-based link title annotator: 영어 요약을 짧은 한국어 제목으로 변환."""

from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from ..report.models import Evidence


SYSTEM_PROMPT = """너는 보안/개발 관련 웹 문서를 한국어로 요약하는 어시스턴트다.

역할:
- 주어진 링크 요약(summary)이 영어일 경우, 이를 기반으로 짧은 한국어 제목을 만들어라.
- 제목은 10~25자 이내로 자연스러운 한국어 문장/구로 작성한다.
- 링크의 핵심 주제(예: SQL 인젝션, 시크릿 관리, Docker 권한 등)를 분명하게 드러내라.

출력 형식:
- JSON 배열로만 응답한다.
- 각 항목은 {"id": number, "ko_title": "짧은 한국어 제목"} 형태여야 한다.
- JSON 이외의 설명 텍스트는 절대 포함하지 마라.
"""


def _looks_english(text: str) -> bool:
    """간단한 휴리스틱: 알파벳 비율이 높으면 영어로 간주."""
    if not text:
        return False
    letters = sum(ch.isalpha() for ch in text)
    if letters == 0:
        return False
    # 한글/기호 섞임을 감안해, 알파벳이 일정 비율 이상이면 영어로 본다
    return letters / max(len(text), 1) > 0.4


def annotate_link_titles_with_llm(evidence: Evidence, max_items: int = 8) -> None:
    """
    Evidence 내 링크 요약(summary)이 영어일 경우, LLM을 사용해 짧은 한국어 제목(summary_ko)을 추가한다.

    - Evidence 객체를 제자리(in-place)에서 수정한다.
    - 실패 시에는 조용히 무시하고 기존 summary를 그대로 사용한다.
    """
    candidates: List[Dict[str, Any]] = []

    def collect_candidates(infos: List[Dict[str, Any]]) -> None:
        for info in infos:
            if len(candidates) >= max_items:
                break
            if "summary_ko" in info:
                continue
            summary = (info.get("summary") or "").strip()
            if not summary:
                continue
            if not _looks_english(summary):
                continue
            candidates.append({"info": info, "summary": summary})

    collect_candidates(evidence.principle_link_infos)
    collect_candidates(evidence.example_link_infos)

    if not candidates:
        return

    # LLM 호출 준비
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    payload = [
        {"id": idx + 1, "summary": c["summary"]} for idx, c in enumerate(candidates)
    ]

    user_content = (
        "다음은 보안/개발 관련 웹 문서의 영어 요약 목록이다. "
        "각 항목에 대해, 링크의 주제를 잘 드러내는 짧은 한국어 제목을 만들어라.\n\n"
        "입력 형식:\n"
        '[{"id": 1, "summary": "..."}, ...]\n\n'
        "출력 형식은 동일한 id를 가진 JSON 배열이어야 한다.\n"
        "예시: [{\"id\": 1, \"ko_title\": \"시크릿 안전 저장 가이드\"}]\n\n"
        f"입력:\n{payload}"
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # 코드 블록 감싸짐 방어
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        import json

        data = json.loads(content)
        if not isinstance(data, list):
            return

        by_id = {item.get("id"): item.get("ko_title", "").strip() for item in data}

        for idx, c in enumerate(candidates, start=1):
            ko = by_id.get(idx)
            if ko:
                c["info"]["summary_ko"] = ko

    except Exception:
        # 요약 실패 시에는 조용히 무시 (로그는 나중에 필요하면 추가)
        return


