from MoodService.repositories import session as session_repository
import pytest
import MoodService.repositories.sqlite_util as database_util

@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_create_session(managed_database):
    result = session_repository.create_session(1,'RaNdOmToKeN')

    assert result.user_int_id == 1


def test_get_session_by_token(managed_database):
    created_session = session_repository.create_session(2, "RaNdOmErToKeN")

    session_validation_result = session_repository.get_session_by_token("RaNdOmErToKeN")

    assert created_session.user_int_id == session_validation_result.user_int_id
    assert created_session.session_id == created_session.session_id
