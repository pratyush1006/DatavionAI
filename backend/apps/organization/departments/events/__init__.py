"""
Department domain events.
"""

from apps.organization.departments.events.department_created import (
    DepartmentCreatedEvent,
)
from apps.organization.departments.events.department_deleted import (
    DepartmentDeletedEvent,
)
from apps.organization.departments.events.department_member_assigned import (
    DepartmentMemberAssignedEvent,
)
from apps.organization.departments.events.department_role_changed import (
    DepartmentRoleChangedEvent,
)
from apps.organization.departments.events.department_settings_updated import (
    DepartmentSettingsUpdatedEvent,
)
from apps.organization.departments.events.department_updated import (
    DepartmentUpdatedEvent,
)

__all__ = (
    "DepartmentCreatedEvent",
    "DepartmentUpdatedEvent",
    "DepartmentDeletedEvent",
    "DepartmentMemberAssignedEvent",
    "DepartmentRoleChangedEvent",
    "DepartmentSettingsUpdatedEvent",
)
