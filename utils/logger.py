"""
Centralised logger used across the test suite.
In CI the output appears in the pipeline logs verbatim.
"""
import logging
import colorlog


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter(
            "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s — %(message)s",
            log_colors={
                "DEBUG":    "cyan",
                "INFO":     "green",
                "WARNING":  "yellow",
                "ERROR":    "red",
                "CRITICAL": "bold_red",
            }
        ))
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    return logger
