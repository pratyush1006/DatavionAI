"""Patient Relationship API views."""

from .lifecycle import (
    PatientRelationshipActivateAPIView,
    PatientRelationshipDeactivateAPIView,
    PatientRelationshipRestoreAPIView,
    PatientRelationshipSetPrimaryAPIView,
    PatientRelationshipTerminateAPIView,
    PatientRelationshipVerifyAPIView,
)
from .list_create import PatientRelationshipListCreateAPIView
from .retrieve_update_destroy import PatientRelationshipRetrieveUpdateDestroyAPIView

__all__ = (
    "PatientRelationshipActivateAPIView",
    "PatientRelationshipDeactivateAPIView",
    "PatientRelationshipListCreateAPIView",
    "PatientRelationshipRestoreAPIView",
    "PatientRelationshipRetrieveUpdateDestroyAPIView",
    "PatientRelationshipSetPrimaryAPIView",
    "PatientRelationshipTerminateAPIView",
    "PatientRelationshipVerifyAPIView",
)
