"""Tests for git operations."""

import pytest
from pushguardian.git_ops import parse_changed_files


def test_parse_changed_files():
    """Test parsing changed files from diff."""
    diff_text = """
diff --git a/src/main.py b/src/main.py
index abc1234..def5678 100644
--- a/src/main.py
+++ b/src/main.py
@@ -1,3 +1,4 @@
diff --git a/.env b/.env
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/.env
    """

    files = parse_changed_files(diff_text)

    assert len(files) == 2
    assert "src/main.py" in files
    assert ".env" in files


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
