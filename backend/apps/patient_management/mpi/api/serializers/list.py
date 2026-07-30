"""
List serializer for the Master Patient Index.
"""

from __future__ import annotations

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)
from rest_framework import serializers


class MPIListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing MPI records.
    """

    class Meta:
        model = MasterPatientIndex
        fields = (
            "id",
            "mpi_id",
            "patient",
            "status",
            "verification_status",
            "match_confidence",
            "merge_status",
            "created_at",
        )
