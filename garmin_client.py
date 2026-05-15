import os
import logging
import warnings
from pathlib import Path

import dill as pickle

warnings.filterwarnings("ignore", category=DeprecationWarning)

from garminconnect import Garmin
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_client: Garmin | None = None
TOKENSTORE = Path(os.getenv("GARMIN_TOKENSTORE", str(Path.home() / ".garth")))
_PICKLE = TOKENSTORE / "garmin_session.pkl"


def _save_session(api: Garmin) -> None:
    TOKENSTORE.mkdir(parents=True, exist_ok=True)
    if hasattr(api, "garth"):
        api.garth.dump(str(TOKENSTORE))
        logger.info("Tokens saved via garth to %s", TOKENSTORE)
    else:
        _PICKLE.write_bytes(pickle.dumps(api))
        logger.info("Session saved via pickle to %s", _PICKLE)


def _load_session() -> Garmin | None:
    """Try to restore a previously authenticated session."""
    if _PICKLE.exists():
        try:
            api = pickle.loads(_PICKLE.read_bytes())
            api.get_full_name()  # quick liveness check
            logger.info("Session restored from pickle at %s", _PICKLE)
            return api
        except Exception as e:
            logger.info("Pickle session invalid (%s), will re-authenticate", e)
    return None


def get_client() -> Garmin:
    global _client
    if _client is not None:
        return _client

    # Try pickle first (works with newer garminconnect that dropped garth)
    api = _load_session()
    if api:
        _client = api
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

    # Try garth-style tokenstore (older garminconnect)
    try:
        api.login(str(TOKENSTORE))
        logger.info("Logged in via garth tokenstore at %s", TOKENSTORE)
        _client = api
        return _client
    except Exception:
        pass

    logger.info("No cached session found. Run `uv run python auth.py` to authenticate.")
    raise RuntimeError(
        "No cached session found. Run `uv run python auth.py` first."
    )


def reset_client() -> None:
    """Force re-authentication on next get_client() call."""
    global _client
    _client = None
