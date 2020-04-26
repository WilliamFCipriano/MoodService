from datetime import datetime, timedelta
from MoodService.repositories import user as user_repository
from MoodService.repositories import mood_report as mood_report_repository
import pytest
import MoodService.repositories.sqlite_util as database_util


@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_create_user(managed_database):
    new_user_id = user_repository.create_new_user("TESTUSER", "PASSWORDHASH")
    assert new_user_id == 1


def test_lookup_user(managed_database):
    new_user_id = user_repository.create_new_user("TESTUSER2", "PASSWORDHASH")
    user = user_repository.get_user_by_id("TESTUSER2")

    assert user.username == "TESTUSER2"
    assert user.password == "PASSWORDHASH"
    assert user.int_id == new_user_id


def test_get_user_streak_length(managed_database):
    user_id = user_repository.create_new_user("TESTUSER3", "PASSWORDHASH")
    mood_report_repository.new_mood_report(user_id, "happy")
    x = user_repository.get_user_streak_length(user_id)
    y = x


def test_get_user_streak_length_historical(managed_database):
    user_id = user_repository.create_new_user("TESTUSER4", "PASSWORDHASH")
    mood_report_repository.new_mood_report(user_id, "happy")
    mood_report_repository.historical_mood_report(user_id, "ok", datetime.now().date() - timedelta(days=1))
    mood_report_repository.historical_mood_report(user_id, "fine", datetime.now().date() - timedelta(days=2))
    mood_report_repository.historical_mood_report(user_id, "great", datetime.now().date() - timedelta(days=3))
    x = user_repository.get_user_streak_length(user_id)
    assert x == 4
