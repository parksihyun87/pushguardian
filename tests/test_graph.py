"""Tests for LangGraph workflow."""

import pytest
from pushguardian.graph import run_guardian, run_guardian_stream


def test_run_guardian_basic():
    """Test basic guardian workflow execution."""
    diff_text = """
diff --git a/test.py b/test.py
index abc1234..def5678 100644
--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
+print("hello")
"""

    state = run_guardian(diff_text, mode="web")

    # Basic state checks
    assert state is not None
    assert "decision" in state
    assert "severity" in state
    assert "risk_score" in state
    assert "report_md" in state
    assert state["decision"] in ["allow", "block"]


def test_run_guardian_with_secret():
    """Test guardian blocks secrets."""
    diff_text = """
diff --git a/.env b/.env
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/.env
@@ -0,0 +1,2 @@
+OPENAI_API_KEY=sk-proj-1234567890abcdef
+DATABASE_PASSWORD=supersecret123
"""

    state = run_guardian(diff_text, mode="web")

    # Should detect secrets
    assert len(state["hard_findings"]) > 0
    assert state["decision"] == "block"
    assert state["severity"] in ["critical", "high"]


def test_run_guardian_clean_code():
    """Test guardian allows clean code."""
    diff_text = """
diff --git a/src/utils.py b/src/utils.py
index abc1234..def5678 100644
--- a/src/utils.py
+++ b/src/utils.py
@@ -1,3 +1,6 @@
+def greet(name: str) -> str:
+    return f"Hello, {name}!"
+
"""

    state = run_guardian(diff_text, mode="web")

    # Should allow clean code
    assert state["decision"] == "allow"
    assert len(state["hard_findings"]) == 0


def test_run_guardian_stream():
    """Test guardian streaming execution."""
    diff_text = """
diff --git a/test.py b/test.py
index abc1234..def5678 100644
--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
+print("test")
"""

    nodes_executed = []
    final_state = None

    for node_name, state in run_guardian_stream(diff_text, mode="web"):
        nodes_executed.append(node_name)
        final_state = state

    # Check nodes were executed
    assert len(nodes_executed) > 0
    assert "load_config" in nodes_executed
    assert "hard_policy_check" in nodes_executed
    assert final_state is not None
    assert "decision" in final_state


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
