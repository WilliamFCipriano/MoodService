from MoodService.exceptions.core import MoodServiceException


class UserPasswordValidationException(MoodServiceException):
    """This is raised when the username or password is incorrect"""
    pass


class UsernameAlreadyInUseException(MoodServiceException):
    """This is raised when the username selected is already in use"""
    pass
