"""Tests for RepoContext (Git repository operations)."""

import pytest
from pathlib import Path
from pushguardian.repo_context import RepoContext


def test_repo_context_initialization():
    """Test RepoContext can be initialized with current directory."""
    repo = RepoContext(".")
    assert repo.root.exists()


def test_ahead_count_no_remote():
    """Test ahead_count when remote branch doesn't exist."""
    # This test assumes it's run in a git repo
    try:
        repo = RepoContext(".")
        # If origin/main doesn't exist, should fallback to counting all commits
        ahead = repo.ahead_count(base_ref="origin/nonexistent-branch", head_ref="HEAD")
        assert ahead >= 0  # Should not crash, returns 0 or total commits
    except RuntimeError:
        # Expected if not in a git repo
        pass


def test_diff_last_n_commits_zero():
    """Test diff_last_n_commits with n=0."""
    repo = RepoContext(".")
    diff = repo.diff_last_n_commits(0)
    assert diff == ""


def test_diff_last_n_commits_negative():
    """Test diff_last_n_commits with negative n."""
    repo = RepoContext(".")
    diff = repo.diff_last_n_commits(-1)
    assert diff == ""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
