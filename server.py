import json
import logging
from datetime import date as _date

from mcp.server.fastmcp import FastMCP

from tools import activities, biometrics, body, health, sleep, user

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("Garmin Connect")


def _today() -> str:
    return _date.today().isoformat()


def _ok(data) -> str:
    return json.dumps(data, default=str)


def _err(e: Exception) -> str:
    return json.dumps({"error": type(e).__name__, "message": str(e)})


# ── Activities ───────────────────────────────────────────────────────────────

@mcp.tool()
def list_activities(start: int = 0, limit: int = 20) -> str:
    """
    List recent Garmin activities (runs, rides, swims, etc.).

    Args:
        start: Pagination offset (0-based).
        limit: Number of activities to return (max 100).
    """
    try:
        return _ok(activities.list_activities(start, limit))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activities_by_date(start_date: str, end_date: str, activity_type: str = "") -> str:
    """
    List activities within a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format.
        end_date: End date in YYYY-MM-DD format.
        activity_type: Optional filter string (e.g. 'running', 'cycling', 'swimming', 'strength_training').
    """
    try:
        return _ok(activities.get_activities_by_date(start_date, end_date, activity_type))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity(activity_id: str) -> str:
    """
    Get full details for a single activity including metrics, GPS summary, and performance data.

    Args:
        activity_id: Garmin activity ID (visible in activity URLs on Garmin Connect).
    """
    try:
        return _ok(activities.get_activity(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_splits(activity_id: str) -> str:
    """
    Get lap/interval splits for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    try:
        return _ok(activities.get_activity_splits(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_split_summaries(activity_id: str) -> str:
    """
    Get aggregated split summaries (pace, HR, power per lap) for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    try:
        return _ok(activities.get_activity_split_summaries(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_hr_in_timezones(activity_id: str) -> str:
    """
    Get time spent in each heart rate zone for an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    try:
        return _ok(activities.get_activity_hr_in_timezones(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_weather(activity_id: str) -> str:
    """
    Get weather conditions recorded during an activity.

    Args:
        activity_id: Garmin activity ID.
    """
    try:
        return _ok(activities.get_activity_weather(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_exercise_sets(activity_id: str) -> str:
    """
    Get exercise sets for a strength/gym activity (reps, weight, set type).

    Args:
        activity_id: Garmin activity ID.
    """
    try:
        return _ok(activities.get_activity_exercise_sets(activity_id))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_last_activity() -> str:
    """Get the most recently recorded activity."""
    try:
        return _ok(activities.get_last_activity())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_activity_types() -> str:
    """List all Garmin activity types available for filtering."""
    try:
        return _ok(activities.get_activity_types())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_personal_records() -> str:
    """Get personal records (PRs) across all activity types."""
    try:
        return _ok(activities.get_personal_records())
    except Exception as e:
        return _err(e)


# ── Daily Health ─────────────────────────────────────────────────────────────

@mcp.tool()
def get_daily_stats(date: str = "") -> str:
    """
    Get comprehensive daily health summary: steps, calories, distance, active minutes, floors.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_daily_stats(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_user_summary(date: str = "") -> str:
    """
    Get the Garmin user daily summary for a date (similar to daily stats but with different fields).

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_user_summary(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_steps_data(date: str = "") -> str:
    """
    Get step count timeline throughout the day in 15-minute intervals.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_steps_data(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_floors(date: str = "") -> str:
    """
    Get floors climbed data for a day.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_floors(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_hydration_data(date: str = "") -> str:
    """
    Get hydration (water intake) data for a day.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_hydration_data(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_intensity_minutes(date: str = "") -> str:
    """
    Get moderate and vigorous intensity minutes for a day.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_intensity_minutes(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_training_status(date: str = "") -> str:
    """
    Get training status (peaking, productive, maintaining, recovery, etc.) for a date.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_training_status(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_training_readiness(date: str = "") -> str:
    """
    Get training readiness score and contributing factors for a date.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_training_readiness(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_fitnessage(date: str = "") -> str:
    """
    Get Garmin fitness age estimate for a date.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(health.get_fitnessage(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_goals(goal_type: str = "active") -> str:
    """
    Get fitness goals.

    Args:
        goal_type: One of 'active', 'future', or 'past'.
    """
    try:
        return _ok(health.get_goals(goal_type))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_earned_badges() -> str:
    """Get all badges earned by the user."""
    try:
        return _ok(health.get_earned_badges())
    except Exception as e:
        return _err(e)


# ── Sleep ────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_sleep_data(date: str = "") -> str:
    """
    Get detailed sleep data: stages (deep, light, REM, awake), score, and SpO2 during sleep.

    Args:
        date: Date in YYYY-MM-DD format (the morning after the sleep). Defaults to today.
    """
    try:
        return _ok(sleep.get_sleep_data(date or _today()))
    except Exception as e:
        return _err(e)


# ── Biometrics ───────────────────────────────────────────────────────────────

@mcp.tool()
def get_heart_rates(date: str = "") -> str:
    """
    Get heart rate readings throughout the day including resting HR.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_heart_rates(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_resting_heart_rate(date: str = "") -> str:
    """
    Get resting heart rate (RHR) for a day.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_resting_heart_rate(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_stress_data(date: str = "") -> str:
    """
    Get stress level readings throughout the day (0-100 scale, higher = more stressed).

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_stress_data(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_body_battery(date: str = "") -> str:
    """
    Get Body Battery energy levels throughout the day (0-100, tracks recovery vs. exertion).

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_body_battery(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_hrv_data(date: str = "") -> str:
    """
    Get Heart Rate Variability (HRV) summary including overnight average and status.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_hrv_data(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_respiration_data(date: str = "") -> str:
    """
    Get breathing rate (breaths per minute) throughout the day and during sleep.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_respiration_data(date or _today()))
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_spo2_data(date: str = "") -> str:
    """
    Get blood oxygen saturation (SpO2) readings for a day.

    Args:
        date: Date in YYYY-MM-DD format. Defaults to today.
    """
    try:
        return _ok(biometrics.get_spo2_data(date or _today()))
    except Exception as e:
        return _err(e)


# ── Body Composition ─────────────────────────────────────────────────────────

@mcp.tool()
def get_body_composition(start_date: str = "", end_date: str = "") -> str:
    """
    Get body composition data (weight, BMI, body fat percentage, muscle mass) for a date range.

    Args:
        start_date: Start date in YYYY-MM-DD format. Defaults to today.
        end_date: End date in YYYY-MM-DD format. Optional; defaults to start_date.
    """
    try:
        sd = start_date or _today()
        return _ok(body.get_body_composition(sd, end_date or None))
    except Exception as e:
        return _err(e)


# ── User & Devices ───────────────────────────────────────────────────────────

@mcp.tool()
def get_user_profile() -> str:
    """Get the authenticated user's Garmin profile (name, location, bio, profile picture URL)."""
    try:
        return _ok(user.get_user_profile())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_full_name() -> str:
    """Get the authenticated user's full name."""
    try:
        return _ok(user.get_full_name())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_devices() -> str:
    """List all Garmin devices registered to the account (watches, bike computers, etc.)."""
    try:
        return _ok(user.get_devices())
    except Exception as e:
        return _err(e)


@mcp.tool()
def get_device_settings(device_id: str) -> str:
    """
    Get settings for a specific Garmin device.

    Args:
        device_id: Device ID from get_devices().
    """
    try:
        return _ok(user.get_device_settings(device_id))
    except Exception as e:
        return _err(e)


if __name__ == "__main__":
    mcp.run()
