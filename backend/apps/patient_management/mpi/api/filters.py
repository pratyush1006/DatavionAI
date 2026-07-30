"""
Filters for the Master Patient Index API.
"""

from __future__ import annotations

import django_filters

from apps.patient_management.mpi.models import (
    MasterPatientIndex,
)


class MPIFilter(django_filters.FilterSet):
    """
    FilterSet for MPI records.
    """

    class Meta:
        model = MasterPatientIndex
        fields = {
            "organization": ["exact"],
            "patient": ["exact"],
            "status": ["exact"],
            "verification_status": ["exact"],
            "record_source": ["exact"],
            "match_confidence": ["exact"],
            "merge_status": ["exact"],
            "mpi_id": ["exact", "icontains"],
            "abha_number": ["exact"],
        }


__all__ = [
    "MPIFilter",
]
