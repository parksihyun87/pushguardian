"""LLM을 사용하여 네이버 검색 쿼리를 동적으로 생성"""

import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


QUERY_GEN_SYSTEM_PROMPT = """당신은 보안 이슈에 대한 한글 검색 쿼리를 생성하는 전문가입니다.

주어진 보안 이슈(Finding)를 분석하여, 네이버에서 유용한 한글 자료를 찾을 수 있는 **최적의 검색 쿼리**를 생성하세요.

**좋은 쿼리의 조건:**
1. **보안 중심**: 단순 기능이 아닌 보안 취약점과 방어 방법에 초점
2. **구체적**: 추상적인 용어보다 구체적인 기술 용어 사용
3. **한글 자료 친화적**: 한국 개발자들이 자주 찾는 키워드 사용
4. **적절한 길이**: 3-6단어 정도

**예시:**
- XSS 취약점 → "XSS 공격 방어 HTML 이스케이프"
- SQL Injection → "SQL Injection 방어 PreparedStatement"
- DTO 검증 → "입력 검증 보안 sanitization"

JSON 형식으로 응답:
{
    "query": "검색 쿼리 (3-6단어)",
    "reason": "이 쿼리를 선택한 이유 (1-2문장)"
}
"""


def generate_naver_query(finding_title: str, finding_detail: str, finding_kind: str) -> str:
    """
    LLM을 사용하여 Finding에 최적화된 네이버 검색 쿼리 생성.

    Args:
        finding_title: Finding 제목
        finding_detail: Finding 상세 설명
        finding_kind: Finding 종류 (dto, xss, sql_injection 등)

    Returns:
        생성된 검색 쿼리
    """
    prompt = f"""다음 보안 이슈에 대한 한글 자료를 찾기 위한 네이버 검색 쿼리를 생성하세요.

**보안 이슈:**
- 종류: {finding_kind}
- 제목: {finding_title}
- 상세: {finding_detail[:300]}

네이버에서 **보안 관점의 실용적인 한글 자료**를 찾을 수 있는 최적의 쿼리를 생성하세요.

JSON 형식으로만 응답하세요 (다른 텍스트 없이).
"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    messages = [
        SystemMessage(content=QUERY_GEN_SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # JSON 추출
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        result = json.loads(content)
        query = result.get("query", "")
        reason = result.get("reason", "")

        print(f"🔍 LLM 생성 쿼리: '{query}'")
        print(f"   이유: {reason}")

        return query if query else "웹 보안 입력 검증"  # 폴백

    except Exception as e:
        print(f"⚠️ 쿼리 생성 실패: {e}")
        # 폴백: 간단한 쿼리 생성
        if "xss" in finding_detail.lower():
            return "XSS 방어 방법"
        elif "sql" in finding_detail.lower():
            return "SQL Injection 방어"
        else:
            return f"{finding_kind} 보안"
