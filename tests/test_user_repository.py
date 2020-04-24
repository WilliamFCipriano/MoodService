from MoodService.repositories import user_repository
import pytest
import MoodService.repositories.sqlite_util as database_util


@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_create_user(managed_database):
    new_user_id = user_repository.create_new_user("testuser", "PASSWORDHASH")
    assert new_user_id == 1


def test_lookup_user(managed_database):
    new_user_id = user_repository.create_new_user("testuser2", "PASSWORDHASH")
    user = user_repository.get_user_by_id("testuser2")

    assert user.username == "testuser2"
    assert user.password == "PASSWORDHASH"
    assert user.int_id == new_user_id


