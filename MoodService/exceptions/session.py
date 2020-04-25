from MoodService.exceptions.core import MoodServiceException


class SessionNotFoundException(MoodServiceException):
    """This exception is raised when a session can not be found for
    a given token."""
    pass
