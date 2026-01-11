"""네이버 검색 결과를 LLM으로 필터링하여 고품질 자료만 선별"""

import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


NAVER_FILTER_SYSTEM_PROMPT = """당신은 보안 자료의 품질을 평가하는 전문가입니다.

네이버 검색으로 찾은 한글 보안 자료들을 평가하여, **정말 유용한 자료만** 선별해주세요.

**평가 기준 (모두 충족해야 함):**
1. **직접적 관련성**: 보안 이슈와 **정확히** 일치하는 주제인가? (예: DTO 이슈면 Spring Security가 아닌 DTO 검증)
2. **실용적 깊이**: 단순 개념 설명이 아닌, **실제 코드 예제**나 구체적인 해결책이 있는가?
3. **기술적 정확성**: 제목과 스니펫이 보안 이슈를 정확히 다루는가?
4. **바로 적용 가능**: 개발자가 읽고 바로 적용할 수 있는 내용인가?

**엄격하게 제외:**
- 주제가 다른 글 (예: DTO 이슈인데 인증/권한 관련 글)
- 단순 TIL(Today I Learned) 형식의 학습 노트
- 광고/홍보성 내용
- 단순 용어 정의만 있는 글
- 제목만 관련있고 내용이 다른 글
- **카테고리/인덱스 페이지** - URL에 `/category/`, `/tag/`, `/list/` 포함된 경우
- **목차 페이지** - 실제 글이 아닌 링크 모음 페이지

**중요**: 엄격하게 평가하세요. 애매하면 제외하세요. **특히 URL이 카테고리나 목록 페이지인 경우 제외**하세요. 최대 2개만 선별하거나, 적절한 자료가 없으면 0-1개만 선택하세요.

JSON 형식으로 응답:
{
    "selected": [
        {
            "url": "URL",
            "title": "제목",
            "reason": "선택 이유 (한글, 1-2문장)"
        }
    ]
}
"""


def filter_naver_results(
    results: List[Dict[str, Any]],
    finding_title: str,
    finding_detail: str,
    mode: str = "security"  # "security" or "tutorial"
) -> List[Dict[str, Any]]:
    """
    네이버 검색 결과를 LLM으로 필터링하여 고품질 자료만 선별.

    Args:
        results: 네이버 검색 결과 리스트
        finding_title: Finding 제목 (또는 약점 스택명)
        finding_detail: Finding 상세 설명 (또는 학습 개념)
        mode: "security" (보안 자료) 또는 "tutorial" (학습 자료)

    Returns:
        선별된 결과 리스트 (최대 2-3개)
    """
    if not results:
        return []

    # 1차 필터: 카테고리/목록 페이지 제외
    bad_patterns = ['/category/', '/tag/', '/list/', '/archive/', '/tags/']
    filtered_results = []
    for result in results:
        url = result.get("url", "").lower()
        if not any(pattern in url for pattern in bad_patterns):
            filtered_results.append(result)
        else:
            print(f"  ⚠️ 카테고리 페이지 제외: {url[:60]}...")

    if not filtered_results:
        print(f"  ⚠️ 1차 필터 후 결과 없음")
        return []

    print(f"  ✅ 1차 필터: {len(results)}개 → {len(filtered_results)}개 (카테고리 페이지 제외)")
    results = filtered_results

    # 결과 요약 (LLM에게 전달)
    results_summary = []
    for i, result in enumerate(results[:10], 1):  # 최대 10개만 평가
        results_summary.append({
            "index": i,
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": result.get("description", "")[:200]  # 스니펫 일부만
        })

    # 모드에 따라 프롬프트 변경
    if mode == "tutorial":
        prompt = f"""다음 **기술 스택/개념**에 대한 한글 학습 자료들을 평가해주세요.

**학습 주제:**
- 기술 스택: {finding_title}
- 관련 개념: {finding_detail[:300]}

**중요**: 이것은 **학습 자료**입니다. 초보자가 이해하기 쉬운 튜토리얼, 실습 예제, 기본 개념 설명 자료를 찾아야 합니다.

**검색 결과:**
{json.dumps(results_summary, ensure_ascii=False, indent=2)}

위 결과를 평가할 때:
1. **기초 친화적인가?** - 초보자도 이해할 수 있는 설명인가?
2. **실습 예제가 있는가?** - 따라 할 수 있는 코드 예제가 포함되어 있는가?
3. **체계적인가?** - 단계별로 잘 정리된 튜토리얼인가?
4. **실제 글인가?** - URL에 `/category/`, `/tag/`, `/list/`가 있으면 제외 (카테고리 페이지)

**실제로 유용한 학습 자료 2-3개** 선별하세요.
모두 품질이 낮거나 너무 고급/전문적이거나 카테고리 페이지면 선택하지 마세요.

JSON 형식으로만 응답하세요 (다른 텍스트 없이).
"""
    else:  # security mode
        prompt = f"""다음 **보안 이슈**와 관련하여, 네이버 검색으로 찾은 한글 자료들을 평가해주세요.

**보안 이슈:**
- 제목: {finding_title}
- 상세: {finding_detail[:300]}

**중요**: 이것은 **보안 이슈**입니다. 단순 기능 구현이 아닌, **보안 관점**에서 문제를 해결하는 자료를 찾아야 합니다.

**검색 결과:**
{json.dumps(results_summary, ensure_ascii=False, indent=2)}

위 결과를 평가할 때:
1. **보안 중심인가?** - XSS, SQL Injection 등 보안 취약점을 다루는가?
2. **구체적인 방어 방법** - HTML 이스케이프, sanitization 등 방어 코드가 있는가?
3. **단순 validation이 아닌 보안 validation** - 형식 검증만이 아닌 보안 검증인가?
4. **실제 글인가?** - URL에 `/category/`, `/tag/`, `/list/`가 있으면 제외 (카테고리 페이지)

**실제로 유용한 자료 1-2개만** 선별하세요.
모두 품질이 낮거나 보안과 무관하거나 카테고리 페이지면 아예 선택하지 마세요.

JSON 형식으로만 응답하세요 (다른 텍스트 없이).
"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    messages = [
        SystemMessage(content=NAVER_FILTER_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        print(f"🤖 LLM 필터링 시작: {len(results)}개 결과 평가 중...")
        response = llm.invoke(messages)
        content = response.content.strip()

        print(f"📝 LLM 응답 (처음 200자): {content[:200]}")

        # JSON 추출
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)
        selected = result.get("selected", [])

        print(f"✅ LLM이 {len(selected)}개 선별함")

        # 선별된 결과 반환 (원본 결과에서 매칭)
        filtered_results = []
        for item in selected:
            url = item.get("url", "")
            print(f"  - 선별: {url[:50]}...")
            # 원본 결과에서 찾기
            for orig in results:
                if orig.get("url") == url:
                    # reason 추가
                    orig["llm_reason"] = item.get("reason", "")
                    filtered_results.append(orig)
                    break

        if len(filtered_results) == 0:
            print(f"⚠️ LLM이 아무것도 선택하지 않음. 폴백: 상위 2개 사용")
            return results[:2]

        print(f"🤖 LLM 필터링 완료: {len(results)}개 → {len(filtered_results)}개 선별")
        return filtered_results[:3]  # 최대 3개

    except Exception as e:
        print(f"⚠️ LLM 필터링 실패: {e}")
        import traceback
        print(traceback.format_exc())
        # 폴백: 상위 2개만 반환
        print(f"📌 폴백: 상위 2개 사용")
        return results[:2]
