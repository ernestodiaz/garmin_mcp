from garmin_client import get_client


def list_activities(start: int, limit: int) -> list:
    return get_client().get_activities(start, limit)


def get_activities_by_date(start_date: str, end_date: str, activity_type: str = "") -> list:
    return get_client().get_activities_by_date(
        start_date, end_date, activity_type or None
    )


def get_activity(activity_id: str) -> dict:
    return get_client().get_activity(activity_id)


def get_activity_splits(activity_id: str) -> dict:
    return get_client().get_activity_splits(activity_id)


def get_activity_split_summaries(activity_id: str) -> dict:
    return get_client().get_activity_split_summaries(activity_id)


def get_activity_hr_in_timezones(activity_id: str) -> dict:
    return get_client().get_activity_hr_in_timezones(activity_id)


def get_activity_weather(activity_id: str) -> dict:
    return get_client().get_activity_weather(activity_id)


def get_activity_exercise_sets(activity_id: str) -> dict:
    return get_client().get_excercise_sets(activity_id)


def get_last_activity() -> dict:
    return get_client().get_last_activity()


def get_activity_types() -> list:
    return get_client().get_activity_types()


def get_personal_records() -> list:
    return get_client().get_personal_record()
