"""File pattern detection (hard abort rules)."""

import re
from pathlib import Path
from typing import List
from ..report.models import Finding


def detect_sensitive_files(changed_files: List[str], file_patterns: List[str]) -> List[Finding]:
    """
    Detect sensitive file patterns in changed files.

    Args:
        changed_files: List of file paths that changed
        file_patterns: List of glob-style patterns to detect (from config)

    Returns:
        List of Finding objects for detected sensitive files
    """
    findings = []

    for filepath in changed_files:
        path = Path(filepath)

        for pattern in file_patterns:
            # Convert glob pattern to regex
            # Simple conversion: * -> .*, ? -> .
            regex_pattern = pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".")
            regex_pattern = f"^{regex_pattern}$"

            try:
                regex = re.compile(regex_pattern, re.IGNORECASE)
            except re.error:
                # Fallback to simple string matching
                if pattern.lower() in filepath.lower():
                    regex = None
                    match = True
                else:
                    continue
            else:
                match = regex.match(path.name) or regex.match(filepath)

            if match:
                findings.append(
                    Finding(
                        kind="file",
                        title=f"Sensitive file detected: {pattern}",
                        detail=f"File: {filepath}",
                        confidence=1.0,
                        severity="critical",
                        fix_now=(
                            "1. Remove the sensitive file from git tracking\n"
                            "2. Add to .gitignore to prevent future commits\n"
                            "3. Use git filter-branch or BFG Repo-Cleaner if already pushed"
                        ),
                    )
                )
                break  # One finding per file is enough

    return findings
