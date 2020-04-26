import bcrypt
import MoodService.services.audit as audit
import MoodService.repositories.user as user_repository
from MoodService.exceptions.user import UserPasswordValidationException
from MoodService.objects.user import User

log = audit.get_logger('user')


def register_new_user(username: str, password: str) -> None:
    """create new user in the database"""
    log.info("Registering new user: %s", username)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    user_repository.create_new_user(username, hashed_password)


def validate_user_password(username: str, password: str) -> User:
    """confirm that the users password is correct"""
    log.info("Checking password of user: %s", username)
    user = user_repository.get_user_by_id(username)

    if bcrypt.checkpw(password.encode('utf8'), user.password):
        log.info("Successful login for: %s", username)
        return user
    else:
        log.error("Password validation error for: %s", username)
        raise UserPasswordValidationException("The username or password provided are incorrect")