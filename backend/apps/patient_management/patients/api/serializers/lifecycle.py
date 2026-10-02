"""
Patient lifecycle action serializers.
"""

from __future__ import annotations

from rest_framework import serializers


class PatientLifecycleActionSerializer(
    serializers.Serializer,
):
    """
    Empty serializer for Patient lifecycle actions.

    Lifecycle transitions are identified entirely by the URL and are
    executed by their corresponding workflow.
    """


__all__ = ("PatientLifecycleActionSerializer",)
