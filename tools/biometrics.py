from garmin_client import get_client


def get_heart_rates(date: str) -> dict:
    return get_client().get_heart_rates(date)


def get_resting_heart_rate(date: str) -> dict:
    return get_client().get_rhr_day(date)


def get_stress_data(date: str) -> dict:
    return get_client().get_stress_data(date)


def get_body_battery(date: str) -> list:
    return get_client().get_body_battery(date)


def get_hrv_data(date: str) -> dict:
    return get_client().get_hrv_data(date)


def get_respiration_data(date: str) -> dict:
    return get_client().get_respiration_data(date)


def get_spo2_data(date: str) -> dict:
    return get_client().get_spo2_data(date)
