import pytest
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import MoodService.repositories.sqlite_util as database_util
import MoodService.repositories.mood_report as mood_report_repository


@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_new_mood_report(managed_database):
    mood_report_repository.new_mood_report(1,'happy')


def test_new_mood_report_failure(managed_database):
    with pytest.raises(MoodAlreadySubmittedException):
        mood_report_repository.new_mood_report(2, 'happy')
        mood_report_repository.new_mood_report(2, 'sad')
