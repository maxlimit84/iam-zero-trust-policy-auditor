# Architecture (early draft)

```
Microsoft Graph API
      │  (MSAL app-only auth, read-only)
      ▼
graph_client.py  ──►  live Conditional Access policies (JSON)
                              │
baselines/zero_trust_baseline.yaml
      │  (declarative rules)
      ▼
baselines.py  ──►  BaselineRule objects
                              │
                              ▼
auditor.py  ──►  runs check_* functions per policy ──►  Finding objects
                              │
                              ▼
report.py  ──►  console / Markdown / JSON output
```

## Design principles

- **Read-only.** This tool never writes to Microsoft Graph. It only reads
  Conditional Access configuration and reports on it.
- **Declarative baseline.** Rules live in YAML, not hardcoded in Python, so
  the baseline can be reviewed and adjusted independently of the check logic.
- **One check function per rule.** Keeps each check testable in isolation
  with fixture data (see tests/test_auditor.py) — no live tenant needed to
  run the test suite.

## Next steps

- Wire each YAML rule to its corresponding `check_*` function by `id`
  (currently the mapping is implicit/hardcoded in `run_audit`).
- Add checks for: compliant-device requirement, high-risk sign-in blocking,
  overly broad policy scoping (all users / all apps with no exclusions).
- Add Markdown/JSON report export (`report.py` is currently a stub).
- Add a `--dry-run` / sample-data mode so the CLI can be demoed without a
  real Azure AD tenant.
