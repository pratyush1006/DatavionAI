"""
List serializer for the Master Patient Index.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


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
