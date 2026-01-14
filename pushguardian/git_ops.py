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


def fetch_base_branch(repo_root: str, base_branch: str) -> bool:
    """
    Fetch latest changes from base branch.

    Args:
        repo_root: Git repository root
        base_branch: Branch to fetch (e.g., "origin/main")

    Returns:
        True if fetch succeeded, False otherwise
    """
    # Parse origin and branch name
    if "/" in base_branch:
        remote, branch = base_branch.split("/", 1)
    else:
        remote = "origin"
        branch = base_branch

    cmd = ["git", "fetch", remote, branch]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
    )

    return result.returncode == 0


def get_merge_base(repo_root: str, base_branch: str, head_ref: str = "HEAD") -> Optional[str]:
    """
    Get the merge base (common ancestor) between HEAD and base branch.

    Args:
        repo_root: Git repository root
        base_branch: Base branch (e.g., "origin/main")
        head_ref: Current HEAD reference

    Returns:
        Merge base commit SHA, or None if not found
    """
    cmd = ["git", "merge-base", head_ref, base_branch]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
    )

    if result.returncode != 0:
        return None

    return result.stdout.strip()


def get_base_diff(repo_root: str, base_branch: str) -> str:
    """
    Get diff from merge-base to base branch HEAD.
    This shows changes that happened on base branch since we diverged.

    Args:
        repo_root: Git repository root
        base_branch: Base branch (e.g., "origin/main")

    Returns:
        Diff text showing changes on base branch
    """
    # Get merge base
    merge_base = get_merge_base(repo_root, base_branch)
    if not merge_base:
        return ""

    # Get diff from merge-base to base branch HEAD
    cmd = ["git", "diff", merge_base, base_branch]
    result = subprocess.run(
        cmd, capture_output=True, text=True, cwd=repo_root, encoding="utf-8"
    )

    if result.returncode != 0:
        return ""

    return result.stdout


def parse_diff_hunks(diff_text: str) -> dict[str, List[Tuple[int, int]]]:
    """
    Parse diff hunks to extract changed line ranges for each file.

    Args:
        diff_text: Git diff output

    Returns:
        Dictionary: {filepath: [(start_line, end_line), ...]}
    """
    hunks_by_file = {}
    current_file = None

    for line in diff_text.split("\n"):
        # New file
        if line.startswith("diff --git"):
            parts = line.split()
            if len(parts) >= 4:
                current_file = parts[3][2:]  # Remove 'b/' prefix
                hunks_by_file[current_file] = []

        # Hunk header: @@ -10,7 +10,8 @@
        elif line.startswith("@@") and current_file:
            # Extract new file line range: +start,count
            try:
                parts = line.split("@@")[1].strip().split()
                if len(parts) >= 2:
                    new_range = parts[1]  # +10,8
                    if new_range.startswith("+"):
                        range_parts = new_range[1:].split(",")
                        start = int(range_parts[0])
                        count = int(range_parts[1]) if len(range_parts) > 1 else 1
                        end = start + count - 1
                        hunks_by_file[current_file].append((start, end))
            except (ValueError, IndexError):
                continue

    return hunks_by_file


def detect_overlapping_files(my_diff: str, base_diff: str) -> List[str]:
    """
    Detect files that were modified in both my branch and base branch.

    Args:
        my_diff: My branch's diff
        base_diff: Base branch's diff

    Returns:
        List of file paths that were modified in both diffs
    """
    my_files = set(parse_changed_files(my_diff))
    base_files = set(parse_changed_files(base_diff))

    return list(my_files & base_files)


def check_line_overlap(my_hunks: List[Tuple[int, int]], base_hunks: List[Tuple[int, int]]) -> bool:
    """
    Check if any line ranges overlap between two sets of hunks.

    Args:
        my_hunks: My changed line ranges
        base_hunks: Base branch changed line ranges

    Returns:
        True if any overlap found
    """
    for my_start, my_end in my_hunks:
        for base_start, base_end in base_hunks:
            # Check overlap: [my_start, my_end] intersects [base_start, base_end]
            if not (my_end < base_start or my_start > base_end):
                return True

    return False
