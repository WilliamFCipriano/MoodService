from MoodService.exceptions.core import MoodServiceException


class MoodAlreadySubmittedException(MoodServiceException):
    """Raised when a mood has already been reported by the user"""
    pass


class PercentileMatrixNotInitializedException(MoodServiceException):
    """Raised when the percentile matrix has not yet been calculated"""
    pass
