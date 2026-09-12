"""
IAM / Zero Trust Policy Auditor — CLI entry point.

Usage:
    python main.py

Pulls Conditional Access policies from Microsoft Graph, compares them
against the Zero Trust baseline in baselines/zero_trust_baseline.yaml,
and prints a drift report.
"""

from src.policy_auditor.auditor import run_audit


def main() -> None:
    findings = run_audit()

    if not findings:
        print("No drift detected — all policies match the Zero Trust baseline.")
        return

    print(f"Found {len(findings)} finding(s):\n")
    for finding in findings:
        print(f"  [{finding.severity}] {finding.policy_name}: {finding.message}")


if __name__ == "__main__":
    main()
