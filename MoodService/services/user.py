import bcrypt
import MoodService.repositories.user as user_repository


def register_new_user(username: str, password: str) -> None:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    user_repository.create_new_user(username.upper(), hashed_password)


def validate_user_password(username: str, password: str) -> bool:
    user = user_repository.get_user_by_id(username.upper())
    return bcrypt.checkpw(password.encode('utf8'), user.password)