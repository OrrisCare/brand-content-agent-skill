"""
Scrape full details of specific Instagram posts/profiles via Apify through Scalekit.

Usage:
  uv run skills/brand-content-agent/scripts/scrape_reels.py --urls "https://instagram.com/p/..."
  uv run skills/brand-content-agent/scripts/scrape_reels.py --profiles "@creator1" "@creator2"

Output: JSON array with full post/profile data. Profiles include extracted email from bio.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apify_client import run_actor_and_fetch


def extract_email_from_bio(bio: str) -> str | None:
    """Extract email address from an Instagram bio string."""
    if not bio:
        return None
    match = re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", bio)
    return match.group(0) if match else None


def scrape_instagram_posts(urls: list[str]) -> list[dict]:
    """Scrape full details of Instagram posts/reels via Apify."""
    print(f"[Apify] Scraping {len(urls)} Instagram posts...", file=sys.stderr)
    return run_actor_and_fetch(
        "apify/instagram-scraper",
        {"directUrls": urls, "resultsType": "posts", "addParentData": True},
        len(urls) * 10,
    )


def scrape_instagram_profiles(handles: list[str]) -> list[dict]:
    """Scrape Instagram profiles and extract emails from bios."""
    print(f"[Apify] Scraping {len(handles)} Instagram profiles...", file=sys.stderr)
    usernames = [h.lstrip("@") for h in handles]

    results = run_actor_and_fetch(
        "apify/instagram-profile-scraper",
        {"usernames": usernames},
        len(usernames) * 5,
    )

    # Enrich each profile with email extracted from bio
    for profile in results:
        bio = profile.get("biography") or profile.get("bio") or ""
        email = extract_email_from_bio(bio)
        if email:
            profile["email"] = email
        # Also check external URL field some scrapers return
        if not email and profile.get("externalUrl"):
            profile.setdefault("email", None)

    return results


def main():
    parser = argparse.ArgumentParser(description="Scrape reel/post/profile details")
    parser.add_argument("--urls", nargs="+", help="Post/reel URLs to scrape")
    parser.add_argument("--profiles", nargs="+", help="Profile handles to scrape")
    args = parser.parse_args()

    if not args.urls and not args.profiles:
        print("Error: provide --urls or --profiles", file=sys.stderr)
        sys.exit(1)

    results = []
    if args.urls:
        results.extend(scrape_instagram_posts(args.urls))
    if args.profiles:
        results.extend(scrape_instagram_profiles(args.profiles))

    print(f"[Scrape] Got details for {len(results)} items.", file=sys.stderr)
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    main()
