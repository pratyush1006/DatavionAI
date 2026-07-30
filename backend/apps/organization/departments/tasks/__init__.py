"""
Department tasks.
"""

from apps.organization.departments.tasks.indexing import (
    index_department,
    remove_department_index,
)
from apps.organization.departments.tasks.notifications import (
    send_department_created_notification,
    send_department_deleted_notification,
    send_department_member_assigned_notification,
    send_department_updated_notification,
)
from apps.organization.departments.tasks.synchronization import (
    synchronize_department,
)

__all__ = (
    "send_department_created_notification",
    "send_department_updated_notification",
    "send_department_deleted_notification",
    "send_department_member_assigned_notification",
    "index_department",
    "remove_department_index",
    "synchronize_department",
)
