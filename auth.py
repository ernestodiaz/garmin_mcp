#!/usr/bin/env python3
"""
Run once interactively to authenticate and cache OAuth tokens.
After this, the MCP server uses cached tokens automatically.

Usage:
    uv run python auth.py

If you get a 429 error, Garmin is rate limiting logins from your IP.
Wait 15-30 minutes, or try from a different network / VPN, then retry.
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKENSTORE = Path(os.getenv("GARMIN_TOKENSTORE", str(Path.home() / ".garth")))

email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ")
password = os.getenv("GARMIN_PASSWORD") or input("Garmin password: ")

MAX_ATTEMPTS = 3
RETRY_DELAYS = [30, 60]  # seconds between attempts


def attempt_login(attempt: int) -> None:
    print(f"\nAttempt {attempt}/{MAX_ATTEMPTS}: logging in to Garmin Connect...")
    try:
        import garth
        garth.login(email, password)
        TOKENSTORE.mkdir(parents=True, exist_ok=True)
        garth.save(str(TOKENSTORE))
    except Exception as e:
        raise RuntimeError(str(e)) from e

    print("Verifying tokens...")
    from garminconnect import Garmin
    api = Garmin()
    api.login(str(TOKENSTORE))
    print(f"\nSuccess! Logged in as: {api.get_full_name()}")
    print(f"Tokens cached at: {TOKENSTORE}")
    print("\nThe MCP server will now authenticate automatically.")


for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        attempt_login(attempt)
        sys.exit(0)
    except Exception as e:
        msg = str(e)
        is_rate_limited = "429" in msg

        if not is_rate_limited or attempt == MAX_ATTEMPTS:
            if is_rate_limited:
                print(
                    "\nGarmin is rate limiting logins from this IP address.\n"
                    "This is enforced server-side — the code is correct.\n\n"
                    "To fix:\n"
                    "  1. Wait 15-30 minutes and run auth.py again\n"
                    "  2. Connect via VPN and run auth.py again\n"
                    "  3. Try from a different network (mobile hotspot, etc.)"
                )
            else:
                print(f"\nLogin failed: {msg}")
            sys.exit(1)

        wait = RETRY_DELAYS[attempt - 1]
        print(f"Rate limited (429). Waiting {wait}s before retry...")
        time.sleep(wait)
