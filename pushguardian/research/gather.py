"""Research gathering and categorization."""

import time
from typing import List, Dict, Any, Tuple
from .tavily_client import search_tavily
from .serper_client import search_serper
from .duckduckgo_client import search_duckduckgo
from ..report.models import Finding, Evidence


PRINCIPLE_KEYWORDS = [
    "best practice",
    "principle",
    "guide",
    "documentation",
    "official",
    "security",
    "owasp",
    "standard",
]

EXAMPLE_KEYWORDS = [
    "example",
    "tutorial",
    "how to",
    "demo",
    "sample",
    "walkthrough",
    "step by step",
]


def _build_compact_summary(title: str, content: str, max_len: int = 80) -> str:
    """
    Build a short, compact summary string for a link.

    - 우선 제목(title)을 사용하되, 사이트 이름/부제 제거
    - 너무 길면 앞부분만 잘라 간결하게 표시
    - 제목이 없으면 본문 첫 줄에서 스니펫 생성
    """
    title = (title or "").strip()
    content = (content or "").strip()

    if title:
        # 공통 패턴 구분자 기준으로 사이트명/부제 제거
        for sep in [" - ", " | ", " — ", " :: "]:
            if sep in title:
                title = title.split(sep)[0].strip()
                break

        if len(title) > max_len:
            return title[: max_len - 1] + "…"
        return title

    if content:
        first_line = content.split("\n", 1)[0].strip()
        if len(first_line) > max_len:
            return first_line[: max_len - 1] + "…"
        return first_line

    return ""


def categorize_link(url: str, title: str, content: str) -> str:
    """
    Categorize a search result as 'principle' or 'example'.

    Args:
        url: Result URL
        title: Result title
        content: Result snippet/content

    Returns:
        'principle' or 'example'
    """
    text = (url + " " + title + " " + content).lower()

    # Count keyword matches
    principle_score = sum(1 for kw in PRINCIPLE_KEYWORDS if kw in text)
    example_score = sum(1 for kw in EXAMPLE_KEYWORDS if kw in text)

    # Boost for official docs
    if any(domain in url for domain in ["docs.", "documentation", "official"]):
        principle_score += 2

    # Boost for tutorial sites
    if any(
        domain in url for domain in ["tutorial", "example", "github.com", "stackoverflow"]
    ):
        example_score += 1

    return "principle" if principle_score >= example_score else "example"


def gather_research(
    findings: List[Finding],
    weak_stack_touched: List[str],
    search_engine: str = "tavily",
    refined_query: str = "",
    learning_points: List[Dict[str, Any]] = None,
) -> Evidence:
    """
    Gather research evidence for findings.

    Args:
        findings: List of findings to research
        weak_stack_touched: List of weak stacks that were touched
        search_engine: Which search engine to use ("tavily", "serper", "duckduckgo")
        refined_query: Optional refined query from LLM planner
        learning_points: Optional learning points from LLM judge (for weak stacks)

    Returns:
        Evidence object with categorized links
    """
    if learning_points is None:
        learning_points = []
    evidence = Evidence()
    evidence.research_iterations = 1
    evidence.tools_used = [search_engine]

    if not findings and not weak_stack_touched:
        return evidence

    # Build search queries
    queries = []

    # Use refined query if provided, otherwise build default
    if refined_query:
        query = refined_query
        queries.append(("finding", query))
        evidence.search_queries.append(query)
    elif findings:
        # Take top finding
        top_finding = max(findings, key=lambda f: f.confidence)

        # Build smarter query based on finding type (영어)
        if top_finding.kind == "secret":
            query = "prevent secrets in git commits API keys environment variables best practices"
            query_ko = "git 커밋에서 시크릿과 API 키, 환경 변수 노출을 방지하는 보안 모범 사례"
        elif top_finding.kind == "file":
            query = "gitignore sensitive files credentials environment configuration security"
            query_ko = "민감한 설정/인증 정보 파일을 git에서 제외하는 방법과 .gitignore 보안 모범 사례"
        elif top_finding.kind == "dto":
            query = "DTO schema validation backend API security best practices"
            query_ko = "백엔드 DTO/스키마 검증과 API 보안 모범 사례"
        elif top_finding.kind == "dependency":
            query = "dependency management security vulnerabilities package updates"
            query_ko = "의존성 관리와 보안 취약점, 패키지 업데이트 전략"
        elif top_finding.kind == "permission":
            query = "file permissions security access control configuration"
            query_ko = "파일 퍼미션과 접근 제어 설정 보안 모범 사례"
        else:
            # Fallback to generic
            query = f"{top_finding.kind} security best practices code review"
            query_ko = f"{top_finding.kind} 관련 보안 모범 사례와 코드 리뷰 체크리스트"

        # 영어/한국어 쿼리를 모두 사용하여 다양한 자료 수집
        queries.append(("finding", query))
        evidence.search_queries.append(query)

        queries.append(("finding", query_ko))
        evidence.search_queries.append(query_ko)

    # Query for weak stack learning
    if weak_stack_touched:
        # If we have specific learning points from LLM, use them for targeted search
        if learning_points:
            for lp in learning_points[:2]:  # Top 2 learning points
                # Use the stack from learning point (LLM判断), not from weak_stack_touched
                lp_stack = lp.get("stack", weak_stack_touched[0])
                concept = lp.get("concept", "")
                if concept:
                    query = f"{lp_stack} {concept} tutorial examples"
                    queries.append(("learning", query))
                    evidence.search_queries.append(query)
        else:
            # Fallback to generic learning query (한국어 위주로 약점 스택 학습 자료 검색)
            stack = weak_stack_touched[0]  # Take first weak stack
            # 예: "react 기초 튜토리얼 모범 사례 예제", "docker 입문 튜토리얼 보안 베스트 프랙티스"
            query = f"{stack} 기초 튜토리얼 모범 사례 예제"
            queries.append(("learning", query))
            evidence.search_queries.append(query)

    # Execute searches
    for query_type, query in queries:
        # Measure search latency
        start_time = time.time()

        if search_engine == "tavily":
            results = search_tavily(query, max_results=5)
        elif search_engine == "serper":
            results = search_serper(query, max_results=5)
        elif search_engine == "duckduckgo":
            results = search_duckduckgo(query, max_results=5)
        else:
            results = []

        # Record latency in milliseconds
        latency_ms = (time.time() - start_time) * 1000
        evidence.search_latencies.append(latency_ms)
        print(f"  [BENCHMARK] Search '{query[:50]}...' took {latency_ms:.2f}ms using {search_engine}")

        # Categorize and add to evidence
        for result in results:
            url = result.get("url", "")
            if not url:
                continue

            # Filter out irrelevant domains
            spam_domains = [
                "eng.sk.com",  # SK company site
                "mdpi.com",    # Academic papers (often not practical)
                "linkedin.com",
                "facebook.com",
                "twitter.com",
                "reddit.com",  # Can be good but often too casual
                "akamai.com",  # CDN promotional content
                "cloudflare.com",  # CDN promotional content
                "advertisement",
                "glossary",  # Generic glossary pages
                # 한국어 페이지(`/ko/`, `/kr/`)는 허용하여 국내/한글 문서를 막지 않음
                "youtube.com",  # Video content (not practical for quick reference)
                "pinterest.com",
                "instagram.com",
            ]

            if any(spam in url.lower() for spam in spam_domains):
                continue

            # Categorize first
            title = result.get("title", "") or ""
            content = result.get("content", "") or ""
            category = categorize_link(result.get("url", ""), title, content)

            # High-quality sources for principles
            principle_sources = [
                "owasp.org",
                "cheatsheetseries.owasp.org",
                "nist.gov",
                "cwe.mitre.org",
                "nvd.nist.gov",
                "docs.github.com/security",
                "security.googleblog.com",
                "learn.microsoft.com/security",
            ]

            # High-quality sources for examples
            example_sources = [
                "github.com",
                "stackoverflow.com",
                "dev.to",
                "auth0.com/blog",
                "snyk.io/blog",
            ]

            # Calculate quality score
            is_high_quality_principle = any(src in url.lower() for src in principle_sources)
            is_high_quality_example = any(src in url.lower() for src in example_sources)

            # 간단한 source 토큰 분류
            source_tag = "other"
            if is_high_quality_principle or is_high_quality_example:
                if "owasp" in url.lower():
                    source_tag = "owasp"
                elif "github.com" in url.lower():
                    source_tag = "github"
                elif "stackoverflow.com" in url.lower():
                    source_tag = "stackoverflow"
                elif "nist.gov" in url.lower():
                    source_tag = "nist"
                else:
                    source_tag = "trusted"
            elif "blog" in url.lower():
                source_tag = "blog"

            # 한 줄 요약(summary) 생성: 제목/본문에서 사이트명 등은 제거하고 짧게 잘라 가독성 향상
            summary = _build_compact_summary(title, content, max_len=80)

            link_info = {
                "url": url,
                "title": title,
                "role": category,  # "principle" or "example"
                "source": source_tag,
                "summary": summary,
            }

            # Prioritize high-quality sources
            if category == "principle":
                if is_high_quality_principle:
                    # Insert at beginning for high quality
                    if url not in evidence.principle_links and len(evidence.principle_links) < 4:
                        evidence.principle_links.insert(0, url)
                        evidence.principle_link_infos.insert(0, link_info)
                elif len(evidence.principle_links) < 4 and url not in evidence.principle_links:
                    evidence.principle_links.append(url)
                    evidence.principle_link_infos.append(link_info)
            else:  # example
                if is_high_quality_example:
                    # Insert at beginning for high quality
                    if url not in evidence.example_links and len(evidence.example_links) < 3:
                        evidence.example_links.insert(0, url)
                        evidence.example_link_infos.insert(0, link_info)
                elif len(evidence.example_links) < 3 and url not in evidence.example_links:
                    evidence.example_links.append(url)
                    evidence.example_link_infos.append(link_info)

    # Add notes
    if findings:
        evidence.notes = f"Research for: {findings[0].title}"
    elif weak_stack_touched:
        evidence.notes = f"Learning resources for: {', '.join(weak_stack_touched)}"

    return evidence


def merge_evidence(old: Evidence, new: Evidence) -> Evidence:
    """Merge two Evidence objects, avoiding duplicates."""
    merged = Evidence()

    merged.principle_links = list(set(old.principle_links + new.principle_links))
    merged.example_links = list(set(old.example_links + new.example_links))

    # 메타정보(annotated link infos)는 URL 기준으로 중복 제거
    seen_urls_principle = set()
    for info in old.principle_link_infos + new.principle_link_infos:
        url = info.get("url")
        if not url or url in seen_urls_principle:
            continue
        seen_urls_principle.add(url)
        merged.principle_link_infos.append(info)

    seen_urls_example = set()
    for info in old.example_link_infos + new.example_link_infos:
        url = info.get("url")
        if not url or url in seen_urls_example:
            continue
        seen_urls_example.add(url)
        merged.example_link_infos.append(info)
    merged.notes = (old.notes + " | " + new.notes) if old.notes and new.notes else (old.notes or new.notes)

    # Merge debug info
    merged.research_iterations = old.research_iterations + new.research_iterations
    merged.tools_used = list(set(old.tools_used + new.tools_used))
    merged.llm_observations = old.llm_observations + new.llm_observations
    merged.search_queries = old.search_queries + new.search_queries
    merged.search_latencies = old.search_latencies + new.search_latencies

    return merged
