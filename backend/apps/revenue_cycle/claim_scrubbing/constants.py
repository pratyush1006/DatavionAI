"""Constants for Revenue Cycle claim scrubbing."""

from __future__ import annotations

from django.db import models


class ScrubStatus(models.TextChoices):
    """Lifecycle states for a scrub run."""

    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    PASSED = "passed", "Passed"
    FAILED = "failed", "Failed"
    OVERRIDDEN = "overridden", "Overridden"


class FindingSeverity(models.TextChoices):
    """Severity levels for scrub findings."""

    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    ERROR = "error", "Error"
    CRITICAL = "critical", "Critical"


class RuleType(models.TextChoices):
    """Supported deterministic scrub rule types."""

    REQUIRED = "required", "Required"
    RANGE = "range", "Range"
    FORMAT = "format", "Format"
    CONSISTENCY = "consistency", "Consistency"
    CODESET = "codeset", "Code Set"


__all__ = ("ScrubStatus", "FindingSeverity", "RuleType")
