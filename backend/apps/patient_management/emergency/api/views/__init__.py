"""Patient emergency API views."""

from apps.patient_management.emergency.api.views.lifecycle import (
    EmergencyLifecycleView,
)
from apps.patient_management.emergency.api.views.list_create import (
    EmergencyListCreateView,
)
from apps.patient_management.emergency.api.views.retrieve_update_destroy import (
    EmergencyRetrieveUpdateDestroyView,
)

__all__ = (
    "EmergencyLifecycleView",
    "EmergencyListCreateView",
    "EmergencyRetrieveUpdateDestroyView",
)
