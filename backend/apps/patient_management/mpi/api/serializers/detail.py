"""
Detail serializer for the Master Patient Index.
"""

from __future__ import annotations

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)
from rest_framework import serializers


class MPIDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving an MPI record.
    """

    class Meta:
        model = MasterPatientIndex
        fields = "__all__"
