"""Tests for LLM judge module."""

import pytest
from pushguardian.llm.judge import run_soft_judge


def test_run_soft_judge_basic():
    """Test basic LLM judge functionality."""
    diff_text = """
diff --git a/src/api.py b/src/api.py
index abc1234..def5678 100644
--- a/src/api.py
+++ b/src/api.py
@@ -1,3 +1,5 @@
+# Added user input handling
+user_data = request.get_json()
"""

    soft_checks = [
        {"name": "xss", "description": "XSS vulnerability"},
        {"name": "sql_injection", "description": "SQL injection risk"}
    ]
    stacks_known = ["python", "fastapi"]
    stacks_weak = []

    # This test may require API keys, so we'll make it lenient
    try:
        result = run_soft_judge(
            diff_text=diff_text,
            soft_checks=soft_checks,
            stacks_known=stacks_known,
            stacks_weak=stacks_weak
        )

        # Basic checks
        assert isinstance(result, dict)
        assert "findings" in result
        assert "risk_score" in result
        assert "severity" in result
        assert isinstance(result["findings"], list)
    except Exception as e:
        # If API keys are not configured, skip
        if "API key" in str(e) or "OPENAI_API_KEY" in str(e) or "Unauthorized" in str(e):
            pytest.skip(f"API keys not configured: {e}")
        else:
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
