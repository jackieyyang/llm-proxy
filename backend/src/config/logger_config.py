import sys
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Handler to intercept standard logging and forward to loguru.

    Args:
        logging.Handler: Base logging handler
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def init_logger(log_level: str = "info") -> None:
    """
    Init the async logger configuration.

    Args:
        log_level (str): Logging level (default: "info")
    """

    # Remove default logger
    logger.remove()

    # Add async stdout handler with enqueue=True for async logging
    logger.add(
        sys.stdout,
        level=log_level.upper(),
        enqueue=True,  # Enable async logging
    )

    # Intercept standard logging and forward to loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # Intercept uvicorn and fastapi loggers
    for logger_name in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
    ):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler()]
        logging_logger.propagate = False