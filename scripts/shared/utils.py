"""Shared utilities used across scripts."""

import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from rich.console import Console

console = Console()


def load_env(env_file: Path | None = None) -> None:
    """Load .env file if present. Call at the top of script entry points."""
    load_dotenv(dotenv_path=env_file, override=False)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any, indent: int = 2) -> None:
    path.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def truncate(text: str, max_len: int = 200) -> str:
    return text if len(text) <= max_len else text[:max_len - 3] + "..."
