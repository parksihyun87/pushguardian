"""Tests for detector modules."""

import pytest
from pushguardian.detectors.secrets import detect_secrets
from pushguardian.detectors.files import detect_sensitive_files
from pushguardian.detectors.stack_guess import guess_stacks, identify_weak_stacks


def test_detect_secrets():
    """Test secret pattern detection."""
    diff_text = """
+OPENAI_API_KEY=sk-proj-1234567890
+PASSWORD=test123
+AKIA_AWS_KEY=AKIAIOSFODNN7EXAMPLE
    """

    patterns = ["sk-", "AKIA"]
    findings = detect_secrets(diff_text, patterns)

    assert len(findings) >= 2
    assert any("sk-" in f.title for f in findings)
    assert all(f.kind == "secret" for f in findings)
    assert all(f.severity == "critical" for f in findings)


def test_detect_sensitive_files():
    """Test sensitive file pattern detection."""
    changed_files = [".env", "config/database.yml", "keys/id_rsa", "src/main.py"]

    patterns = [".env", "*.pem", "id_rsa"]
    findings = detect_sensitive_files(changed_files, patterns)

    assert len(findings) >= 2  # .env and id_rsa
    assert any(".env" in f.detail for f in findings)
    assert all(f.kind == "file" for f in findings)


def test_guess_stacks():
    """Test stack guessing from file paths."""
    files = [
        "src/components/Button.tsx",
        "backend/api/routes.py",
        "Dockerfile",
        "k8s/deployment.yaml",
    ]

    stacks = guess_stacks(files)

    assert "typescript" in stacks or "react" in stacks
    assert "python" in stacks
    assert "docker" in stacks
    assert "kubernetes" in stacks


def test_identify_weak_stacks():
    """Test weak stack identification."""
    detected = {"react", "python", "docker"}
    known = ["python", "fastapi"]
    weak = ["react", "typescript", "kubernetes"]

    weak_touched = identify_weak_stacks(detected, known, weak)

    assert "react" in weak_touched
    assert "python" not in weak_touched  # Known stack
    assert "kubernetes" not in weak_touched  # Not detected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
