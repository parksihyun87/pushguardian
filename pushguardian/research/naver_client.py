"""네이버 검색 API 클라이언트 (한글 자료 검색용)."""

import os
from typing import List, Dict, Any
import requests


def search_naver(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    네이버 검색 API로 한글 자료를 검색합니다.

    Args:
        query: 검색 쿼리
        max_results: 최대 결과 개수 (네이버는 최대 100)

    Returns:
        List of search results with url, title, content (짧은 snippet)
    """
    client_id = os.getenv("NAVER_CLIENT_ID")
    client_secret = os.getenv("NAVER_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("네이버 API 키가 설정되지 않음 (NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)")
        return []

    try:
        # 네이버 웹 검색 API (한국어 문서)
        url = "https://openapi.naver.com/v1/search/webkr.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        }
        params = {
            "query": query,
            "display": min(max_results, 100),  # 네이버는 최대 100
            "sort": "sim",  # 정확도 순 (sim) 또는 날짜순 (date)
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for item in data.get("items", []):
            # HTML 태그 제거 (네이버는 <b> 태그로 강조)
            title = item.get("title", "").replace("<b>", "").replace("</b>", "")
            description = item.get("description", "").replace("<b>", "").replace("</b>", "")

            # snippet 길이 제한
            snippet_max_len = 400
            snippet = description[:snippet_max_len]
            if len(description) > snippet_max_len:
                snippet += "..."

            results.append(
                {
                    "url": item.get("link", ""),
                    "title": title,
                    "content": snippet,
                    "score": 0.5,  # 네이버는 점수를 제공하지 않으므로 기본값
                }
            )

        print(f"네이버 검색 완료: {len(results)}개 결과")
        return results

    except requests.exceptions.RequestException as e:
        print(f"네이버 검색 API 호출 실패: {e}")
        return []
    except Exception as e:
        print(f"네이버 검색 중 오류 발생: {e}")
        return []
