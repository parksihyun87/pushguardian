"""Serper search client for research (backup)."""

import os
import requests
from typing import List, Dict, Any


def search_serper(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search using Serper API (Google Search).

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of search results with url, title, snippet
    """
    api_key = os.getenv("SERPER_API_KEY")

    if not api_key:
        return []

    try:
        url = "https://google.serper.dev/search"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        payload = {"q": query, "num": max_results}

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get("organic", []):
            results.append(
                {
                    "url": item.get("link", ""),
                    "title": item.get("title", ""),
                    "content": item.get("snippet", ""),
                    "score": 0.7,  # Serper doesn't provide scores
                }
            )

        return results

    except Exception as e:
        print(f"Serper search failed: {e}")
        return []
