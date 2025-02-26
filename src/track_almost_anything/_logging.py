import logging
import os
import sys

_logger = logging.getLogger("TrackerLogger")
__is_logger_configured__ = False


class TrackAlmostAnythingException(Exception):
    """Exception thrown by Track Almost Anything"""

    status_code = -1


class TrackerFileNotFoundError(TrackAlmostAnythingException):
    """Exception thrown by Track Almost Anything"""

    status_code = 3


class TrackerIncompatibleFileError(TrackAlmostAnythingException):
    """No compatible image files have been found."""

    status_code = 3


def configure_logger(log_level, log_dir: str = ""):
    global __is_logger_configured__
    if not __is_logger_configured__:
        __is_logger_configured__ = True

        fmt = logging.Formatter("[%(asctime)s] [Tracker %(levelname)s]: %(message)s")
        _logger.setLevel(log_level)

        if log_dir:
            log_file_out = os.path.join(log_dir, "tracker.log")
            log_file_handler = logging.FileHandler(log_file_out)

            log_file_handler.setLevel(log_level)
            log_file_handler.setFormatter(fmt)

            _logger.addHandler(log_file_handler)

    # Stream output
    handler_console_out = logging.StreamHandler(sys.stdout)
    handler_console_out.setLevel(log_level)
    handler_console_out.setFormatter(fmt)

    _logger.addHandler(handler_console_out)


def log_debug(log: str):
    _logger.debug(log)


def log_info(log: str):
    _logger.info(log)


def log_error(log: str):
    _logger.error(log)


def log_fatal(log: str):
    _logger.fatal(log)
