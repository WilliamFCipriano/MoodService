import pytest
import MoodService.repositories.sqlite_util as database_util


@pytest.fixture(scope="session")
def managed_database():
    database_util.create_database_if_not_exists()
    yield
    database_util.remove_database()