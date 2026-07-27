"""
Family Member API views.
"""

from .create import FamilyMemberCreateAPIView
from .delete import FamilyMemberDeleteAPIView
from .detail import FamilyMemberDetailAPIView
from .list import FamilyMemberListAPIView
from .update import FamilyMemberUpdateAPIView

__all__ = [
    "FamilyMemberCreateAPIView",
    "FamilyMemberDeleteAPIView",
    "FamilyMemberDetailAPIView",
    "FamilyMemberListAPIView",
    "FamilyMemberUpdateAPIView",
]
