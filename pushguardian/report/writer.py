"""Markdown report generation and persistence."""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from .models import Finding, Evidence


def generate_report_md(
    findings: List[Finding],
    evidence: Evidence,
    severity: str,
    risk_score: float,
    decision: str,
    override_reason: str | None = None,
    history_hint: Dict[str, Any] | None = None,
    weak_stack_touched: List[str] | None = None,
    quick_fixes: List[str] | None = None,
    learning_points: List[Dict[str, Any]] | None = None,
) -> str:
    """
    Generate a markdown report.

    Args:
        findings: List of findings
        evidence: Research evidence
        severity: Overall severity
        risk_score: Overall risk score (0-1)
        decision: allow/block/override
        override_reason: Reason for override (if applicable)
        history_hint: History scan results
        weak_stack_touched: Weak stacks that were touched
        quick_fixes: Quick fix suggestions

    Returns:
        Markdown report as string
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 결정 한글 변환
    decision_ko = {
        "allow": "허용",
        "block": "차단",
        "override": "오버라이드"
    }.get(decision.lower(), decision.upper())

    # 심각도 한글 변환
    severity_ko = {
        "low": "낮음",
        "medium": "중간",
        "high": "높음",
        "critical": "심각"
    }.get(severity.lower(), severity.upper())

    md_lines = [
        "# 🛡️ PushGuardian 리포트\n",
        f"**생성 시각:** {timestamp}\n",
        f"**결정:** `{decision_ko}`\n",
        f"**심각도:** `{severity_ko}`\n",
        f"**위험 점수:** {risk_score:.2f}/1.00\n",
        "",
    ]

    # Override reason
    if override_reason:
        md_lines.extend(
            [
                "## ⚠️ 오버라이드 적용됨\n",
                f"{override_reason}\n",
                "",
            ]
        )

    # Findings summary
    if findings:
        md_lines.append("## 🔍 발견된 이슈\n")
        for i, finding in enumerate(findings, 1):
            # 개별 finding 심각도도 한글로 변환
            finding_severity_ko = {
                "low": "낮음",
                "medium": "중간",
                "high": "높음",
                "critical": "심각"
            }.get(finding.severity.lower(), finding.severity.upper())

            md_lines.extend(
                [
                    f"### {i}. [{finding_severity_ko}] {finding.title}\n",
                    f"**유형:** `{finding.kind}`  ",
                    f"**신뢰도:** {finding.confidence:.0%}\n",
                    f"{finding.detail}\n",
                    f"**즉시 조치 가이드:**\n```\n{finding.fix_now}\n```\n",
                    "",
                ]
            )
    else:
        md_lines.append("## ✅ 치명적인 보안 이슈가 없습니다.\n\n")

    # Quick fixes
    if quick_fixes:
        md_lines.append("## 🔧 즉시 조치 항목\n")
        for fix in quick_fixes:
            md_lines.append(f"- {fix}")
        md_lines.append("\n")

    # Security Evidence (only if there are findings)
    if findings and (evidence.principle_link_infos or evidence.principle_links):
        md_lines.append("## 🔒 보안 참고 자료\n")
        md_lines.append("발견된 보안 이슈와 관련된 참고 자료 링크입니다:\n\n")

        # 영문 자료와 한글 자료 분리
        english_links = []
        korean_links = []

        if evidence.principle_link_infos:
            for info in evidence.principle_link_infos:
                source = info.get("source", "")
                if source == "naver_ko":
                    korean_links.append(info)
                else:
                    english_links.append(info)

        # 영문 자료 먼저 표시 (최대 4개)
        if english_links:
            for info in english_links[:4]:
                tokens = []
                role = info.get("role")
                source = info.get("source")
                if role == "principle":
                    tokens.append("원리")
                if source in ["owasp", "nist", "github", "stackoverflow", "trusted"]:
                    tokens.append(source.upper())
                elif source == "blog":
                    tokens.append("블로그")

                token_str = f"[{', '.join(tokens)}] " if tokens else ""
                summary = (info.get("summary_ko") or info.get("summary", "")).strip()
                url = info.get("url", "")
                md_lines.append(f"- {token_str}{summary}\n  {url}\n")
        elif not korean_links:
            # 메타정보가 없으면 기존 URL 리스트 사용
            for link in evidence.principle_links[:4]:
                md_lines.append(f"- {link}\n")

        # 한글 자료 섹션 (네이버 검색 결과)
        if korean_links:
            md_lines.append("\n### 📚 한글 자료 (LLM 선별)\n")
            md_lines.append("*네이버 검색 결과 중 AI가 선별한 고품질 한글 자료입니다.*\n\n")
            for info in korean_links[:3]:  # 최대 3개
                summary = (info.get("summary_ko") or info.get("summary", "")).strip()
                url = info.get("url", "")
                md_lines.append(f"- [한글] {summary}\n  {url}\n")

        md_lines.append("\n")

    # Learning Section (only for weak stacks)
    if weak_stack_touched and learning_points:
        md_lines.append("---\n\n")
        md_lines.extend(
            [
                "## 📖 학습: 약점 스택 감지됨\n",
                f"⚠️ 이번 변경사항은 사용자가 상대적으로 약점으로 표시한 스택 **{', '.join(weak_stack_touched)}** 와(과) 관련되어 있습니다.\n\n",
                "### 🎯 현재 코드에 등장하는 핵심 개념들\n",
            ]
        )

        for lp in learning_points:
            # Learning points always use 🟡 to distinguish from security findings
            md_lines.extend(
                [
                    f"🟡 **{lp.get('concept', '알 수 없음')}**\n",
                    f"   {lp.get('detail', '상세 설명이 제공되지 않았습니다.')}\n\n",
                ]
            )

        # Learning resources (tutorials only)
        if evidence.example_link_infos or evidence.example_links:
            md_lines.append("### 💡 튜토리얼 & 예제\n")

            # 영문 자료와 한글 자료 분리
            english_examples = []
            korean_examples = []

            if evidence.example_link_infos:
                for info in evidence.example_link_infos:
                    source = info.get("source", "")
                    if source == "naver_ko":
                        korean_examples.append(info)
                    else:
                        english_examples.append(info)

            # 영문 예제 먼저 표시 (최대 5개)
            if english_examples:
                for info in english_examples[:5]:
                    tokens = []
                    role = info.get("role")
                    source = info.get("source")
                    if role == "example":
                        tokens.append("예제")
                    if source in ["github", "stackoverflow", "trusted"]:
                        tokens.append(source.upper())
                    elif source == "blog":
                        tokens.append("블로그")

                    token_str = f"[{', '.join(tokens)}] " if tokens else ""
                    summary = (info.get("summary_ko") or info.get("summary", "")).strip()
                    url = info.get("url", "")
                    md_lines.append(f"- {token_str}{summary}\n  {url}\n")
            elif not korean_examples:
                # 메타정보가 없으면 기존 URL 리스트 사용
                for link in evidence.example_links[:5]:
                    md_lines.append(f"- {link}\n")

            # 한글 예제 섹션
            if korean_examples:
                md_lines.append("\n**한글 튜토리얼 (LLM 선별):**\n\n")
                for info in korean_examples[:3]:
                    summary = (info.get("summary_ko") or info.get("summary", "")).strip()
                    url = info.get("url", "")
                    md_lines.append(f"- [한글] {summary}\n  {url}\n")

            md_lines.append("\n")

    # History hint
    if history_hint:
        md_lines.append("## 📅 히스토리 스캔 결과\n")
        if history_hint.get("first_seen_commit"):
            md_lines.append(f"최초로 감지된 커밋: `{history_hint['first_seen_commit']}`\n")
        # message 내용 자체는 LLM/로직에서 생성되므로 그대로 사용 (프롬프트를 한국어화하면 이 부분도 자연스럽게 한글로 생성됨)
        md_lines.append(f"{history_hint.get('message', '히스토리 정보가 없습니다.')}\n\n")

    # Footer
    md_lines.extend(
        [
            "---\n",
            "*[PushGuardian](https://github.com/parksihyun87/pushguardian) 에 의해 생성됨*\n",
        ]
    )

    return "".join(md_lines)


def save_report(
    report_md: str,
    report_dir: str,
    prefix: str = "report",
) -> str:
    """
    Save report to markdown file.

    Args:
        report_md: Markdown content
        report_dir: Directory to save report
        prefix: Filename prefix

    Returns:
        Path to saved report
    """
    # Create directory if needed
    report_path = Path(report_dir)
    report_path.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.md"
    filepath = report_path / filename

    # Write file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_md)

    return str(filepath)
