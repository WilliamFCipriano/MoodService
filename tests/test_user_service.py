import pytest
from MoodService.services import user as user_service
from MoodService.repositories import sqlite_util as database_util
from MoodService.repositories import user as user_repository


@pytest.fixture(scope="module")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()


def test_register_new_user(managed_database):
    user_service.register_new_user("HappyUser", "hunter2")
    user = user_repository.get_user_by_id("HAPPYUSER")
    assert user.username == "HAPPYUSER"


def test_validate_user_password(managed_database):
    user_service.register_new_user("UnhappyUser", "hunter3")
    assert user_service.validate_user_password("UnhappyUser", "hunter3")