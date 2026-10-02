"""
Organization domain events.
"""

from __future__ import annotations

from .branding_updated import BrandingUpdatedEvent
from .feature_disabled import FeatureDisabledEvent
from .feature_enabled import FeatureEnabledEvent
from .hierarchy_changed import HierarchyChangedEvent
from .module_disabled import ModuleDisabledEvent
from .module_enabled import ModuleEnabledEvent
from .organization_activated import OrganizationActivatedEvent
from .organization_created import OrganizationCreatedEvent
from .organization_deactivated import OrganizationDeactivatedEvent
from .organization_deleted import OrganizationDeletedEvent
from .organization_restored import OrganizationRestoredEvent
from .organization_suspended import OrganizationSuspendedEvent
from .organization_updated import OrganizationUpdatedEvent
from .organization_verified import OrganizationVerifiedEvent
from .settings_updated import SettingsUpdatedEvent

__all__: tuple[str, ...] = (
    "BrandingUpdatedEvent",
    "FeatureDisabledEvent",
    "FeatureEnabledEvent",
    "HierarchyChangedEvent",
    "ModuleDisabledEvent",
    "ModuleEnabledEvent",
    "OrganizationActivatedEvent",
    "OrganizationCreatedEvent",
    "OrganizationDeactivatedEvent",
    "OrganizationDeletedEvent",
    "OrganizationRestoredEvent",
    "OrganizationSuspendedEvent",
    "OrganizationUpdatedEvent",
    "OrganizationVerifiedEvent",
    "SettingsUpdatedEvent",
)
