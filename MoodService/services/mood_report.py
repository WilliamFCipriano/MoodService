import MoodService.repositories.mood_report as mood_report_repository
import MoodService.services.audit as audit
import MoodService.repositories.user as user_repository
from MoodService.exceptions.mood_report import PercentileMatrixNotInitializedException
import math
import collections

log = audit.get_logger('mood_report')


def _percent_range(start: float,stop: float, step=0.01) -> collections.Iterable:
    """Produces an iterator that goes from 0.01 to 0.99"""
    while start < stop:
        yield round(start, 2)
        start += step


def create_new_mood_report(user_int_id: int, mood: str) -> int:
    """Creates a mood report for the current day, then returns the
    users current streak length"""
    log.info("Generating mood report for user: %s", user_int_id)
    mood_report_repository.new_mood_report(user_int_id, mood)
    return user_repository.get_user_streak_length(user_int_id)


def get_streak_percentile(streak: int) -> int:
    """Retrieves precalculated percentile for a given streak length"""
    log.info("Getting streak percentile for: %s", streak)
    try:
        return int(mood_report_repository.get_percentile_for_streak(streak) * 100)
    except PercentileMatrixNotInitializedException:
        calculate_mood_report_percentiles()
    return int(mood_report_repository.get_percentile_for_streak(streak) * 100)


def calculate_mood_report_percentiles() -> dict:
    """Calculates the percentile of every user currently on a streak,
    then saves that result to the database, returns output as a dictionary"""
    log.info("Calculating mood report percentiles")
    user_totals = mood_report_repository.get_streak_eligible_user_totals()

    k = len(user_totals)
    percentiles = dict()

    for n in _percent_range(0.01, 1.00):
        index = math.ceil(k * n)
        percentiles[round(1.00 - n, 2)] = user_totals[index - 1][0]

    mood_report_repository.save_percentile_data(percentiles)
    return percentiles


def get_mood_reports_by_id(user_int_id: int) -> list:
    """Returns a list of dictionaries containing mood report data"""
    log.info("Getting all mood reports for user: %s", user_int_id)
    mood_reports = mood_report_repository.get_mood_reports_by_user(user_int_id)

    results = list()
    for mood_report in mood_reports:
        results.append(mood_report.__dict__)

    return results


def update_mood_report(user_int_id: int, mood: str):
    """Updates a previously recorded mood"""
    log.info("Updating mood for user: %s", user_int_id)
    mood_report_repository.update_mood_report_by_user(user_int_id, mood)