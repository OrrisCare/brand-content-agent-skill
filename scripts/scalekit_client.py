"""
Shared Scalekit client initialization.
All scripts import this to get the configured client + actions object.
"""

import scalekit.client
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

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
