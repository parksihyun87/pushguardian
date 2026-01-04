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
        List of search results with url, title, content
    """
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return []

    try:
        client = TavilyClient(api_key=api_key)

        response = client.search(query=query, max_results=max_results, search_depth="advanced")

        results = []
        for item in response.get("results", []):
            results.append(
                {
                    "url": item.get("url", ""),
                    "title": item.get("title", ""),
                    "content": item.get("content", ""),
                    "score": item.get("score", 0.5),
                }
            )

        return results

    except Exception as e:
        print(f"Tavily search failed: {e}")
        return []
