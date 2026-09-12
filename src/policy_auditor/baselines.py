"""
Load and represent the Zero Trust baseline rule set.

The baseline is defined declaratively in baselines/zero_trust_baseline.yaml
so it can be reviewed, versioned, and adjusted without touching code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

DEFAULT_BASELINE_PATH = Path(__file__).resolve().parents[2] / "baselines" / "zero_trust_baseline.yaml"


@dataclass
class BaselineRule:
    id: str
    description: str
    severity: str


def load_baseline(path: Path = DEFAULT_BASELINE_PATH) -> list[BaselineRule]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    return [
        BaselineRule(id=rule["id"], description=rule["description"], severity=rule["severity"])
        for rule in raw.get("rules", [])
    ]
