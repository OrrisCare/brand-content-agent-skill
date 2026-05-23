"""
Search Instagram/TikTok for trending content via Apify MCP through Scalekit.

Usage: uv run skills/brand-content-agent/scripts/search_content.py --query "fitness tips" --platform instagram --max-results 15

Output: JSON array of discovered content to stdout.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apify_client import run_actor_and_fetch, get_apify_tools


def search_instagram(query: str, max_results: int) -> list[dict]:
    print(f"[Apify] Searching Instagram for '{query}' (max {max_results})...", file=sys.stderr)
    return run_actor_and_fetch(
        "apify/instagram-hashtag-scraper",
        {"hashtags": [query], "resultsLimit": max_results, "resultsType": "posts"},
        max_results,
    )


def search_tiktok(query: str, max_results: int) -> list[dict]:
    print(f"[Apify] Searching TikTok for '{query}' (max {max_results})...", file=sys.stderr)
    return run_actor_and_fetch(
        "clockworks/tiktok-scraper",
        {"searchQueries": [query], "resultsPerPage": max_results, "shouldDownloadVideos": False},
        max_results,
    )


def search_actors(query: str) -> list:
    """Search Apify Store for relevant actors via MCP."""
    print(f"[Apify] Searching Apify Store for: '{query}'...", file=sys.stderr)
    tool_map = get_apify_tools()
    result = tool_map["apifymcp_search_actors"].invoke({"query": query})
    if isinstance(result, str):
        try:
            import ast
            result = ast.literal_eval(result)
        except Exception:
            pass
    if isinstance(result, list):
        return result
    if isinstance(result, dict):
        return result.get("items", [])
    return []


def main():
    parser = argparse.ArgumentParser(description="Search for trending content")
    parser.add_argument("--query", required=True, help="Search query or hashtag")
    parser.add_argument("--platform", choices=["instagram", "tiktok", "both"], default="instagram")
    parser.add_argument("--max-results", type=int, default=15)
    parser.add_argument("--find-actors", action="store_true", help="Search Apify Store for actors")
    args = parser.parse_args()

    if args.find_actors:
        results = search_actors(args.query)
    else:
        results = []
        if args.platform in ("instagram", "both"):
            results.extend(search_instagram(args.query, args.max_results))
        if args.platform in ("tiktok", "both"):
            results.extend(search_tiktok(args.query, args.max_results))

    print(f"[Search] Found {len(results)} results.", file=sys.stderr)
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
