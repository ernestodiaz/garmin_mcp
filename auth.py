#!/usr/bin/env python3
"""
Run once to authenticate and cache OAuth tokens.
After this the MCP server authenticates automatically.

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

import dill as pickle

warnings.filterwarnings("ignore", category=DeprecationWarning)

from dotenv import load_dotenv
from garminconnect import Garmin

load_dotenv()

TOKENSTORE = Path(os.getenv("GARMIN_TOKENSTORE", str(Path.home() / ".garth")))
_PICKLE = TOKENSTORE / "garmin_session.pkl"

email = os.getenv("GARMIN_EMAIL") or input("Garmin email: ")
password = os.getenv("GARMIN_PASSWORD") or input("Garmin password: ")

MAX_ATTEMPTS = 3
RETRY_DELAYS = [30, 60]


def prompt_mfa() -> str:
    return input("Enter MFA/2FA code from your authenticator app: ").strip()


def save_session(api: Garmin) -> None:
    TOKENSTORE.mkdir(parents=True, exist_ok=True)
    if hasattr(api, "garth"):
        api.garth.dump(str(TOKENSTORE))
        print(f"Tokens cached at: {TOKENSTORE}")
    else:
        _PICKLE.write_bytes(pickle.dumps(api))
        print(f"Session cached at: {_PICKLE}")


def attempt_login(n: int) -> None:
    print(f"Attempt {n}/{MAX_ATTEMPTS}: connecting to Garmin...")
    api = Garmin(email=email, password=password, prompt_mfa=prompt_mfa)
    api.login()
    save_session(api)
    print(f"Logged in as: {api.get_full_name()}")
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
                    "This is enforced server-side — the code is correct.\n\n"
                    "Fix options:\n"
                    "  1. Wait 15-30 minutes, then run:  uv run python auth.py\n"
                    "  2. Switch to a mobile hotspot and retry\n"
                    "  3. Connect via VPN and retry"
                )
                sys.exit(1)
        else:
            print(f"Login failed: {msg}")
            sys.exit(1)
