"""
Patient Timeline model tests.
"""

from __future__ import annotations

from apps.core.models import BaseModel
from apps.patient_management.timeline.models import TimelineEntry


def test_timeline_model_inherits_platform_base_model() -> None:
    """Ensure TimelineEntry uses the canonical platform persistence foundation."""

    assert issubclass(
        TimelineEntry,
        BaseModel,
    )


def test_timeline_model_uses_platform_lifecycle_fields() -> None:
    """Ensure core lifecycle fields are inherited from BaseModel."""

    assert TimelineEntry._meta.get_field("id") is not None
    assert TimelineEntry._meta.get_field("created_at") is not None
    assert TimelineEntry._meta.get_field("updated_at") is not None
    assert TimelineEntry._meta.get_field("is_deleted") is not None
    assert TimelineEntry._meta.get_field("deleted_at") is not None
    assert TimelineEntry._meta.get_field("deleted_by_id") is not None
    assert TimelineEntry._meta.get_field("is_active") is not None
