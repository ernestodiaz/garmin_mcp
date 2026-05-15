# MCP Garmin Connect

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that connects Claude to your Garmin Connect account, giving it access to all your health, fitness, and activity data.

Once connected, you can ask Claude things like:
- *"How did I sleep last night?"*
- *"Show me my running activities from this week"*
- *"What's my HRV trend over the past month?"*
- *"Compare my Body Battery levels on workout days vs rest days"*

## Features

### Activities
| Tool | Description |
|---|---|
| `list_activities` | Recent activities with pagination |
| `get_activities_by_date` | Activities filtered by date range and type |
| `get_activity` | Full detail for a single activity |
| `get_activity_splits` | Lap/interval splits |
| `get_activity_split_summaries` | Per-lap pace, HR, and power summaries |
| `get_activity_hr_in_timezones` | Time spent in each HR zone |
| `get_activity_weather` | Weather conditions during an activity |
| `get_activity_exercise_sets` | Sets/reps for strength training activities |
| `get_last_activity` | Most recently recorded activity |
| `get_activity_types` | All available Garmin activity types |
| `get_personal_records` | Personal records across all activity types |

### Daily Health
| Tool | Description |
|---|---|
| `get_daily_stats` | Steps, calories, distance, active minutes |
| `get_user_summary` | Daily summary with additional fields |
| `get_steps_data` | Step count in 15-minute intervals |
| `get_floors` | Floors climbed |
| `get_hydration_data` | Water intake |
| `get_intensity_minutes` | Moderate and vigorous intensity minutes |
| `get_training_status` | Peaking / productive / recovery status |
| `get_training_readiness` | Readiness score and contributing factors |
| `get_fitnessage` | Garmin fitness age estimate |
| `get_goals` | Active, future, or past fitness goals |
| `get_earned_badges` | All earned badges |

### Sleep
| Tool | Description |
|---|---|
| `get_sleep_data` | Sleep stages (deep/light/REM/awake), score, SpO2 |

### Biometrics
| Tool | Description |
|---|---|
| `get_heart_rates` | HR readings throughout the day |
| `get_resting_heart_rate` | Daily resting HR |
| `get_stress_data` | Stress levels throughout the day (0–100) |
| `get_body_battery` | Body Battery energy levels (0–100) |
| `get_hrv_data` | HRV overnight average and status |
| `get_respiration_data` | Breathing rate (breaths/min) |
| `get_spo2_data` | Blood oxygen saturation |

### Body Composition
| Tool | Description |
|---|---|
| `get_body_composition` | Weight, BMI, body fat %, muscle mass over a date range |

### User & Devices
| Tool | Description |
|---|---|
| `get_user_profile` | Name, location, bio |
| `get_full_name` | Authenticated user's name |
| `get_devices` | Registered Garmin devices |
| `get_device_settings` | Settings for a specific device |

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- A Garmin Connect account
- Claude Desktop

## Setup

### 1. Install dependencies

```bash
cd mcp_garmin
uv sync
```

### 2. Configure credentials

```bash
copy .env.example .env
```

Edit `.env` and fill in your Garmin email and password:

```env
GARMIN_EMAIL=your@email.com
GARMIN_PASSWORD=yourpassword
```

### 3. Authenticate

Run this once to log in and cache your OAuth tokens:

```bash
uv run python auth.py
```

If your account has two-factor authentication enabled, you will be prompted to enter a code from your authenticator app. After a successful login, tokens are saved to `~/.garth/garmin_tokens.json` and the server will authenticate automatically on every subsequent start — no MFA prompt needed again until the tokens expire.

> **Getting a 429 error?** Garmin rate-limits login attempts from the same IP. Wait 15–30 minutes and retry, or connect via a mobile hotspot or VPN.

### 4. Connect to Claude Desktop

Open your Claude Desktop configuration file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following (update the `--directory` path to match where you cloned this repo):

```json
{
  "mcpServers": {
    "garmin": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "C:\\Temp\\claude\\mcp_garmin",
        "python",
        "server.py"
      ],
      "env": {
        "GARMIN_EMAIL": "your@email.com",
        "GARMIN_PASSWORD": "yourpassword"
      }
    }
  }
}
```

Restart Claude Desktop. A hammer icon (🔨) will appear in the chat input confirming the tools are loaded.

## Usage

Just ask Claude naturally. All date parameters default to today if omitted.

**Activity examples:**
- *"List my last 10 running activities"*
- *"Show the splits for my most recent run"*
- *"What were my HR zones during my ride on Monday?"*

**Health examples:**
- *"How many steps did I take yesterday?"*
- *"What's my average resting heart rate this week?"*
- *"Show my Body Battery levels for today"*

**Sleep examples:**
- *"How did I sleep last night?"*
- *"How much deep sleep did I get this week?"*

**Trends and analysis:**
- *"Compare my stress levels on workout days vs rest days over the past 2 weeks"*
- *"Is my HRV improving this month?"*
- *"Show my weight trend for the last 30 days"*

## Development

Test tools interactively with the MCP Inspector (opens in browser):

```bash
uv run mcp dev server.py
```

## Notes

- This project uses the unofficial Garmin Connect API via the [`garminconnect`](https://github.com/cyberjunky/python-garminconnect) library. Garmin does not provide a public API, so availability may change without notice.
- Cached tokens are stored at `~/.garth/garmin_tokens.json`. Delete this file to force re-authentication.
- If tokens expire, re-run `uv run python auth.py`.
