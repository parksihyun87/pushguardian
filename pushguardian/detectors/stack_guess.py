"""Stack inference from file extensions and paths."""

from pathlib import Path
from typing import List, Set


STACK_INDICATORS = {
    "react": {
        "extensions": [".jsx", ".tsx"],
        # React 전용 폴더 패턴 위주로 한정하고, 일반적인 "app/" 는 제외하여 파이썬 앱 등에서의 오탐을 줄인다.
        "paths": ["components/", "hooks/", "pages/"],
        "files": ["package.json", "next.config.js", "vite.config.ts"],
    },
    "typescript": {
        "extensions": [".ts", ".tsx"],
        "paths": [],
        "files": ["tsconfig.json"],
    },
    "python": {
        "extensions": [".py"],
        "paths": [],
        "files": ["requirements.txt", "setup.py", "pyproject.toml"],
    },
    "fastapi": {
        "extensions": [".py"],
        "paths": ["api/", "routers/", "endpoints/"],
        "files": [],
    },
    "springboot": {
        "extensions": [".java"],
        "paths": ["src/main/java/", "controller/", "service/", "repository/"],
        "files": ["pom.xml", "build.gradle"],
    },
    "docker": {
        "extensions": [],
        "paths": [],
        "files": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"],
    },
    "kubernetes": {
        "extensions": [],  # Removed generic .yml to avoid false positives with docker-compose
        "paths": ["k8s/", "kubernetes/", "manifests/", ".kube/"],
        "files": ["deployment.yaml", "deployment.yml", "service.yaml", "service.yml",
                  "configmap.yaml", "configmap.yml", "ingress.yaml", "ingress.yml"],
    },
    "nextjs": {
        "extensions": [".tsx", ".ts", ".jsx"],
        # Next.js 프로젝트에서도 "app/" 폴더가 흔하지만, 다른 스택과 충돌을 줄이기 위해
        # pages/public 위주로 감지하고, next.config.* 파일로 보완한다.
        "paths": ["pages/", "public/"],
        "files": ["next.config.js", "next.config.mjs"],
    },
    "git": {
        "extensions": [],
        "paths": [".github/", ".git/"],
        "files": [".gitignore", ".gitattributes"],
    },
}


def guess_stacks(changed_files: List[str]) -> Set[str]:
    """
    Guess which stacks/technologies are touched based on changed files.

    Args:
        changed_files: List of file paths that changed

    Returns:
        Set of stack names (e.g., {'react', 'typescript', 'docker'})
    """
    detected_stacks = set()

    for filepath in changed_files:
        path = Path(filepath)
        ext = path.suffix.lower()
        filename = path.name.lower()

        # Check each stack
        for stack_name, indicators in STACK_INDICATORS.items():
            # Check extension
            if ext in indicators["extensions"]:
                detected_stacks.add(stack_name)
                continue

            # Check path patterns
            for path_pattern in indicators["paths"]:
                if path_pattern.lower() in filepath.lower():
                    detected_stacks.add(stack_name)
                    break

            # Check specific files
            if filename in [f.lower() for f in indicators["files"]]:
                detected_stacks.add(stack_name)

    return detected_stacks


def identify_weak_stacks(
    detected_stacks: Set[str], stacks_known: List[str], stacks_weak: List[str]
) -> List[str]:
    """
    Identify which weak stacks were touched.

    Args:
        detected_stacks: Set of detected stack names
        stacks_known: User's known stacks (from config)
        stacks_weak: User's weak stacks (from config)

    Returns:
        List of weak stack names that were detected
    """
    weak_touched = []

    stacks_weak_lower = [s.lower() for s in stacks_weak]

    for stack in detected_stacks:
        if stack.lower() in stacks_weak_lower:
            weak_touched.append(stack)

    return weak_touched
