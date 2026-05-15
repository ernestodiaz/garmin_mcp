from garmin_client import get_client


def get_sleep_data(date: str) -> dict:
    return get_client().get_sleep_data(date)
