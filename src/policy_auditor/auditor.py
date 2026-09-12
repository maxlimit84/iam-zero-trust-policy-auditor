"""
Core audit logic: compare live Conditional Access policies against the
Zero Trust baseline and produce a list of Finding objects describing
any drift.

This module is intentionally the first thing to build out — start here.
Each check_* function below is a placeholder for one baseline rule from
baselines/zero_trust_baseline.yaml.
"""

from __future__ import annotations

from dataclasses import dataclass

from .baselines import load_baseline
from .graph_client import get_conditional_access_policies


@dataclass
class Finding:
    policy_name: str
    severity: str
    message: str


def check_mfa_required(policy: dict) -> Finding | None:
    """Flag policies that don't enforce MFA as a grant control."""
    grant_controls = policy.get("grantControls") or {}
    built_in_controls = grant_controls.get("builtInControls") or []

    if "mfa" not in built_in_controls:
        return Finding(
            policy_name=policy.get("displayName", "unknown"),
            severity="high",
            message="Policy does not require MFA as a grant control.",
        )
    return None


def check_legacy_auth_blocked(policy: dict) -> Finding | None:
    """Flag policies meant to block legacy auth that aren't set to 'block'."""
    conditions = policy.get("conditions") or {}
    client_app_types = conditions.get("clientAppTypes") or []

    targets_legacy_auth = "exchangeActiveSync" in client_app_types or "other" in client_app_types
    grant_controls = policy.get("grantControls") or {}
    blocks_access = grant_controls.get("builtInControls") == ["block"]

    if targets_legacy_auth and not blocks_access:
        return Finding(
            policy_name=policy.get("displayName", "unknown"),
            severity="high",
            message="Policy targets legacy auth clients but does not block access.",
        )
    return None


def run_audit() -> list[Finding]:
    """Fetch live policies, run each check, and return all findings."""
    # Baseline is loaded here so it's validated even before checks run;
    # wiring specific rules to specific check functions is the next step.
    load_baseline()

    policies = get_conditional_access_policies()

    findings: list[Finding] = []
    for policy in policies:
        for check in (check_mfa_required, check_legacy_auth_blocked):
            result = check(policy)
            if result:
                findings.append(result)

    return findings
