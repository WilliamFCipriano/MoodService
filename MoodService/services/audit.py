import logging
import MoodService.constants as constants


def get_logger(service_name: str) -> logging.Logger:
    logger = logging.getLogger(service_name + "_service")
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(constants.log_location)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    return logger
