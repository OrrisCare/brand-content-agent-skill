"""
Save data to Notion databases via Scalekit proxy.

Usage:
  uv run skills/brand-content-agent/scripts/notion_save.py --database content-library --data '{"title": "...", ...}'
  uv run skills/brand-content-agent/scripts/notion_save.py --database scripts --data '{"title": "...", ...}'
  uv run skills/brand-content-agent/scripts/notion_save.py --database creators --data '{"name": "...", ...}'

Output: Created page ID and URL to stdout.
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scalekit_client import actions, USER_IDENTIFIER, NOTION_CONNECTION_NAME

# Database IDs — set these in .env after creating Notion databases
DATABASES = {
    "content-library": os.getenv("NOTION_DB_CONTENT_LIBRARY"),
    "scripts": os.getenv("NOTION_DB_SCRIPTS"),
    "creators": os.getenv("NOTION_DB_CREATORS"),
    "calendar": os.getenv("NOTION_DB_CALENDAR"),
}


def create_page(database_key: str, properties: dict) -> dict:
    """Create a page in a Notion database via Scalekit proxy."""
    db_id = DATABASES.get(database_key)
    if not db_id:
        print(f"Error: No database ID configured for '{database_key}'.", file=sys.stderr)
        print(f"Set NOTION_DB_{database_key.upper().replace('-', '_')} in .env", file=sys.stderr)
        sys.exit(1)

    print(f"[Notion] Creating page in '{database_key}' database...", file=sys.stderr)

    response = actions.request(
        connection_name=NOTION_CONNECTION_NAME,
        identifier=USER_IDENTIFIER,
        path="/v1/pages",
        method="POST",
        headers={"Notion-Version": "2022-06-28"},
        body={
            "parent": {"database_id": db_id},
            "properties": properties,
        },
    )
    if hasattr(response, "json"):
        return response.json()
    return response


def build_content_library_properties(data: dict) -> dict:
    """Build Notion properties for Content Library database."""
    props = {}
    if data.get("title"):
        props["Name"] = {"title": [{"text": {"content": data["title"][:2000]}}]}
    if data.get("platform"):
        props["Platform"] = {"select": {"name": data["platform"]}}
    if data.get("creator"):
        props["Creator"] = {"rich_text": [{"text": {"content": data["creator"]}}]}
    if data.get("url"):
        props["URL"] = {"url": data["url"]}
    if data.get("views"):
        props["Views"] = {"number": data["views"]}
    if data.get("likes"):
        props["Likes"] = {"number": data["likes"]}
    if data.get("comments"):
        props["Comments"] = {"number": data["comments"]}
    if data.get("engagement_rate"):
        props["Engagement Rate"] = {"number": data["engagement_rate"]}
    if data.get("posted_date"):
        props["Posted Date"] = {"date": {"start": data["posted_date"]}}
    if data.get("hashtags"):
        props["Hashtags"] = {"multi_select": [{"name": h} for h in data["hashtags"][:10]]}
    if data.get("hook_type"):
        props["Hook Type"] = {"select": {"name": data["hook_type"]}}
    if data.get("format"):
        props["Format"] = {"select": {"name": data["format"]}}
    if data.get("why_it_worked"):
        props["Why It Worked"] = {"rich_text": [{"text": {"content": data["why_it_worked"][:2000]}}]}
    if data.get("relevance"):
        props["Relevance"] = {"select": {"name": data["relevance"]}}
    return props


def build_script_properties(data: dict) -> dict:
    """Build Notion properties for Content Scripts database."""
    props = {}
    if data.get("title"):
        props["Title"] = {"title": [{"text": {"content": data["title"]}}]}
    if data.get("platform"):
        props["Platform"] = {"select": {"name": data["platform"]}}
    if data.get("format"):
        props["Format"] = {"select": {"name": data["format"]}}
    if data.get("hook"):
        props["Hook"] = {"rich_text": [{"text": {"content": data["hook"][:2000]}}]}
    if data.get("script"):
        props["Script"] = {"rich_text": [{"text": {"content": data["script"][:2000]}}]}
    if data.get("cta"):
        props["CTA"] = {"rich_text": [{"text": {"content": data["cta"]}}]}
    if data.get("status"):
        props["Status"] = {"select": {"name": data["status"]}}
    if data.get("priority"):
        props["Priority"] = {"select": {"name": data["priority"]}}
    return props


def build_creator_properties(data: dict) -> dict:
    """Build Notion properties for Creator Prospects database."""
    props = {}
    if data.get("name"):
        props["Name"] = {"title": [{"text": {"content": data["name"]}}]}
    if data.get("platform"):
        props["Platform"] = {"select": {"name": data["platform"]}}
    if data.get("handle"):
        props["Handle"] = {"rich_text": [{"text": {"content": data["handle"]}}]}
    if data.get("followers"):
        props["Followers"] = {"number": data["followers"]}
    if data.get("engagement_rate"):
        props["Engagement Rate"] = {"number": data["engagement_rate"]}
    if data.get("niche"):
        props["Niche"] = {"multi_select": [{"name": n} for n in data["niche"][:5]]}
    if data.get("email"):
        props["Email"] = {"email": data["email"]}
    if data.get("collab_type"):
        props["Collab Type"] = {"select": {"name": data["collab_type"]}}
    if data.get("relevance_score"):
        props["Relevance Score"] = {"number": data["relevance_score"]}
    if data.get("outreach_status"):
        props["Outreach Status"] = {"select": {"name": data["outreach_status"]}}
    return props


PROPERTY_BUILDERS = {
    "content-library": build_content_library_properties,
    "scripts": build_script_properties,
    "creators": build_creator_properties,
}


def main():
    parser = argparse.ArgumentParser(description="Save data to Notion")
    parser.add_argument("--database", required=True, choices=DATABASES.keys())
    parser.add_argument("--data", required=True, help="JSON string of data to save")
    args = parser.parse_args()

    data = json.loads(args.data)
    builder = PROPERTY_BUILDERS.get(args.database)
    if not builder:
        print(f"Error: No property builder for '{args.database}'", file=sys.stderr)
        sys.exit(1)

    properties = builder(data)
    result = create_page(args.database, properties)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
