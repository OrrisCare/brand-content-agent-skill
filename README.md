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

1. Copy `.env.example` to `.env` in the skill directory and fill in your credentials:
   ```
   SCALEKIT_ENV_URL=https://your-env.scalekit.cloud
   SCALEKIT_CLIENT_ID=skc_...
   SCALEKIT_CLIENT_SECRET=sks_...
   APIFY_TOKEN=apify_api_...
   NOTION_CONNECTION_NAME=notion
   GMAIL_CONNECTION_NAME=gmail
   NOTION_DB_CONTENT_LIBRARY=<your-notion-db-id>
   ```

2. Install Python dependencies:
   ```bash
   uv sync
   ```

3. Authorize connections:
   ```bash
   uv run scripts/ensure_connections.py
   ```
   Apify is auto-provisioned from `APIFY_TOKEN`. Click the printed links for Notion and Gmail.

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
