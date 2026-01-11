"""Benchmark runner for testing workflow performance."""

import os
import time
from pathlib import Path
from typing import List
from .metrics import MetricsCollector, BenchmarkResult
from ..graph import build_graph


def run_benchmark_on_file(test_file: Path, test_name: str) -> BenchmarkResult:
    """
    Run benchmark on a single test file.

    Args:
        test_file: Path to test diff file
        test_name: Name for this test case

    Returns:
        BenchmarkResult with all metrics
    """
    # Read diff content
    with open(test_file, 'r', encoding='utf-8') as f:
        diff_text = f.read()

    # Create metrics collector
    collector = MetricsCollector()
    collector.start_workflow()

    # Build and run graph
    graph = build_graph()

    initial_state = {
        "diff_text": diff_text,
        "mode": "cli",
        "repo_root": None,
    }

    # Track execution with metrics
    final_state = initial_state  # Initialize with initial state

    for chunk in graph.stream(initial_state):
        # chunk is a dict like {"node_name": state}
        for node_name, state in chunk.items():
            # Debug: Check if state is None
            if state is None:
                print(f"    DEBUG: Node '{node_name}' returned None state")
                continue

            # NOTE: stream() returns AFTER the node has executed
            # So we can't measure timing here. We need to use a different approach.
            # For now, just collect the results without timing.

            try:
                # Don't call start_node here - node already executed
                # collector.start_node(node_name)

                # Capture search metrics if it's a research node
                if node_name in ["research_tavily", "research_serper", "research_duckduckgo"]:
                    evidence = state.get("evidence") if state else None

                    # Get search engine name
                    search_engine = "unknown"
                    if "tavily" in node_name:
                        search_engine = "tavily"
                    elif "serper" in node_name:
                        search_engine = "serper"
                    elif "duckduckgo" in node_name:
                        search_engine = "duckduckgo"

                    # Extract queries (handle None or dict evidence)
                    if evidence:
                        if hasattr(evidence, "search_queries"):
                            queries = evidence.search_queries
                        elif isinstance(evidence, dict):
                            queries = evidence.get("search_queries", [])
                        else:
                            queries = []
                    else:
                        queries = []

                    # Extract latencies (handle None or dict evidence)
                    if evidence:
                        if hasattr(evidence, "search_latencies"):
                            latencies = evidence.search_latencies
                        elif isinstance(evidence, dict):
                            latencies = evidence.get("search_latencies", [])
                        else:
                            latencies = []
                    else:
                        latencies = []

                    # Debug: Print what we collected
                    print(f"    DEBUG: Node {node_name} - Queries: {len(queries)}, Latencies: {len(latencies)}")
                    if latencies:
                        print(f"    DEBUG: Latencies: {latencies}")

                    # Get links (handle None or dict evidence)
                    if evidence:
                        if hasattr(evidence, "principle_links"):
                            principle_links = evidence.principle_links
                            example_links = evidence.example_links
                        elif isinstance(evidence, dict):
                            principle_links = evidence.get("principle_links", [])
                            example_links = evidence.get("example_links", [])
                        else:
                            principle_links = []
                            example_links = []
                    else:
                        principle_links = []
                        example_links = []

                    iteration = state.get("recheck_count", 0) if state else 0

                # Store final state (always update to latest)
                final_state = state

                # Skip timing collection since stream() returns after execution
                # collector.end_node(node_name, state)

                # Add search metrics after node completion
                if node_name in ["research_tavily", "research_serper", "research_duckduckgo"]:
                    # Get LLM assessment if available (from observation_validate)
                    research_plan = state.get("research_plan", {}) if state else {}
                    llm_sufficient = research_plan.get("next_action", "done") == "done" if research_plan else True
                    llm_reasoning = research_plan.get("reasoning", "") if research_plan else ""

                    # Assume no spam filtering for now (we'd need to instrument gather.py to get exact numbers)
                    total_results = len(principle_links) + len(example_links)

                    # Add metrics for each query executed (queries and latencies should have same length)
                    for i in range(len(queries)):
                        query = queries[i]
                        latency_ms = latencies[i] if i < len(latencies) else 0.0

                        collector.add_search_metrics(
                            query=query,
                            search_engine=search_engine,
                            iteration=iteration,
                            results_before_filter=total_results,  # Simplified
                            results_after_filter=total_results,
                            principle_links=principle_links,
                            example_links=example_links,
                            latency_ms=latency_ms,
                            llm_sufficient=llm_sufficient,
                            llm_reasoning=llm_reasoning
                        )
            except Exception as e:
                # If error occurs in this node, log and continue
                import traceback
                import sys
                print(f"    Warning: Error in node {node_name}: {e}")
                # Always print traceback for debugging
                traceback.print_exc()

    # Finalize and return results
    return collector.finalize(test_name, str(test_file), final_state)


def run_all_benchmarks(examples_dir: Path) -> List[BenchmarkResult]:
    """
    Run benchmarks on all test files in examples directory.

    Args:
        examples_dir: Path to examples directory

    Returns:
        List of BenchmarkResult objects
    """
    results = []

    test_files = sorted(examples_dir.glob("*.txt"))

    for test_file in test_files:
        test_name = test_file.stem
        print(f"Running benchmark: {test_name}...")

        try:
            result = run_benchmark_on_file(test_file, test_name)
            results.append(result)
            print(f"  ✓ Completed in {result.total_duration_sec}s")
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    return results
