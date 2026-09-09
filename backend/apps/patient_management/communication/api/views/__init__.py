"""Patient Communication API view exports."""

from __future__ import annotations

from apps.patient_management.communication.api.views.lifecycle import (
    CommunicationLifecycleView,
)
from apps.patient_management.communication.api.views.list_create import (
    CommunicationListCreateView,
)
from apps.patient_management.communication.api.views.retrieve_update_destroy import (
    CommunicationRetrieveUpdateDestroyView,
)

__all__ = (
    "CommunicationListCreateView",
    "CommunicationLifecycleView",
    "CommunicationRetrieveUpdateDestroyView",
)
