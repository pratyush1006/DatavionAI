"""
Notification admin registrations.
"""

from .notification import NotificationAdmin
from .notification_log import NotificationLogAdmin

__all__ = [
    "NotificationAdmin",
    "NotificationLogAdmin",
]
