from garmin_client import get_client


def get_body_composition(start_date: str, end_date: str | None = None) -> dict:
    return get_client().get_body_composition(start_date, end_date)
