import MoodService.repositories.mood_report as mood_report_repository
from MoodService.objects.mood_report import MoodReport


def create_new_mood_report(user_id, mood) -> int:
    mood_report_repository.new_mood_report(user_id, mood)
    return 99
