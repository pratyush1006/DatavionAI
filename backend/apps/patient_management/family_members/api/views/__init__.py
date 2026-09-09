"""
Family Member API views.
"""

from .lifecycle import (
    FamilyMemberActivateAPIView,
    FamilyMemberDeactivateAPIView,
    FamilyMemberRestoreAPIView,
    FamilyMemberSetEmergencyContactAPIView,
    FamilyMemberSetNextOfKinAPIView,
)
from .list_create import FamilyMemberListCreateAPIView
from .retrieve_update_destroy import FamilyMemberRetrieveUpdateDestroyAPIView

__all__ = (
    "FamilyMemberActivateAPIView",
    "FamilyMemberDeactivateAPIView",
    "FamilyMemberRestoreAPIView",
    "FamilyMemberSetEmergencyContactAPIView",
    "FamilyMemberSetNextOfKinAPIView",
    "FamilyMemberListCreateAPIView",
    "FamilyMemberRetrieveUpdateDestroyAPIView",
)
