"""
Patient Timeline service tests.
"""

from __future__ import annotations

from apps.patient_management.timeline.services import (
    activate_timeline,
    archive_timeline,
    deactivate_timeline,
    restore_timeline,
)


def test_timeline_service_exports_lifecycle_operations() -> None:
    """Ensure all Timeline lifecycle service operations are importable."""

    assert callable(activate_timeline)
    assert callable(deactivate_timeline)
    assert callable(archive_timeline)
    assert callable(restore_timeline)
