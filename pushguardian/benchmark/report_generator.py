"""Markdown report generator for benchmark results."""

from typing import List
from .metrics import BenchmarkResult, NodeMetrics, SearchQualityMetrics
from datetime import datetime


def generate_markdown_report(results: List[BenchmarkResult]) -> str:
    """
    Generate comprehensive markdown report from benchmark results.

    Args:
        results: List of benchmark results

    Returns:
        Markdown formatted report
    """

    lines = []

    # Header
    lines.append("# 🔍 PushGuardian Performance Benchmark Report")
    lines.append("")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Total Test Cases:** {len(results)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary Statistics
    lines.append("## 📊 Overall Summary")
    lines.append("")

    if results:
        avg_duration = sum(r.total_duration_sec for r in results) / len(results)
        avg_search_time = sum(r.total_search_time_ms for r in results) / len(results)
        avg_llm_calls = sum(r.llm_calls_count for r in results) / len(results)
        avg_query_length = sum(r.avg_query_length for r in results) / len(results)

        total_searches = sum(len(r.search_quality) for r in results)
        avg_principle_links = sum(r.principle_links_count for r in results) / len(results)
        avg_example_links = sum(r.example_links_count for r in results) / len(results)

        lines.append(f"- **Average Total Duration:** {avg_duration:.2f}s")
        lines.append(f"- **Average Search Time:** {avg_search_time:.2f}ms")
        lines.append(f"- **Average LLM Calls:** {avg_llm_calls:.1f} per test")
        lines.append(f"- **Average Query Length:** {avg_query_length:.1f} words")
        lines.append(f"- **Total Searches Performed:** {total_searches}")
        lines.append(f"- **Average Principle Links:** {avg_principle_links:.1f}")
        lines.append(f"- **Average Example Links:** {avg_example_links:.1f}")
        lines.append("")

        # Decision breakdown
        decisions = {}
        severities = {}
        for r in results:
            decisions[r.decision] = decisions.get(r.decision, 0) + 1
            severities[r.severity] = severities.get(r.severity, 0) + 1

        lines.append("### Decision Distribution")
        lines.append("")
        for decision, count in sorted(decisions.items()):
            lines.append(f"- **{decision.upper()}:** {count} cases")
        lines.append("")

        lines.append("### Severity Distribution")
        lines.append("")
        for severity, count in sorted(severities.items()):
            lines.append(f"- **{severity.upper()}:** {count} cases")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Detailed Test Case Results
    lines.append("## 📋 Detailed Test Case Results")
    lines.append("")

    for i, result in enumerate(results, 1):
        lines.append(f"### {i}. Test: `{result.test_name}`")
        lines.append("")
        lines.append(f"**File:** `{result.test_file}`")
        lines.append(f"**Timestamp:** {result.timestamp}")
        lines.append("")

        # Key metrics table
        lines.append("#### ⏱️ Performance Metrics")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| **Total Duration** | {result.total_duration_ms:.2f}ms ({result.total_duration_sec:.2f}s) |")
        lines.append(f"| **Search Time** | {result.total_search_time_ms:.2f}ms |")
        lines.append(f"| **LLM Calls** | {result.llm_calls_count} |")
        lines.append(f"| **Research Iterations** | {result.research_iterations} |")
        lines.append("")

        # Results summary
        lines.append("#### 🎯 Results Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| **Decision** | `{result.decision}` |")
        lines.append(f"| **Severity** | `{result.severity}` |")
        lines.append(f"| **Findings** | {result.findings_count} |")
        lines.append(f"| **Principle Links** | {result.principle_links_count} |")
        lines.append(f"| **Example Links** | {result.example_links_count} |")
        lines.append(f"| **Tools Used** | {', '.join(result.tools_used) if result.tools_used else 'None'} |")
        lines.append("")

        # Node-by-node breakdown
        if result.node_metrics:
            lines.append("#### 🔄 Node Execution Timeline")
            lines.append("")
            lines.append("| Node | Duration (ms) | Details |")
            lines.append("|------|---------------|---------|")

            for node in result.node_metrics:
                details = []
                if node.findings_detected:
                    details.append(f"{node.findings_detected} findings")
                if node.search_engine:
                    details.append(f"Engine: {node.search_engine}")
                if node.results_count:
                    details.append(f"{node.results_count} results")
                if node.llm_called:
                    details.append(f"LLM: {node.llm_model or 'unknown'}")

                details_str = ", ".join(details) if details else "-"
                lines.append(f"| `{node.node_name}` | {node.duration_ms:.2f} | {details_str} |")

            lines.append("")

        # Search quality breakdown
        if result.search_quality:
            lines.append("#### 🔍 Search Quality Analysis")
            lines.append("")

            for j, search in enumerate(result.search_quality, 1):
                lines.append(f"**Search #{j} ({search.search_engine}, Iteration {search.iteration})**")
                lines.append("")
                lines.append(f"- **Query:** `{search.query_text}`")
                lines.append(f"- **Query Length:** {search.query_length} words")
                lines.append(f"- **Latency:** {search.search_latency_ms:.2f}ms")
                lines.append(f"- **Total Results:** {search.total_results}")
                lines.append(f"- **Spam Filtered:** {search.spam_filtered}")
                lines.append(f"- **High-Quality Domains:** {search.high_quality_domains_count} ({search.trusted_domain_ratio*100:.0f}%)")
                lines.append(f"- **Principle Links:** {len(search.principle_links)}")
                lines.append(f"- **Example Links:** {len(search.example_links)}")

                if search.llm_reasoning:
                    lines.append(f"- **LLM Assessment:** {'✓ Sufficient' if search.llm_sufficient else '✗ Needs refinement'}")
                    lines.append(f"  - *Reasoning:* {search.llm_reasoning[:150]}...")

                lines.append("")

                # Show actual links (top 3 each)
                if search.principle_links:
                    lines.append("  **Top Principle Links:**")
                    for link in search.principle_links[:3]:
                        lines.append(f"  - {link}")
                    lines.append("")

                if search.example_links:
                    lines.append("  **Top Example Links:**")
                    for link in search.example_links[:3]:
                        lines.append(f"  - {link}")
                    lines.append("")

        # Errors
        if result.errors:
            lines.append("#### ⚠️ Errors")
            lines.append("")
            for error in result.errors:
                lines.append(f"- {error}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Comparative Analysis
    lines.append("## 📈 Comparative Analysis")
    lines.append("")

    if len(results) > 1:
        lines.append("### Search Performance Comparison")
        lines.append("")
        lines.append("| Test Case | Total Time (s) | Search Time (ms) | Queries | Query Avg Length | Links Found |")
        lines.append("|-----------|----------------|------------------|---------|------------------|-------------|")

        for result in results:
            total_links = result.principle_links_count + result.example_links_count
            query_count = len(result.search_quality)

            lines.append(
                f"| `{result.test_name}` | {result.total_duration_sec:.2f} | "
                f"{result.total_search_time_ms:.0f} | {query_count} | "
                f"{result.avg_query_length:.1f} | {total_links} |"
            )

        lines.append("")

        lines.append("### Search Engine Usage")
        lines.append("")

        # Count search engine usage
        engine_usage = {}
        for result in results:
            for tool in result.tools_used:
                engine_usage[tool] = engine_usage.get(tool, 0) + 1

        if engine_usage:
            for engine, count in sorted(engine_usage.items()):
                lines.append(f"- **{engine.upper()}:** Used in {count} test(s)")
        else:
            lines.append("- No search engines used")

        lines.append("")

    # Recommendations
    lines.append("---")
    lines.append("")
    lines.append("## 💡 Performance Optimization Opportunities")
    lines.append("")

    if results:
        # Find slowest components
        all_nodes = []
        for result in results:
            all_nodes.extend(result.node_metrics)

        if all_nodes:
            # Group by node name
            node_times = {}
            for node in all_nodes:
                if node.node_name not in node_times:
                    node_times[node.node_name] = []
                node_times[node.node_name].append(node.duration_ms)

            # Calculate averages
            node_averages = {
                name: sum(times) / len(times)
                for name, times in node_times.items()
            }

            # Find top 3 slowest nodes
            slowest = sorted(node_averages.items(), key=lambda x: x[1], reverse=True)[:3]

            lines.append("### 🐌 Slowest Components (Avg Duration)")
            lines.append("")
            for i, (node_name, avg_time) in enumerate(slowest, 1):
                lines.append(f"{i}. **`{node_name}`** - {avg_time:.2f}ms")
            lines.append("")

        # Query length analysis
        long_queries = [
            (r.test_name, s.query_text, s.query_length)
            for r in results
            for s in r.search_quality
            if s.query_length > 10
        ]

        if long_queries:
            lines.append("### 📝 Query Length Optimization Candidates")
            lines.append("")
            lines.append("*Queries with 10+ words (may benefit from keyword extraction):*")
            lines.append("")
            for test_name, query, length in sorted(long_queries, key=lambda x: x[2], reverse=True)[:5]:
                lines.append(f"- **{test_name}** ({length} words)")
                lines.append(f"  - `{query}`")
            lines.append("")

        # Search quality insights
        low_quality = [
            (r.test_name, s.search_engine, s.trusted_domain_ratio)
            for r in results
            for s in r.search_quality
            if s.trusted_domain_ratio < 0.5 and s.total_results > 0
        ]

        if low_quality:
            lines.append("### 🎯 Search Quality Improvements Needed")
            lines.append("")
            lines.append("*Searches with <50% high-quality domains:*")
            lines.append("")
            for test_name, engine, ratio in low_quality:
                lines.append(f"- **{test_name}** ({engine}): {ratio*100:.0f}% trusted domains")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 📌 Next Steps")
    lines.append("")
    lines.append("### Recommended Improvements:")
    lines.append("")
    lines.append("1. **Query Optimization**")
    lines.append("   - Implement keyword extraction (TF-IDF or LLM-based)")
    lines.append("   - Reduce query length by 30-50% while maintaining relevance")
    lines.append("   - Target: Average query length < 8 words")
    lines.append("")
    lines.append("2. **Search Quality Enhancement**")
    lines.append("   - Add `site:` operator for trusted domains (OWASP, NIST, GitHub)")
    lines.append("   - Implement domain whitelisting in query construction")
    lines.append("   - Target: >70% results from high-quality sources")
    lines.append("")
    lines.append("3. **Latency Reduction**")
    lines.append("   - Consider parallel search execution for independent queries")
    lines.append("   - Implement caching for common security topics")
    lines.append("   - Target: Reduce search time by 20-30%")
    lines.append("")
    lines.append("4. **Search Engine Selection**")
    lines.append("   - Analyze Tavily vs Serper quality differences")
    lines.append("   - Consider direct fallback strategy based on query type")
    lines.append("   - Optimize retry logic based on LLM confidence")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Report generated by PushGuardian Benchmark Suite*")

    return "\n".join(lines)


def save_report(report: str, output_path: str):
    """
    Save markdown report to file.

    Args:
        report: Markdown report content
        output_path: Path to save the report
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
