"""
Update serializer for the Master Patient Index.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


class MPIUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an MPI record.
    """

    class Meta:
        model = MasterPatientIndex
        fields = (
            "abha_number",
            "aadhaar_number",
            "passport_number",
            "status",
            "verification_status",
            "record_source",
            "match_confidence",
            "merge_status",
            "merged_into",
            "notes",
        )
