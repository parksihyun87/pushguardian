"""Secret pattern detection (hard abort rules)."""

import re
from typing import List
from ..report.models import Finding


def detect_secrets(diff_text: str, secret_patterns: List[str]) -> List[Finding]:
    """
    Detect secret patterns in diff text.

    Args:
        diff_text: Git diff output
        secret_patterns: List of regex patterns to detect (from config)

    Returns:
        List of Finding objects for detected secrets
    """
    findings = []

    for pattern in secret_patterns:
        # Create regex pattern (case-sensitive for most secrets)
        try:
            regex = re.compile(pattern)
        except re.error:
            # If pattern is not valid regex, treat as literal string
            regex = re.compile(re.escape(pattern))

        # Search in diff (only in added lines: +)
        for line_num, line in enumerate(diff_text.split("\n"), start=1):
            # Only check added lines
            if not line.startswith("+"):
                continue

            matches = regex.finditer(line)
            for match in matches:
                findings.append(
                    Finding(
                        kind="secret",
                        title=f"Secret pattern detected: {pattern}",
                        detail=f"Line {line_num}: {line[:100]}...",
                        confidence=1.0,
                        severity="critical",
                        fix_now=(
                            "1. Remove the secret from code immediately\n"
                            "2. Rotate/revoke the exposed credential\n"
                            "3. Use environment variables or secret managers"
                        ),
                    )
                )

    return findings
