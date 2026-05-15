import os
import logging
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=DeprecationWarning)

from garminconnect import Garmin
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_client: Garmin | None = None
TOKENSTORE = Path(os.getenv("GARMIN_TOKENSTORE", str(Path.home() / ".garth")))


def get_client() -> Garmin:
    global _client
    if _client is not None:
        return _client

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        raise RuntimeError(
            "GARMIN_EMAIL and GARMIN_PASSWORD must be set. "
            "Copy .env.example to .env, fill in credentials, then run `uv run python auth.py` once."
        )

    def _no_mfa() -> str:
        raise RuntimeError(
            "MFA required but no interactive session available. "
            "Run `uv run python auth.py` to re-authenticate."
        )

    api = Garmin(email=email, password=password, prompt_mfa=_no_mfa)
    # login(tokenstore) loads cached tokens if present; falls back to fresh
    # credential login and auto-saves tokens on success.
    api.login(str(TOKENSTORE))
    logger.info("Authenticated as %s", api.full_name)

    _client = api
    return _client


def reset_client() -> None:
    """Force re-authentication on next get_client() call."""
    global _client
    _client = None
