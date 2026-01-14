"""Data models for findings and evidence."""

from dataclasses import dataclass, field
from typing import Literal, List, Dict, Any


@dataclass
class ConflictWarning:
    """Represents a potential merge conflict."""

    file_path: str  # 충돌 발생 가능 파일
    conflict_probability: float  # 0.0 to 1.0
    conflict_type: Literal["routing", "config", "refactoring", "semantic_duplicate", "unknown"]
    recommendation: Literal["keep_both", "choose_one", "manual_merge"]
    advice_ko: str  # 한국어 조언
    merge_suggestion_ko: str  # 병합 권장 방법
    my_changes: str  # 내 diff
    their_changes: str  # 상대방 diff
    line_overlap: bool  # 라인 범위 겹침 여부

    def to_dict(self):
        return {
            "file_path": self.file_path,
            "conflict_probability": self.conflict_probability,
            "conflict_type": self.conflict_type,
            "recommendation": self.recommendation,
            "advice_ko": self.advice_ko,
            "merge_suggestion_ko": self.merge_suggestion_ko,
            "my_changes": self.my_changes,
            "their_changes": self.their_changes,
            "line_overlap": self.line_overlap,
        }


@dataclass
class Finding:
    """Represents a security or best-practice finding."""

    kind: Literal["secret", "file", "dto", "dependency", "permission", "structure"]
    title: str
    detail: str
    confidence: float  # 0.0 to 1.0
    severity: Literal["low", "medium", "high", "critical"]
    fix_now: str  # 1-3 lines of immediate fix steps

    def to_dict(self):
        return {
            "kind": self.kind,
            "title": self.title,
            "detail": self.detail,
            "confidence": self.confidence,
            "severity": self.severity,
            "fix_now": self.fix_now,
        }


@dataclass
class Evidence:
    """Represents research evidence and links."""

    # Backward-compatible raw URL lists (기존 필드: 여전히 사용 가능)
    principle_links: list[str] = field(default_factory=list)
    example_links: list[str] = field(default_factory=list)

    # 확장된 링크 메타데이터: 각 링크에 대한 토큰/요약 정보를 포함
    # 예: {"url": "...", "title": "...", "role": "principle", "source": "owasp", "summary": "..."}
    principle_link_infos: List[Dict[str, Any]] = field(default_factory=list)
    example_link_infos: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""
    # Debug info for developers
    research_iterations: int = 0
    tools_used: list[str] = field(default_factory=list)
    llm_observations: list[dict] = field(default_factory=list)
    search_queries: list[str] = field(default_factory=list)
    search_latencies: list[float] = field(default_factory=list)  # Latency in milliseconds for each search

    def to_dict(self):
        return {
            "principle_links": self.principle_links,
            "example_links": self.example_links,
            "principle_link_infos": self.principle_link_infos,
            "example_link_infos": self.example_link_infos,
            "notes": self.notes,
            "research_iterations": self.research_iterations,
            "tools_used": self.tools_used,
            "llm_observations": self.llm_observations,
            "search_queries": self.search_queries,
            "search_latencies": self.search_latencies,
        }
