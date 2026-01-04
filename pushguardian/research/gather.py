"""Research gathering and categorization."""

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

        # Build smarter query based on finding type
        if top_finding.kind == "secret":
            query = "prevent secrets in git commits API keys environment variables best practices"
        elif top_finding.kind == "file":
            query = "gitignore sensitive files credentials environment configuration security"
        elif top_finding.kind == "dto":
            query = "DTO schema validation backend API security best practices"
        elif top_finding.kind == "dependency":
            query = "dependency management security vulnerabilities package updates"
        elif top_finding.kind == "permission":
            query = "file permissions security access control configuration"
        else:
            # Fallback to generic
            query = f"{top_finding.kind} security best practices code review"

        queries.append(("finding", query))
        evidence.search_queries.append(query)

    # Query for weak stack learning
    if weak_stack_touched:
        stack = weak_stack_touched[0]  # Take first weak stack

        # If we have specific learning points from LLM, use them for targeted search
        if learning_points:
            for lp in learning_points[:2]:  # Top 2 learning points
                concept = lp.get("concept", "")
                if concept:
                    query = f"{stack} {concept} tutorial examples"
                    queries.append(("learning", query))
                    evidence.search_queries.append(query)
        else:
            # Fallback to generic learning query
            query = f"{stack} beginner tutorial best practices examples"
            queries.append(("learning", query))
            evidence.search_queries.append(query)

    # Execute searches
    for query_type, query in queries:
        if search_engine == "tavily":
            results = search_tavily(query, max_results=5)
        elif search_engine == "serper":
            results = search_serper(query, max_results=5)
        elif search_engine == "duckduckgo":
            results = search_duckduckgo(query, max_results=5)
        else:
            results = []

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
                "/ko/",  # Korean language promotional pages
                "/kr/",
                "youtube.com",  # Video content (not practical for quick reference)
                "pinterest.com",
                "instagram.com",
            ]

            if any(spam in url.lower() for spam in spam_domains):
                continue

            # Categorize first
            category = categorize_link(
                result.get("url", ""), result.get("title", ""), result.get("content", "")
            )

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

            # Prioritize high-quality sources
            if category == "principle":
                if is_high_quality_principle:
                    # Insert at beginning for high quality
                    if url not in evidence.principle_links and len(evidence.principle_links) < 4:
                        evidence.principle_links.insert(0, url)
                elif len(evidence.principle_links) < 4 and url not in evidence.principle_links:
                    evidence.principle_links.append(url)
            else:  # example
                if is_high_quality_example:
                    # Insert at beginning for high quality
                    if url not in evidence.example_links and len(evidence.example_links) < 3:
                        evidence.example_links.insert(0, url)
                elif len(evidence.example_links) < 3 and url not in evidence.example_links:
                    evidence.example_links.append(url)

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
    merged.notes = (old.notes + " | " + new.notes) if old.notes and new.notes else (old.notes or new.notes)

    # Merge debug info
    merged.research_iterations = old.research_iterations + new.research_iterations
    merged.tools_used = list(set(old.tools_used + new.tools_used))
    merged.llm_observations = old.llm_observations + new.llm_observations
    merged.search_queries = old.search_queries + new.search_queries

    return merged
