from MoodService.exceptions.core import MoodServiceException


class MoodAlreadySubmittedException(MoodServiceException):
    """raised when a mood has already been reported by the user"""
    pass


class PercentileMatrixNotInitializedException(MoodServiceException):
    """raised when the percentile matrix has not yet been calculated"""
    pass
