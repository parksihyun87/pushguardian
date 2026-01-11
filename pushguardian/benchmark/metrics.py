"""Performance and quality metrics collection module."""

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class NodeMetrics:
    """Metrics for a single node execution."""
    node_name: str
    start_time: float
    end_time: float
    duration_ms: float

    # Node-specific metrics
    findings_detected: int = 0
    search_queries: List[str] = field(default_factory=list)
    search_engine: Optional[str] = None
    results_count: int = 0

    # LLM metrics
    llm_called: bool = False
    llm_model: Optional[str] = None

    # Error tracking
    errors: List[str] = field(default_factory=list)


@dataclass
class SearchQualityMetrics:
    """Metrics for evaluating search quality."""

    # Query metrics
    query_text: str
    query_length: int  # Number of words
    search_engine: str
    iteration: int  # 0=first search, 1=retry

    # Result metrics
    total_results: int
    spam_filtered: int
    principle_links: List[str] = field(default_factory=list)
    example_links: List[str] = field(default_factory=list)

    # Quality indicators
    high_quality_domains_count: int = 0  # OWASP, NIST, GitHub official docs
    trusted_domain_ratio: float = 0.0  # Ratio of results from trusted domains

    # Performance
    search_latency_ms: float = 0.0

    # LLM assessment
    llm_sufficient: bool = False
    llm_reasoning: str = ""


@dataclass
class BenchmarkResult:
    """Complete benchmark result for a single test case."""

    # Test metadata
    test_name: str
    test_file: str
    timestamp: str

    # Overall metrics
    total_duration_ms: float
    total_duration_sec: float

    # Final results
    decision: str  # allow, block, override
    severity: str  # low, medium, high, critical

    # Node-by-node breakdown
    node_metrics: List[NodeMetrics] = field(default_factory=list)

    # Search quality metrics
    search_quality: List[SearchQualityMetrics] = field(default_factory=list)

    # Findings and links
    findings_count: int = 0
    principle_links_count: int = 0
    example_links_count: int = 0

    # Research metrics
    research_iterations: int = 0
    tools_used: List[str] = field(default_factory=list)

    # Quality indicators
    avg_query_length: float = 0.0
    total_search_time_ms: float = 0.0
    llm_calls_count: int = 0

    # Error tracking
    errors: List[str] = field(default_factory=list)


class MetricsCollector:
    """Collects metrics during workflow execution."""

    def __init__(self):
        self.current_node_start: Optional[float] = None
        self.current_node_name: Optional[str] = None
        self.workflow_start: Optional[float] = None

        self.node_metrics: List[NodeMetrics] = []
        self.search_metrics: List[SearchQualityMetrics] = []

        self.high_quality_domains = {
            "owasp.org",
            "cheatsheetseries.owasp.org",
            "nist.gov",
            "cwe.mitre.org",
            "nvd.nist.gov",
            "docs.github.com",
            "security.googleblog.com",
            "learn.microsoft.com",
        }

    def start_workflow(self):
        """Mark workflow start time."""
        self.workflow_start = time.time()

    def start_node(self, node_name: str):
        """Mark node execution start."""
        self.current_node_name = node_name
        self.current_node_start = time.time()
        # Debug: Confirm start time was set
        # print(f"    DEBUG: start_node({node_name}) at {self.current_node_start}")

    def end_node(self, node_name: str, state: Dict[str, Any]):
        """Mark node execution end and collect metrics."""
        if self.current_node_start is None:
            print(f"    DEBUG: end_node({node_name}) called but start_time is None!")
            return

        end_time = time.time()
        duration_ms = (end_time - self.current_node_start) * 1000

        # Debug: Check duration
        if duration_ms < 0.01:
            print(f"    DEBUG: Node {node_name} duration is suspiciously low: {duration_ms}ms (start={self.current_node_start}, end={end_time})")

        # Create basic node metrics
        metrics = NodeMetrics(
            node_name=node_name,
            start_time=self.current_node_start,
            end_time=end_time,
            duration_ms=round(duration_ms, 2)
        )

        # Extract node-specific metrics
        if node_name == "hard_policy_check":
            metrics.findings_detected = len(state.get("hard_findings", []))

        elif node_name == "soft_llm_judge":
            metrics.findings_detected = len(state.get("soft_findings", []))
            metrics.llm_called = True
            metrics.llm_model = "gpt-4o-mini"

        elif node_name in ["research_tavily", "research_serper", "research_duckduckgo"]:
            evidence = state.get("evidence", {})
            if hasattr(evidence, "search_queries"):
                metrics.search_queries = evidence.search_queries[-1:] if evidence.search_queries else []

            if "tavily" in node_name:
                metrics.search_engine = "tavily"
            elif "serper" in node_name:
                metrics.search_engine = "serper"
            elif "duckduckgo" in node_name:
                metrics.search_engine = "duckduckgo"

            # Count results
            if hasattr(evidence, "principle_links"):
                metrics.results_count = len(evidence.principle_links) + len(getattr(evidence, "example_links", []))

        elif node_name == "observation_validate":
            metrics.llm_called = True
            metrics.llm_model = "gpt-4o-mini"

        # Track errors
        if "errors" in state and state["errors"]:
            metrics.errors = state["errors"]

        self.node_metrics.append(metrics)

    def add_search_metrics(
        self,
        query: str,
        search_engine: str,
        iteration: int,
        results_before_filter: int,
        results_after_filter: int,
        principle_links: List[str],
        example_links: List[str],
        latency_ms: float,
        llm_sufficient: bool = False,
        llm_reasoning: str = ""
    ):
        """Add search quality metrics."""

        # Count high-quality domains
        all_links = principle_links + example_links
        high_quality_count = sum(
            1 for link in all_links
            if any(domain in link for domain in self.high_quality_domains)
        )

        trusted_ratio = high_quality_count / len(all_links) if all_links else 0.0

        metrics = SearchQualityMetrics(
            query_text=query,
            query_length=len(query.split()),
            search_engine=search_engine,
            iteration=iteration,
            total_results=results_after_filter,
            spam_filtered=results_before_filter - results_after_filter,
            principle_links=principle_links,
            example_links=example_links,
            high_quality_domains_count=high_quality_count,
            trusted_domain_ratio=round(trusted_ratio, 2),
            search_latency_ms=round(latency_ms, 2),
            llm_sufficient=llm_sufficient,
            llm_reasoning=llm_reasoning
        )

        self.search_metrics.append(metrics)

    def finalize(self, test_name: str, test_file: str, final_state: Dict[str, Any]) -> BenchmarkResult:
        """Create final benchmark result."""

        total_duration = (time.time() - self.workflow_start) * 1000 if self.workflow_start else 0

        # Calculate aggregate metrics
        avg_query_length = 0.0
        if self.search_metrics:
            avg_query_length = sum(m.query_length for m in self.search_metrics) / len(self.search_metrics)

        total_search_time = sum(m.search_latency_ms for m in self.search_metrics)
        llm_calls = sum(1 for m in self.node_metrics if m.llm_called)

        # Handle None final_state
        if final_state is None:
            final_state = {}

        # Extract final state info
        evidence = final_state.get("evidence", {})
        principle_links = getattr(evidence, "principle_links", []) if evidence else []
        example_links = getattr(evidence, "example_links", []) if evidence else []
        tools_used = getattr(evidence, "tools_used", []) if evidence else []

        all_findings = final_state.get("hard_findings", []) + final_state.get("soft_findings", [])

        result = BenchmarkResult(
            test_name=test_name,
            test_file=test_file,
            timestamp=datetime.now().isoformat(),
            total_duration_ms=round(total_duration, 2),
            total_duration_sec=round(total_duration / 1000, 2),
            node_metrics=self.node_metrics,
            search_quality=self.search_metrics,
            decision=final_state.get("decision", "unknown"),
            severity=final_state.get("severity", "unknown"),
            findings_count=len(all_findings),
            principle_links_count=len(principle_links),
            example_links_count=len(example_links),
            research_iterations=final_state.get("recheck_count", 0) + (1 if tools_used else 0),
            tools_used=tools_used,
            avg_query_length=round(avg_query_length, 2),
            total_search_time_ms=round(total_search_time, 2),
            llm_calls_count=llm_calls,
            errors=final_state.get("errors", [])
        )

        return result
