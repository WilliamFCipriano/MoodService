from MoodService.repositories import user_repository


def test_create_user(managed_database):
    new_user_id = user_repository.create_new_user("testuser", "PASSWORDHASH")
    assert new_user_id == 0


def test_lookup_user(managed_database):
    new_user_id = user_repository.create_new_user("testuser", "PASSWORDHASH")
    user = user_repository.get_user_by_id(new_user_id)

    assert user.username == "testuser"
    assert user.password == "PASSWORDHASH"


