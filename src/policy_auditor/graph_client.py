"""
Authentication and Microsoft Graph API access.

Uses MSAL client-credentials flow (app-only auth) against an Azure AD
app registration with read-only Conditional Access permissions
(Policy.Read.All). This tool never writes to Graph — audit only.
"""

from __future__ import annotations

import os

import msal
import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_SCOPE = ["https://graph.microsoft.com/.default"]
GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"


def _get_access_token() -> str:
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_secret,
        authority=f"https://login.microsoftonline.com/{tenant_id}",
    )

    result = app.acquire_token_for_client(scopes=GRAPH_SCOPE)

    if "access_token" not in result:
        raise RuntimeError(
            f"Failed to acquire Graph access token: "
            f"{result.get('error')}: {result.get('error_description')}"
        )

    return result["access_token"]


def get_conditional_access_policies() -> list[dict]:
    """Fetch all Conditional Access policies from Microsoft Graph."""
    token = _get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{GRAPH_BASE_URL}/identity/conditionalAccess/policies"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json().get("value", [])
