"""Tavily search client for research."""

import os
from typing import List, Dict, Any
from tavily import TavilyClient


def search_tavily(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search using Tavily API.

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of search results with url, title, content (짧은 요약 snippet)
    """
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return []

    try:
        client = TavilyClient(api_key=api_key)

        # 검색 품질 차이가 크지 않은 한, latency를 줄이기 위해 기본 search_depth를 'basic'으로 사용
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )

        results = []
        for item in response.get("results", []):
            raw_content = item.get("content", "") or ""
            # 전체 본문 대신, downstream에서는 링크만 쓰므로 짧은 snippet으로 잘라서 전달
            snippet_max_len = 400
            snippet = raw_content[:snippet_max_len]
            if len(raw_content) > snippet_max_len:
                snippet += "..."

            results.append(
                {
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "content": snippet,
                    "score": item.get("score", 0.5),
                }
            )

        return results

    except Exception as e:
        print(f"Tavily search failed: {e}")
        return []
