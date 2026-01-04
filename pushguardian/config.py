"""Configuration loader with environment variable expansion."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict
from dotenv import load_dotenv

# Load .env file
load_dotenv()


def expand_env_vars(value: Any) -> Any:
    """Recursively expand environment variables in config values."""
    if isinstance(value, str):
        # Expand %USERPROFILE% and other env vars
        return os.path.expandvars(value)
    elif isinstance(value, dict):
        return {k: expand_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [expand_env_vars(item) for item in value]
    return value


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """
    Load YAML config with environment variable expansion.

    Args:
        config_path: Path to config.yaml. If None, searches for .pushguardian/config.yaml

    Returns:
        Configuration dictionary with expanded env vars (or defaults if not found)
    """
    # Default configuration
    default_config = {
        "version": 1,
        "report_dir": os.path.expandvars("%USERPROFILE%\\Documents\\PushGuardian\\reports"),
        "override_dir": os.path.expandvars("%USERPROFILE%\\Documents\\PushGuardian\\overrides"),
        "history_scan_commits": 5,
        "stacks_known": ["python", "git"],
        "stacks_weak": ["react", "typescript", "docker", "kubernetes"],
        "hard_abort": {
            "file_patterns": [".env", ".env.*", "*.pem", "*.key", "id_rsa", "id_rsa.*"],
            "secret_patterns": ["sk-", "AKIA", "BEGIN PRIVATE KEY", "BEGIN RSA PRIVATE KEY"],
        },
        "soft_checks": [
            {"name": "dto_schema_bypass", "description": "DTO/Schema bypass detection"},
            {"name": "dependency_risk", "description": "Dependency version changes"},
            {"name": "permission_risk", "description": "Permission file changes"},
        ],
        "research": {
            "max_loops": 2,
            "require_categories": ["principle", "example"],
        },
        "ui": {"show_markdown_in_terminal": True},
    }

    if config_path is None:
        # Try to find .pushguardian/config.yaml in current or parent dirs
        current = Path.cwd()
        for parent in [current] + list(current.parents):
            candidate = parent / ".pushguardian" / "config.yaml"
            if candidate.exists():
                config_path = candidate
                break

        if config_path is None:
            # No config found, use defaults
            return default_config

    config_path = Path(config_path)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Expand all environment variables
        config = expand_env_vars(config)

        return config
    except Exception:
        # If config file is invalid, return defaults
        return default_config


def load_api_keys(api_dir: str = r"C:\workplace\document\API") -> Dict[str, str]:
    """
    Load API keys from text files in the specified directory.

    Expected files:
        - openai.txt
        - tavily.txt
        - serper.txt (optional)
        - langsmith.txt (optional)

    Returns:
        Dictionary with API keys
    """
    api_dir = Path(api_dir)
    keys = {}

    # OpenAI (required)
    openai_file = api_dir / "openai.txt"
    if openai_file.exists():
        keys["OPENAI_API_KEY"] = openai_file.read_text(encoding="utf-8").strip()

    # Tavily (required)
    tavily_file = api_dir / "tavily.txt"
    if tavily_file.exists():
        keys["TAVILY_API_KEY"] = tavily_file.read_text(encoding="utf-8").strip()

    # Serper (optional)
    serper_file = api_dir / "serper.txt"
    if serper_file.exists():
        keys["SERPER_API_KEY"] = serper_file.read_text(encoding="utf-8").strip()

    # LangSmith (optional)
    langsmith_file = api_dir / "langsmith.txt"
    if langsmith_file.exists():
        keys["LANGSMITH_API_KEY"] = langsmith_file.read_text(encoding="utf-8").strip()

    # Set as environment variables
    for key, value in keys.items():
        os.environ[key] = value

    return keys


# Auto-load API keys when module is imported
# Priority: 1) .env file, 2) API directory
try:
    # Check if .env has keys loaded already
    if not os.getenv("OPENAI_API_KEY"):
        # If not in .env, try loading from API directory
        load_api_keys()
except Exception:
    # Silently fail if API directory doesn't exist (e.g., in CI/CD)
    pass
