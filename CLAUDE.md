# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

MCP server that exposes Garmin Connect data as tools for Claude. Uses the unofficial `garminconnect` Python library (cyberjunky/python-garminconnect) which wraps Garmin's web API.

## Commands

```bash
# Install dependencies
uv sync

# Authenticate once (interactive — required before running server)
uv run python auth.py

# Run the MCP server (stdio transport, for Claude Desktop)
uv run python server.py

# Inspect tools interactively
uv run mcp dev server.py
```

## Setup

Copy `.env.example` to `.env` and fill in credentials. Then run `auth.py` once to cache OAuth tokens to `~/.garth`. The server reads cached tokens on startup; `auth.py` only needs to be re-run if tokens expire.

## Architecture

```
server.py           # FastMCP server — all MCP tool definitions live here
garmin_client.py    # Garmin session singleton; handles token caching via garth
auth.py             # One-shot interactive auth script (not part of server)
tools/
  activities.py     # Thin wrappers around garminconnect activity methods
  health.py         # Daily stats, steps, floors, hydration, training status
  sleep.py          # Sleep stages and scores
  biometrics.py     # HR, stress, Body Battery, HRV, respiration, SpO2
  body.py           # Body composition (weight, BMI, body fat)
  user.py           # User profile and devices
```

**Key design decisions:**
- `garmin_client.get_client()` returns a singleton `Garmin` instance. On first call it tries to load tokens from the tokenstore; if absent it does a fresh OAuth login and saves tokens.
- Tool functions in `tools/` are plain Python functions — no MCP decorators. `server.py` owns all `@mcp.tool()` registrations so the MCP interface is visible in one place.
- All tools return JSON strings. Errors are caught per-tool and returned as `{"error": "...", "message": "..."}` so Claude can handle them gracefully.
- Date parameters default to today (`datetime.date.today().isoformat()`). All Garmin endpoints accept `YYYY-MM-DD` strings.

## Claude Desktop config

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uv",
      "args": ["run", "--directory", "C:/Temp/claude/mcp_garmin", "python", "server.py"],
      "env": {
        "GARMIN_EMAIL": "your@email.com",
        "GARMIN_PASSWORD": "yourpassword"
      }
    }
  }
}
```

## Adding new tools

1. Add a function to the appropriate `tools/*.py` module calling the relevant `garminconnect` method.
2. Add a `@mcp.tool()` decorated function in `server.py` that calls it, wraps in `try/except`, and returns `_ok(data)` or `_err(e)`.
