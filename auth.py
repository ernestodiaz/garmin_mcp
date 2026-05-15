#!/usr/bin/env python3
"""
Run once to authenticate and cache OAuth tokens.
After this the MCP server authenticates automatically via cached tokens.

If you get a 429 error, Garmin is rate limiting your IP.
Wait 15-30 minutes (or connect via a different network / VPN) then retry.

Usage:
    uv run python auth.py
"""

import os
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()

TOKENSTORE = Path(os.getenv("GARMIN_TOKENSTORE", str(Path.home() / ".garth")))
email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ")
password = os.getenv("GARMIN_PASSWORD") or input("Garmin password: ")

MAX_ATTEMPTS = 3
RETRY_DELAYS = [30, 60]


def prompt_mfa() -> str:
    return input("Enter MFA/2FA code from your authenticator app: ").strip()


def attempt_login(n: int) -> None:
    print(f"Attempt {n}/{MAX_ATTEMPTS}: connecting to Garmin...")
    api = Garmin(email=email, password=password, prompt_mfa=prompt_mfa)
    # Passing tokenstore causes login() to save tokens automatically on success
    api.login(str(TOKENSTORE))
    token_file = TOKENSTORE / "garmin_tokens.json"
    print(f"Logged in as: {api.get_full_name()}")
    print(f"Tokens cached at: {token_file}")
    print("The MCP server will now authenticate automatically.")


for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        attempt_login(attempt)
        sys.exit(0)
    except Exception as e:
        msg = str(e)
        if "429" in msg:
            if attempt < MAX_ATTEMPTS:
                wait = RETRY_DELAYS[attempt - 1]
                print(f"Rate limited (429). Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(
                    "\nGarmin is rate limiting logins from this IP (429).\n\n"
                    "Fix options:\n"
                    "  1. Wait 15-30 minutes, then run:  uv run python auth.py\n"
                    "  2. Switch to a mobile hotspot and retry\n"
                    "  3. Connect via VPN and retry"
                )
                sys.exit(1)
        else:
            print(f"Login failed: {msg}")
            sys.exit(1)
