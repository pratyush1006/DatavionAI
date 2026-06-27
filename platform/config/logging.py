"""
Enterprise logging configuration for DatavionAI.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_id": {
            "()": "apps.common.logging.RequestIDFilter",
        },
    },
    "formatters": {
        "standard": {
            "format": (
                "[{asctime}] "
                "{levelname:<8} "
                "{name:<20} "
                "[{request_id}] "
                "{message}"
            ),
            "style": "{",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
        "verbose": {
            "format": (
                "[{asctime}] "
                "{levelname:<8} "
                "{name:<20} "
                "[{request_id}] "
                "{module}:{lineno} "
                "{message}"
            ),
            "style": "{",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": ["request_id"],
        },
        "application_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "application.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
            "level": "ERROR",
            "filters": ["request_id"],
        },
        "audit_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "audit.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
            "encoding": "utf-8",
            "filters": ["request_id"],
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
        "audit": {
            "handlers": [
                "console",
                "audit_file",
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
        "django": {
            "handlers": [
                "console",
                "application_file",
            ],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": [
                "console",
                "error_file",
            ],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": {
            "handlers": [
                "console",
            ],
            "level": "INFO",
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
