import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


def setup_logging() -> None:
    """Configure application-wide logging once for the current process."""
    log_directory = Path("logs")
    log_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    log_file = log_directory / "library.log"
    file_log_level = logging.DEBUG
    console_log_level = logging.WARNING

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
        delay=True,
    )

    file_handler.setLevel(file_log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()

 
    for handler in root_logger.handlers:
        handler.close()
    root_logger.handlers.clear()

    root_logger.setLevel(file_log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)