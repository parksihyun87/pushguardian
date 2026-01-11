"""Git 레포지토리 래퍼: 미푸시 커밋 개수 및 diff 범위 계산 도우미."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


class RepoContext:
    """Git 레포지토리 컨텍스트 헬퍼.

    - 특정 루트 경로 기준으로 git 명령을 실행
    - origin/main 대비 앞서 있는 커밋 개수 계산
    - 마지막 N개 커밋에 대한 diff 범위 추출
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def _run_git(self, args: list[str]) -> str:
        """해당 레포 루트 기준으로 git 명령을 실행하고 stdout을 반환."""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "git 명령 실행 실패")
        return result.stdout.strip()

    def ahead_count(self, base_ref: str = "origin/main", head_ref: str = "HEAD") -> int:
        """base_ref..head_ref 범위에서 head가 base보다 몇 커밋 앞서는지 계산.

        base_ref가 존재하지 않으면 (원격 브랜치가 없는 경우) 전체 커밋 수를 반환.
        """
        try:
            # 먼저 base_ref가 존재하는지 확인
            self._run_git(["rev-parse", "--verify", base_ref])
            # 존재하면 정상적으로 범위 계산
            out = self._run_git(["rev-list", "--count", f"{base_ref}..{head_ref}"])
            return int(out or "0")
        except RuntimeError:
            # base_ref가 없으면 전체 커밋 수 반환 (초기 저장소)
            try:
                out = self._run_git(["rev-list", "--count", head_ref])
                return int(out or "0")
            except (RuntimeError, ValueError):
                return 0

    def diff_range(self, base_ref: str, head_ref: str = "HEAD") -> str:
        """특정 ref 범위의 git diff를 반환."""
        return self._run_git(["git", "diff", f"{base_ref}..{head_ref}"])

    def diff_last_n_commits(self, n: int, head_ref: str = "HEAD") -> str:
        """마지막 N개 커밋에 대한 diff (HEAD~N..HEAD)를 반환. n<=0이면 빈 문자열.

        전체 커밋 수가 N보다 적으면, 첫 커밋부터의 diff를 반환.
        """
        if n <= 0:
            return ""

        try:
            # 전체 커밋 수 확인
            total_commits = int(self._run_git(["rev-list", "--count", head_ref]))

            if total_commits == 0:
                return ""
            elif total_commits <= n:
                # 전체 커밋 수가 N 이하면, 첫 커밋부터의 diff (빈 트리 대비)
                return self._run_git(["diff", "4b825dc642cb6eb9a060e54bf8d69288fbee4904", head_ref])
            else:
                # 정상 케이스: HEAD~N..HEAD
                base = f"{head_ref}~{n}"
                return self._run_git(["diff", f"{base}..{head_ref}"])

        except (RuntimeError, ValueError):
            return ""


