import pytest
from datetime import datetime, timedelta
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import MoodService.repositories.sqlite_util as database_util
import MoodService.repositories.mood_report as mood_report_repository
import MoodService.repositories.user as user_repository
import MoodService.services.mood_report as mood_report_service


@pytest.fixture()
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_new_mood_report(managed_database):
    result = mood_report_service.create_new_mood_report(1, "happy")
    assert result == 1


def test_new_mood_report_failure(managed_database):
    mood_report_service.create_new_mood_report(2, "happy")
    with pytest.raises(MoodAlreadySubmittedException):
        mood_report_service.create_new_mood_report(2, "sad")


def test_calculate_mood_report_percentiles(managed_database):
    long_time_user_id = user_repository.create_new_user("longTimeUser", "hunter2")
    mood_report_repository.historical_mood_report(long_time_user_id, "great", datetime.now().date() - timedelta(days=9))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=8))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=7))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=6))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=5))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(long_time_user_id, "fantastic")

    mid_user_id = user_repository.create_new_user("midTimeUser", "hunter3")
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(mid_user_id, "better")

    short_user_id = user_repository.create_new_user("shortTimeUser", "hunter4")
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(short_user_id, "best day ever")

    first_day_user_id = user_repository.create_new_user("firstTimeUser", "hunter5")
    mood_report_service.create_new_mood_report(first_day_user_id, "first time here")

    percentiles = mood_report_service.calculate_mood_report_percentiles()

    assert percentiles[0.01] == 10
    assert percentiles[0.26] == 5
    assert percentiles[0.51] == 4
    assert percentiles[0.76] == 1


def test_get_streak_percentile(managed_database):
    long_time_user_id = user_repository.create_new_user("longTimeUser", "hunter2")
    mood_report_repository.historical_mood_report(long_time_user_id, "great", datetime.now().date() - timedelta(days=9))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=8))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=7))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=6))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=5))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(long_time_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(long_time_user_id, "fantastic")

    mid_user_id = user_repository.create_new_user("midTimeUser", "hunter3")
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=4))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(mid_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(mid_user_id, "better")

    short_user_id = user_repository.create_new_user("shortTimeUser", "hunter4")
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=3))
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(short_user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_service.create_new_mood_report(short_user_id, "best day ever")

    first_day_user_id = user_repository.create_new_user("firstTimeUser", "hunter5")
    mood_report_service.create_new_mood_report(first_day_user_id, "first time here")

    mood_report_service.calculate_mood_report_percentiles()

    assert mood_report_service.get_streak_percentile(10) == 25
    assert mood_report_service.get_streak_percentile(5) == 50
    assert mood_report_service.get_streak_percentile(4) == 75
    assert mood_report_service.get_streak_percentile(1) == 99



