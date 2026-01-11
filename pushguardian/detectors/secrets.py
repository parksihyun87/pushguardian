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
                        title=f"시크릿 패턴 감지: {pattern}",
                        detail=f"라인 {line_num}: {line[:100]}...",
                        confidence=1.0,
                        severity="critical",
                        fix_now=(
                            "1. 코드에서 시크릿을 즉시 제거하세요\n"
                            "2. 노출된 자격증명을 교체/폐기하세요\n"
                            "3. 환경 변수나 시크릿 매니저를 사용하세요"
                        ),
                    )
                )

    return findings
