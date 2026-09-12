# IAM / Zero Trust Policy Auditor

A Python tool that connects to the Microsoft Graph API and audits Microsoft
Entra ID (Azure AD) Conditional Access policies and identity configuration
against a Zero Trust / least-privilege baseline — flagging policy drift
before it becomes an incident.

## Why this exists

Conditional Access policies tend to sprawl over time: exceptions get added
for one-off business needs, legacy protocols get re-enabled "just for now,"
and nobody circles back to clean it up. This tool gives a repeatable,
scriptable way to check a tenant's actual policy configuration against a
defined Zero Trust baseline (MFA enforcement, blocked legacy auth,
device compliance requirements, least-privilege role assignments, etc.) and
produce a report of where reality has drifted from policy.

## Status

🚧 Early scaffold — architecture and first working checks in progress.

## Planned features

- Pull Conditional Access policies via Microsoft Graph (`/identity/conditionalAccess/policies`)
- Compare each policy against a YAML-defined Zero Trust baseline
- Flag drift: missing MFA requirements, legacy auth not blocked, overly
  broad user/app scoping, disabled policies that should be enabled
- Generate a human-readable report (console + Markdown/JSON export)
- Read-only by design — this tool audits, it does not modify tenant policy

## Tech stack

- Python 3.11+
- [MSAL for Python](https://github.com/AzureAD/microsoft-authentication-library-for-python) for auth against Microsoft Entra ID
- Microsoft Graph REST API
- PyYAML for baseline rule definitions

## Getting started

1. Clone this repo and create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your own Azure AD app
   registration values (tenant ID, client ID, client secret). **Never commit
   `.env` — it's already in `.gitignore`.**
3. Run the auditor:
   ```bash
   python main.py
   ```

## Project layout

```
iam-zero-trust-policy-auditor/
├── main.py                        # CLI entry point
├── requirements.txt
├── .env.example                   # template for required auth config
├── baselines/
│   └── zero_trust_baseline.yaml   # the Zero Trust rules we audit against
├── src/policy_auditor/
│   ├── graph_client.py            # MSAL auth + Graph API calls
│   ├── baselines.py               # load/parse baseline rule definitions
│   ├── auditor.py                 # compare live policies vs. baseline
│   └── report.py                  # console/Markdown/JSON output
├── tests/
│   └── test_auditor.py            # unit tests against sample fixtures
└── docs/
    └── ARCHITECTURE.md
```

## Disclaimer

This is a personal portfolio/learning project. It is read-only against a
tenant's Conditional Access configuration and is not affiliated with or
endorsed by Microsoft.

## License

MIT — see [LICENSE](LICENSE).
