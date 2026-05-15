from garmin_client import get_client


def get_daily_stats(date: str) -> dict:
    return get_client().get_stats(date)


def get_user_summary(date: str) -> dict:
    return get_client().get_user_summary(date)


def get_steps_data(date: str) -> list:
    return get_client().get_steps_data(date)


def get_floors(date: str) -> list:
    return get_client().get_floors(date)


def get_hydration_data(date: str) -> dict:
    return get_client().get_hydration_data(date)


def get_intensity_minutes(date: str) -> dict:
    return get_client().get_intensity_minutes_data(date)


def get_training_status(date: str) -> dict:
    return get_client().get_training_status(date)


def get_training_readiness(date: str) -> dict:
    return get_client().get_training_readiness(date)


def get_fitnessage(date: str) -> dict:
    return get_client().get_fitnessage(date)


def get_goals(goal_type: str = "active") -> list:
    return get_client().get_goals(goal_type)


def get_earned_badges() -> list:
    return get_client().get_earned_badges()
