"""
Shared Apify helpers — actor execution and dataset fetching via Scalekit MCP.

All other scripts import run_actor_and_fetch() from here instead of duplicating the logic.
"""

import ast
import os
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scalekit_client import actions, USER_IDENTIFIER, APIFY_CONNECTION_NAME

_apify_tools: dict | None = None


def get_apify_tools() -> dict:
    global _apify_tools
    if _apify_tools is None:
        tools = actions.langchain.get_tools(
            identifier=USER_IDENTIFIER,
            providers=[APIFY_CONNECTION_NAME.upper()],
            page_size=100,
        )
        _apify_tools = {t.name: t for t in tools}
    return _apify_tools


def fetch_dataset_items(dataset_id: str, limit: int) -> list[dict]:
    """Fetch dataset items directly via Apify API (MCP get-dataset-items is broken in Scalekit)."""
    token = os.getenv("APIFY_TOKEN")
    resp = requests.get(
        f"https://api.apify.com/v2/datasets/{dataset_id}/items",
        params={"limit": limit, "token": token},
    )
    if resp.status_code == 200:
        return resp.json()
    return []


def run_actor_and_fetch(actor: str, input_data: dict, max_results: int) -> list[dict]:
    """Run an Apify actor via Scalekit MCP and return the dataset items."""
    tool_map = get_apify_tools()
    run_result = tool_map["apifymcp_call_actor"].invoke({"actor": actor, "input": input_data})
    # LangChain returns Python repr string — parse with ast.literal_eval
    if isinstance(run_result, str):
        try:
            run_result = ast.literal_eval(run_result)
        except Exception:
            return []
    if not isinstance(run_result, dict):
        return []
    dataset_id = (
        run_result.get("storages", {}).get("datasets", {}).get("default", {}).get("id")
    )
    if not dataset_id:
        return []
    return fetch_dataset_items(dataset_id, max_results)
