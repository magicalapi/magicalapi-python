"""
logging handling module to create custom and particular loggers.

"""

import logging

from magicalapi.settings import settings

logging.basicConfig(format=settings.logging_format, style="{")


def get_logger(
    name: str | None = None, log_level: str | None = settings.log_level
) -> logging.Logger:
    """
    get a logger object.

    Args:
        name (:obj:`str`, optional): Specify a name if you want
            to retrieve a logger which is a child of
            MagicalAPI logger.
        log_level (:obj:`str`, optional): Specify the log level
            for this particular logger.

    Returns:
        The MagicalAPI logger, or one of its children.
    """

    # create logger
    _logger_name = "MagicalAPI"
    if name:
        _logger_name += f".{name}"

    # create logger
    logger = logging.getLogger(name=_logger_name)
    # set log level
    if not log_level == None:
        logger.setLevel(log_level)
    logging.debug(f"logger created {logger}")

    return logger
