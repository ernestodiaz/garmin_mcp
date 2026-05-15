from garmin_client import get_client


def get_user_profile() -> dict:
    return get_client().get_user_profile()


def get_full_name() -> str:
    return get_client().get_full_name()


def get_devices() -> list:
    return get_client().get_devices()


def get_device_settings(device_id: str) -> dict:
    return get_client().get_device_settings(device_id)
