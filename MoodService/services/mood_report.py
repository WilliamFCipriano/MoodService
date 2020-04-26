import MoodService.repositories.mood_report as mood_report_repository
import MoodService.repositories.user as user_repository
from MoodService.exceptions.mood_report import PercentileMatrixNotInitializedException
import math


def percent_range(start,stop, step=0.01):
    while start < stop:
        yield round(start, 2)
        start +=step


def create_new_mood_report(user_id, mood) -> int:
    mood_report_repository.new_mood_report(user_id, mood)
    return user_repository.get_user_streak_length(user_id)


def get_streak_percentile(streak: int) -> int:
    try:
        return int(mood_report_repository.get_percentile_for_streak(streak) * 100)
    except PercentileMatrixNotInitializedException:
        calculate_mood_report_percentiles()
    return int(mood_report_repository.get_percentile_for_streak(streak) * 100)


def calculate_mood_report_percentiles() -> dict:
    user_totals = mood_report_repository.get_streak_eligible_user_totals()

    k = len(user_totals)
    percentiles = dict()

    for n in percent_range(0.01, 1.00):
        index = math.ceil(k * n)
        percentiles[round(1.00 - n, 2)] = user_totals[index - 1][0]

    mood_report_repository.save_percentile_data(percentiles)
    return percentiles

