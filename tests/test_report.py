"""Tests for report generation."""

import pytest
from pushguardian.report.writer import generate_report_md
from pushguardian.report.models import Finding, Evidence


def test_generate_report_basic():
    """Test basic report generation."""
    findings = [
        Finding(
            title="Test Finding",
            kind="security",
            severity="medium",
            confidence=0.8,
            detail="Test detail",
            fix_now="Fix suggestion"
        )
    ]

    evidence = Evidence(
        principle_links=["https://example.com/principle"],
        example_links=["https://example.com/example"],
        notes="Test notes",
        search_queries=["test query"],
        tools_used=["tavily"],
        research_iterations=1,
        llm_observations=[]
    )

    report = generate_report_md(
        findings=findings,
        evidence=evidence,
        severity="medium",
        risk_score=0.5,
        decision="allow",
        override_reason=None,
        history_hint=None,
        weak_stack_touched=[],
        quick_fixes=[]
    )

    # Check report contains expected sections
    assert "PushGuardian" in report
    assert "Test Finding" in report
    assert "medium" in report.lower()
    assert "allow" in report.lower()


def test_generate_report_with_block():
    """Test report generation for blocked commits."""
    findings = [
        Finding(
            title="Critical Security Issue",
            kind="secret",
            severity="critical",
            confidence=1.0,
            detail="API key detected",
            fix_now="Remove the API key"
        )
    ]

    evidence = Evidence(
        principle_links=[],
        example_links=[],
        notes="",
        search_queries=[],
        tools_used=[],
        research_iterations=0,
        llm_observations=[]
    )

    report = generate_report_md(
        findings=findings,
        evidence=evidence,
        severity="critical",
        risk_score=1.0,
        decision="block",
        override_reason=None,
        history_hint=None,
        weak_stack_touched=[],
        quick_fixes=[]
    )

    # Check report indicates blocking
    assert "block" in report.lower()
    assert "critical" in report.lower()
    assert "Critical Security Issue" in report


def test_generate_report_empty_findings():
    """Test report generation with no findings."""
    findings = []

    evidence = Evidence(
        principle_links=[],
        example_links=[],
        notes="",
        search_queries=[],
        tools_used=[],
        research_iterations=0,
        llm_observations=[]
    )

    report = generate_report_md(
        findings=findings,
        evidence=evidence,
        severity="low",
        risk_score=0.0,
        decision="allow",
        override_reason=None,
        history_hint=None,
        weak_stack_touched=[],
        quick_fixes=[]
    )

    # Check report is still valid
    assert "PushGuardian" in report
    assert "allow" in report.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
