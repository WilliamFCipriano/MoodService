import MoodService.services.session as session_service
from MoodService.exceptions.session import SessionNotFoundException
import MoodService.repositories.session as session_repository
import pytest
import MoodService.repositories.sqlite_util as database_util


@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_create_session(managed_database):
    new_session = session_service.create_session(1,"ImAValidToken")
    session_from_database = session_repository.get_session_by_token("ImAValidToken")

    assert new_session.user_int_id == session_from_database.user_int_id
    assert new_session.session_id == session_from_database.session_id


def test_validate_token(managed_database):
    new_session = session_service.create_session(1,"ITooAmAValidToken")


def test_validate_token_failure_case(managed_database):
    with pytest.raises(SessionNotFoundException):
        session_service.validate_token("ThisTokenIsNotInTheDatabase")

