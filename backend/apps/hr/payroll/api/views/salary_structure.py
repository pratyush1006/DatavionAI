"""
API views for salary structures.
"""

from __future__ import annotations

from typing import Final

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.hr.payroll.api.serializers import (
    SalaryStructureCreateSerializer,
    SalaryStructureDetailSerializer,
    SalaryStructureListSerializer,
    SalaryStructureUpdateSerializer,
)
from apps.hr.payroll.models import SalaryStructure
from apps.hr.payroll.permissions import (
    CanCreateSalaryStructure,
    CanDeleteSalaryStructure,
    CanUpdateSalaryStructure,
    CanViewSalaryStructure,
)
from apps.hr.payroll.selectors import (
    get_salary_structure_by_id,
    get_salary_structures,
)
from apps.hr.payroll.services import (
    create_salary_structure,
    delete_salary_structure,
    update_salary_structure,
)

PAYROLL_TAG: Final[tuple[str, ...]] = ("Payroll",)


@extend_schema(tags=PAYROLL_TAG)
class SalaryStructureListCreateAPIView(BaseListCreateAPIView):
    """
    List existing salary structures or create a new one.
    """

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewSalaryStructure),
        "POST": (IsAuthenticated, CanCreateSalaryStructure),
    }

    serializer_classes = {
        "GET": SalaryStructureListSerializer,
        "POST": SalaryStructureCreateSerializer,
    }

    detail_serializer_class = SalaryStructureDetailSerializer

    create_service = create_salary_structure

    create_success_message = "Salary structure created successfully."

    search_fields = ("employee__employee_code",)

    ordering = ("-effective_from",)

    ordering_fields = ("effective_from", "created_at")

    filterset_fields = ("organization", "employee", "is_active")

    def get_queryset(self) -> QuerySet[SalaryStructure]:
        return get_salary_structures()


@extend_schema(tags=PAYROLL_TAG)
class SalaryStructureRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    Retrieve, update or delete a salary structure.
    """

    lookup_url_kwarg = "salary_structure_id"

    permission_classes_map = {
        "GET": (IsAuthenticated, CanViewSalaryStructure),
        "PUT": (IsAuthenticated, CanUpdateSalaryStructure),
        "PATCH": (IsAuthenticated, CanUpdateSalaryStructure),
        "DELETE": (IsAuthenticated, CanDeleteSalaryStructure),
    }

    serializer_classes = {
        "GET": SalaryStructureDetailSerializer,
        "PUT": SalaryStructureUpdateSerializer,
        "PATCH": SalaryStructureUpdateSerializer,
    }

    detail_serializer_class = SalaryStructureDetailSerializer

    update_service = update_salary_structure

    delete_service = delete_salary_structure

    update_success_message = "Salary structure updated successfully."

    def get_object(self):
        return get_salary_structure_by_id(
            salary_structure_id=self.kwargs[self.lookup_url_kwarg],
        )


__all__ = [
    "SalaryStructureListCreateAPIView",
    "SalaryStructureRetrieveUpdateDestroyAPIView",
]
