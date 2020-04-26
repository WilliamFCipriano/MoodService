import pytest
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import MoodService.repositories.sqlite_util as database_util
import MoodService.repositories.mood_report as mood_report_repository


@pytest.fixture()
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_new_mood_report(managed_database):
    mood_report_repository.new_mood_report(10,'happy')


def test_new_mood_report_failure(managed_database):
    mood_report_repository.new_mood_report(10, 'happy')
    mood_report_repository.new_mood_report(20, 'happy')
    with pytest.raises(MoodAlreadySubmittedException):
        mood_report_repository.new_mood_report(20, 'happy')


def test_get_mood_reports_by_user(managed_database):
    mood_report_repository.new_mood_report(1000, 'happy')
    reports = mood_report_repository.get_mood_reports_by_user(1000)
    assert len(reports) == 1
