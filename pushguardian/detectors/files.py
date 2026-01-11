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
                        title=f"민감한 파일 감지: {pattern}",
                        detail=f"파일: {filepath}",
                        confidence=1.0,
                        severity="critical",
                        fix_now=(
                            "1. git 추적에서 민감한 파일을 제거하세요\n"
                            "2. .gitignore에 추가하여 향후 커밋을 방지하세요\n"
                            "3. 이미 푸시했다면 git filter-branch나 BFG Repo-Cleaner를 사용하세요"
                        ),
                    )
                )
                break  # One finding per file is enough

    return findings
