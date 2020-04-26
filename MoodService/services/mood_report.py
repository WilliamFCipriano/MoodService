import MoodService.repositories.mood_report as mood_report_repository
import MoodService.repositories.user as user_repository
import math
from MoodService.objects.mood_report import MoodReport


def percent_range(start,stop, step=0.01):
    while start < stop:
        yield round(start, 2)
        start +=step


def create_new_mood_report(user_id, mood) -> int:
    mood_report_repository.new_mood_report(user_id, mood)
    return user_repository.get_user_streak_length(user_id)


def calculate_mood_report_percentiles() -> dict:
    user_totals = mood_report_repository.get_streak_eligible_user_totals()

    k = len(user_totals)
    percentiles = dict()

    for n in percent_range(0.01, 1):
        index = math.ceil(k * n)
        percentiles[n] = user_totals[index - 1][0]

    return percentiles


