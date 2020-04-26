import MoodService.repositories.session as session_repository
from MoodService.objects.session import Session
import MoodService.services.audit as audit
import secrets

log = audit.get_logger('session')


def _generate_session_token() -> str:
    """Returns a urlsafe token 64 characters long"""
    return secrets.token_urlsafe(64)


def create_session(user_int_id: int) -> Session:
    """Creates a new session in the database for future use"""
    log.info("Creating session for user: %s", user_int_id)
    return session_repository.create_session(user_int_id, _generate_session_token())


def validate_token(token: str) -> Session:
    """Validates a given token and returns a Session object if it matches,
    throws SessionNotFoundException if not"""
    log.info("Validating token starting with: %s", token[:4])
    return session_repository.get_session_by_token(token)
