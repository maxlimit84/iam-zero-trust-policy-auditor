"""
Report formatting for audit findings — console, Markdown, and JSON output.
Currently a stub; console output is handled inline in main.py for now.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path


def write_json_report(findings, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(f) for f in findings], f, indent=2)
