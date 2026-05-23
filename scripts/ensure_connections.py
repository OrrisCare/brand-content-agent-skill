"""
Ensures all required connections are ACTIVE.
Prints auth links for any that aren't connected yet.
For BEARER providers (Apify), sets credentials from env automatically.

Usage: uv run skills/brand-content-agent/scripts/ensure_connections.py
"""

import os
import sys
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scalekit_client import (
    actions, USER_IDENTIFIER,
    APIFY_CONNECTION_NAME, NOTION_CONNECTION_NAME, GMAIL_CONNECTION_NAME,
)
from pathlib import Path
from dotenv import load_dotenv

_config_env = Path.home() / ".config" / "brand-content-agent" / ".env"
if not load_dotenv(_config_env) and not load_dotenv():
    pass

# OAuth connectors — need user to click an auth link
OAUTH_CONNECTIONS = {
    "Notion": NOTION_CONNECTION_NAME,
    "Gmail": GMAIL_CONNECTION_NAME,
}


def get_scalekit_access_token() -> str:
    env_url = os.getenv("SCALEKIT_ENV_URL")
    resp = requests.post(
        f"{env_url}/oauth/token",
        data={
            "grant_type": "client_credentials",
            "client_id": os.getenv("SCALEKIT_CLIENT_ID"),
            "client_secret": os.getenv("SCALEKIT_CLIENT_SECRET"),
        },
    )
    return resp.json()["access_token"]


def provision_apify_token():
    """Set Apify BEARER token from APIFY_TOKEN env var via Scalekit REST API."""
    apify_token = os.getenv("APIFY_TOKEN")
    if not apify_token:
        print("  ✗ Apify — APIFY_TOKEN not set. Run: uv run scripts/setup.py", file=sys.stderr)
        return False

    response = actions.get_or_create_connected_account(
        connection_name=APIFY_CONNECTION_NAME,
        identifier=USER_IDENTIFIER,
    )
    ca = response.connected_account

    # Check if token is already stored
    if ca.authorization_details is not None:
        print(f"  ✓ Apify ({APIFY_CONNECTION_NAME}) — ACTIVE")
        return True

    # Token not stored yet — provision via REST API
    env_url = os.getenv("SCALEKIT_ENV_URL")
    access_token = get_scalekit_access_token()
    r = requests.put(
        f"{env_url}/api/v1/connected_accounts",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json={
            "id": ca.id,
            "connector": APIFY_CONNECTION_NAME,
            "identifier": USER_IDENTIFIER,
            "connected_account": {
                "authorization_details": {
                    "static_auth": {"details": {"token": apify_token}}
                }
            },
        },
    )
    if r.status_code == 200:
        print(f"  ✓ Apify ({APIFY_CONNECTION_NAME}) — token provisioned from APIFY_TOKEN")
        return True
    else:
        print(f"  ✗ Apify ({APIFY_CONNECTION_NAME}) — failed to provision token: {r.text[:200]}")
        return False


def check_oauth_connection(display_name: str, connection_name: str) -> bool:
    """Check an OAuth connection. Returns True if ACTIVE."""
    response = actions.get_or_create_connected_account(
        connection_name=connection_name,
        identifier=USER_IDENTIFIER,
    )
    account = response.connected_account

    if account.status == "ACTIVE":
        print(f"  ✓ {display_name} ({connection_name}) — ACTIVE")
        return True
    else:
        print(f"  ✗ {display_name} ({connection_name}) — {account.status}")
        link_response = actions.get_authorization_link(
            connection_name=connection_name,
            identifier=USER_IDENTIFIER,
        )
        print(f"    → Authorize: {link_response.link}")
        return False


def main():
    print(f"\n[Scalekit] Checking connections for user: {USER_IDENTIFIER}\n")

    all_active = True

    # Apify: BEARER — auto-provision from env
    if not provision_apify_token():
        all_active = False

    # OAuth connectors — require user click
    for display_name, conn_name in OAUTH_CONNECTIONS.items():
        try:
            if not check_oauth_connection(display_name, conn_name):
                all_active = False
        except Exception as e:
            print(f"  ✗ {display_name} ({conn_name}) — ERROR: {e}")
            all_active = False

    print()
    if all_active:
        print("[Scalekit] All connections are active. Ready to go!")
    else:
        print("[Scalekit] Some connections need authorization.")
        print("           Click the links above, authorize, then re-run this script.")

    return 0 if all_active else 1


if __name__ == "__main__":
    sys.exit(main())
