"""
Enterprise logging configuration for DatavionOS.

Centralized Django logging configuration built on top of the
apps.common.logging framework.
"""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "request_context": {
            "()": ("apps.common.logging.RequestContextFilter"),
        },
        "health_check": {
            "()": ("apps.common.logging.HealthCheckFilter"),
        },
    },
    "formatters": {
        "console": {
            "()": ("apps.common.logging.ConsoleFormatter"),
        },
        "json": {
            "()": ("apps.common.logging.JSONFormatter"),
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
            "filters": [
                "request_context",
                "health_check",
            ],
        },
        "application_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(
                LOG_DIR / "application.log",
            ),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "formatter": "json",
            "filters": [
                "request_context",
            ],
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(
                LOG_DIR / "error.log",
            ),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "encoding": "utf-8",
            "level": "ERROR",
            "formatter": "json",
            "filters": [
                "request_context",
            ],
        },
        "audit_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(
                LOG_DIR / "audit.log",
            ),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 10,
            "encoding": "utf-8",
            "formatter": "json",
            "filters": [
                "request_context",
            ],
        },
    },
    "loggers": {
        "apps": {
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
