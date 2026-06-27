"""
Central logging configuration for DatavionAI.

All logging configuration lives here to keep settings.py clean.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": ("[{asctime}] " "{levelname} " "{name} " "{message}"),
            "style": "{",
        },
        "verbose": {
            "format": (
                "[{asctime}] " "{levelname} " "{name} " "{module}:{lineno} " "{message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "application_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "application.log",
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "error.log",
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
    "loggers": {
        "application": {
            "handlers": [
                "console",
                "application_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "error": {
            "handlers": [
                "console",
                "error_file",
            ],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {
        "handlers": [
            "console",
        ],
        "level": "INFO",
    },
}
