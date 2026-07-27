"""
Application-level signals for the Datavion AI platform.
"""

from __future__ import annotations

from django.dispatch import Signal

#: Sent after the platform has completed startup.
application_started = Signal()

#: Sent before the platform begins shutdown.
application_stopping = Signal()

__all__ = [
    "application_started",
    "application_stopping",
]
