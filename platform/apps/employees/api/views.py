from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.api.base_generics import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView,
)
from apps.employees.selectors import (
    get_employee_by_id,
    get_employees,
)
from apps.employees.serializers import (
    EmployeeCreateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeeUpdateSerializer,
)
from apps.employees.services import (
    create_employee,
    delete_employee,
    update_employee,
)
from apps.rbac.permissions import (
    CanAddEmployees,
    CanChangeEmployees,
    CanDeleteEmployees,
    CanViewEmployees,
)


class EmployeeListCreateAPIView(BaseListCreateAPIView):
    """
    GET -> List Employees
    POST -> Create Employee
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "employee_code",
        "user__first_name",
        "user__last_name",
        "user__email",
        "designation",
    )

    ordering = ("employee_code",)

    ordering_fields = (
        "employee_code",
        "hire_date",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "department",
        "team",
        "designation",
        "is_active",
    )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewEmployees,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                CanAddEmployees,
            ]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return get_employees()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EmployeeCreateSerializer

        return EmployeeListSerializer

    @extend_schema(tags=["Employees"])
    def get(self, request, *args, **kwargs):
        return self.list(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Employees"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        employee = create_employee(
            serializer.validated_data.copy(),
        )

        return Response(
            EmployeeDetailSerializer(employee).data,
            status=status.HTTP_201_CREATED,
        )


class EmployeeRetrieveUpdateDestroyAPIView(
    BaseRetrieveUpdateDestroyAPIView,
):
    """
    GET
    PUT
    PATCH
    DELETE
    """

    lookup_url_kwarg = "employee_id"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewEmployees,
            ]

        elif self.request.method in (
            "PUT",
            "PATCH",
        ):
            permission_classes = [
                IsAuthenticated,
                CanChangeEmployees,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                CanDeleteEmployees,
            ]

        return [permission() for permission in permission_classes]

    def get_object(self):
        return get_employee_by_id(
            self.kwargs["employee_id"],
        )

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return EmployeeUpdateSerializer

        return EmployeeDetailSerializer

    @extend_schema(tags=["Employees"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Employees"])
    def patch(self, request, *args, **kwargs):
        employee = self.get_object()

        serializer = self.get_serializer(
            employee,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        employee = update_employee(
            employee,
            serializer.validated_data.copy(),
        )

        return Response(
            EmployeeDetailSerializer(employee).data,
        )

    @extend_schema(tags=["Employees"])
    def put(self, request, *args, **kwargs):
        employee = self.get_object()

        serializer = self.get_serializer(
            employee,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(raise_exception=True)

        employee = update_employee(
            employee,
            serializer.validated_data.copy(),
        )

        return Response(
            EmployeeDetailSerializer(employee).data,
        )

    @extend_schema(tags=["Employees"])
    def delete(self, request, *args, **kwargs):
        employee = self.get_object()

        delete_employee(employee)

        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
