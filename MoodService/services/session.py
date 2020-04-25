import MoodService.repositories.session as session_repository
from MoodService.objects.session import Session


def validate_token(token: str) -> Session:
    """Validates a given token and returns a Session object if it matches,
    throws SessionNotFoundException if not"""
    return session_repository.get_session_by_token(token)


def create_session(user_int_id: int, token: str) -> Session:
    """Creates a new session in the database for future use"""
    return session_repository.create_session(user_int_id, token)