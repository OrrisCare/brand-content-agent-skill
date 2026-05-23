# Brand Content Agent

A Claude Code skill for content intelligence, creator outreach, and script writing — powered by **Scalekit** (auth + MCP) and **Apify** (Instagram/TikTok scraping).

## What it does

- **Finds trending content** on Instagram and TikTok by hashtag
- **Scrapes creator profiles** and extracts emails from bios
- **Writes ready-to-film scripts** (15–60 second reels)
- **Saves everything to Notion** (content library, scripts, creator CRM)
- **Sends outreach emails** via Gmail

## Install

```bash
npx skills add OrrisCare/brand-content-agent-skill --skill brand-content-agent -g
```

[![skills.sh](https://skills.sh/b/OrrisCare/brand-content-agent-skill)](https://skills.sh/OrrisCare/brand-content-agent-skill)

## Setup

1. Install Python dependencies:
   ```bash
   uv sync
   ```

2. Run the interactive setup wizard — saves credentials to `~/.config/brand-content-agent/.env` (outside the skill directory, survives reinstalls):
   ```bash
   uv run scripts/setup.py
   ```

3. Authorize Notion + Gmail connections:
   ```bash
   uv run scripts/ensure_connections.py
   ```
   Apify is auto-provisioned from your token. Click the printed links for Notion and Gmail.

## Usage

Open Claude Code and ask things like:

- *"Find trending skincare content on Instagram"*
- *"Find micro-influencers in the fitness niche and get their emails"*
- *"Write 3 scripts for a coffee brand"*
- *"Send outreach to the creators we found"*
- *"Plan my content calendar for this week"*

## Stack

- [Scalekit AgentKit](https://docs.scalekit.com/agentkit/quickstart/) — OAuth, token vault, MCP proxy
- [Apify](https://apify.com) — Instagram + TikTok scrapers
- [Notion API](https://developers.notion.com) — content database
- Gmail API — outreach emails
