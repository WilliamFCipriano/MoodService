import pytest
from MoodService.exceptions.mood_report import MoodAlreadySubmittedException
import MoodService.repositories.sqlite_util as database_util
import MoodService.services.mood_report as mood_report_service


@pytest.fixture()
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_new_mood_report(managed_database):
    result = mood_report_service.create_new_mood_report(1, "happy")
    assert isinstance(result, int)


def test_new_mood_report_failure(managed_database):
    mood_report_service.create_new_mood_report(2, "happy")
    with pytest.raises(MoodAlreadySubmittedException):
        mood_report_service.create_new_mood_report(2, "sad")