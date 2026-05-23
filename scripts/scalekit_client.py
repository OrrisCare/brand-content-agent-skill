"""
Shared Scalekit client initialization.
All scripts import this to get the configured client + actions object.
"""

import scalekit.client
import os
from pathlib import Path
from dotenv import load_dotenv

# Credentials live in ~/.config/brand-content-agent/.env — outside the skill
# directory so they survive reinstalls and `npx skills add` updates.
_config_env = Path.home() / ".config" / "brand-content-agent" / ".env"
if not load_dotenv(_config_env) and not load_dotenv():
    pass  # no .env found — os.getenv calls below will return None and fail clearly

scalekit_client = scalekit.client.ScalekitClient(
    client_id=os.getenv("SCALEKIT_CLIENT_ID"),
    client_secret=os.getenv("SCALEKIT_CLIENT_SECRET"),
    env_url=os.getenv("SCALEKIT_ENV_URL"),
)
actions = scalekit_client.actions

USER_IDENTIFIER = os.getenv("USER_IDENTIFIER", "user_123")
APIFY_CONNECTION_NAME = os.getenv("APIFY_CONNECTION_NAME", "apifymcp")
NOTION_CONNECTION_NAME = os.getenv("NOTION_CONNECTION_NAME", "notion")
GMAIL_CONNECTION_NAME = os.getenv("GMAIL_CONNECTION_NAME", "gmail")
