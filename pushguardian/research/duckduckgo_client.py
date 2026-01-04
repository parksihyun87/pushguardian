"""DuckDuckGo search client for research (3rd fallback)."""

from typing import List, Dict, Any


def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search using DuckDuckGo (no API key required).

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        List of search results with url, title, snippet
    """
    try:
        # Use duckduckgo-search library (free, no API key)
        from duckduckgo_search import DDGS

        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(query, max_results=max_results)

            for item in search_results:
                results.append(
                    {
                        "url": item.get("href", ""),
                        "title": item.get("title", ""),
                        "content": item.get("body", ""),
                        "score": 0.6,  # DuckDuckGo doesn't provide scores
                    }
                )

        return results

    except ImportError:
        print("DuckDuckGo search requires: pip install duckduckgo-search")
        return []
    except Exception as e:
        print(f"DuckDuckGo search failed: {e}")
        return []
