"""Git operations: diff extraction, file parsing, history scanning."""

import subprocess
from pathlib import Path
from typing import List, Tuple, Optional


def get_diff_range(local_ref: str, remote_ref: str, repo_root: Optional[str] = None) -> str:
    """
    Get git diff for the push range.

    Args:
        local_ref: Local commit SHA (e.g., HEAD)
        remote_ref: Remote commit SHA (or all zeros for new branch)
        repo_root: Git repository root (defaults to cwd)

    Returns:
        Diff text as string
    """
    if repo_root:
        cwd = repo_root
    else:
        cwd = None

    # Check if remote_ref is new branch (all zeros) or doesn't exist
    # Git's empty tree SHA - represents "no content"
    EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

    if remote_ref == "0" * 40 or not remote_ref or remote_ref == "0":
        # New branch: diff against empty tree to get all changes
        cmd = ["git", "diff", EMPTY_TREE, local_ref]
    else:
        # Existing branch: normal diff
        cmd = ["git", "diff", f"{remote_ref}..{local_ref}"]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, encoding="utf-8")

    if result.returncode != 0:
        raise RuntimeError(f"Git diff failed: {result.stderr}")

    return result.stdout


def parse_changed_files(diff_text: str) -> List[str]:
    """
    Extract changed file paths from git diff output.

    Args:
        diff_text: Git diff output

    Returns:
        List of changed file paths
    """
    files = []

    for line in diff_text.split("\n"):
        # Look for diff --git a/path b/path
        if line.startswith("diff --git"):
            parts = line.split()
            if len(parts) >= 4:
                # Extract b/path (new version)
                filepath = parts[3][2:]  # Remove 'b/' prefix
                files.append(filepath)

    return files


def scan_history_for_first_appearance(
    repo_root: str, added_lines: List[str], max_commits: int = 5
) -> Optional[str]:
    """
    Scan recent commit history to find when a line was first added.

    Args:
        repo_root: Git repository root
        added_lines: List of added line content to search for
        max_commits: Number of recent commits to scan

    Returns:
        Commit SHA where line first appeared, or None
    """
    if not added_lines:
        return None

    # Get recent commit SHAs
    cmd = ["git", "log", f"-{max_commits}", "--format=%H"]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
    )

    if result.returncode != 0:
        return None

    commits = result.stdout.strip().split("\n")

    # Search each commit for the added lines
    for commit_sha in reversed(commits):  # Oldest first
        cmd = ["git", "show", commit_sha]
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
        )

        if result.returncode != 0:
            continue

        commit_diff = result.stdout

        # Check if any of the added lines appear in this commit
        for line in added_lines:
            if line.strip() and line.strip() in commit_diff:
                return commit_sha

    return None


def get_repo_root() -> str:
    """
    Get the root directory of the current git repository.

    Returns:
        Absolute path to repo root

    Raises:
        RuntimeError: If not in a git repository
    """
    cmd = ["git", "rev-parse", "--show-toplevel"]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

    if result.returncode != 0:
        raise RuntimeError("Not in a git repository")

    return result.stdout.strip()
