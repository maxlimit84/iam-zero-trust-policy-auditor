"""
Unit tests for the audit checks, using sample policy fixtures — no live
Graph API calls. Run with: pytest
"""

from src.policy_auditor.auditor import check_legacy_auth_blocked, check_mfa_required

POLICY_MISSING_MFA = {
    "displayName": "Require MFA for admins",
    "grantControls": {"builtInControls": []},
}

POLICY_WITH_MFA = {
    "displayName": "Require MFA for all users",
    "grantControls": {"builtInControls": ["mfa"]},
}

POLICY_LEGACY_AUTH_NOT_BLOCKED = {
    "displayName": "Legacy auth policy",
    "conditions": {"clientAppTypes": ["exchangeActiveSync"]},
    "grantControls": {"builtInControls": ["mfa"]},
}

POLICY_LEGACY_AUTH_BLOCKED = {
    "displayName": "Block legacy auth",
    "conditions": {"clientAppTypes": ["exchangeActiveSync", "other"]},
    "grantControls": {"builtInControls": ["block"]},
}


def test_check_mfa_required_flags_missing_mfa():
    finding = check_mfa_required(POLICY_MISSING_MFA)
    assert finding is not None
    assert finding.severity == "high"


def test_check_mfa_required_passes_when_mfa_present():
    assert check_mfa_required(POLICY_WITH_MFA) is None


def test_check_legacy_auth_flags_unblocked_policy():
    finding = check_legacy_auth_blocked(POLICY_LEGACY_AUTH_NOT_BLOCKED)
    assert finding is not None
    assert finding.severity == "high"


def test_check_legacy_auth_passes_when_blocked():
    assert check_legacy_auth_blocked(POLICY_LEGACY_AUTH_BLOCKED) is None
