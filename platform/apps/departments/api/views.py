from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.departments.selectors import (
    get_department_by_id,
    get_departments,
)
from apps.departments.serializers import (
    DepartmentCreateSerializer,
    DepartmentDetailSerializer,
    DepartmentListSerializer,
    DepartmentUpdateSerializer,
)
from apps.departments.services import (
    create_department,
    delete_department,
    update_department,
)
from apps.rbac.permissions import (
    CanAddDepartments,
    CanChangeDepartments,
    CanDeleteDepartments,
    CanViewDepartments,
)


class DepartmentListCreateAPIView(ListCreateAPIView):
    """
    GET  -> List Departments
    POST -> Create Department
    """

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    search_fields = (
        "name",
        "code",
        "organization__name",
    )

    ordering = (
        "name",
    )

    ordering_fields = (
        "name",
        "code",
        "created_at",
    )

    filterset_fields = (
        "organization",
        "is_active",
    )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewDepartments,
            ]
        else:
            permission_classes = [
                IsAuthenticated,
                CanAddDepartments,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_queryset(self):
        return get_departments()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DepartmentCreateSerializer

        return DepartmentListSerializer

    @extend_schema(tags=["Departments"])
    def get(self, request, *args, **kwargs):
        return self.list(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Departments"])
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = create_department(
            serializer.validated_data.copy()
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data,
            status=status.HTTP_201_CREATED,
        )


class DepartmentRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    """
    GET
    PUT
    PATCH
    DELETE
    """

    lookup_url_kwarg = "department_id"

    def get_permissions(self):

        if self.request.method == "GET":
            permission_classes = [
                IsAuthenticated,
                CanViewDepartments,
            ]

        elif self.request.method in (
            "PUT",
            "PATCH",
        ):
            permission_classes = [
                IsAuthenticated,
                CanChangeDepartments,
            ]

        else:
            permission_classes = [
                IsAuthenticated,
                CanDeleteDepartments,
            ]

        return [
            permission()
            for permission in permission_classes
        ]

    def get_object(self):
        return get_department_by_id(
            self.kwargs["department_id"]
        )

    def get_serializer_class(self):

        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return DepartmentUpdateSerializer

        return DepartmentDetailSerializer

    @extend_schema(tags=["Departments"])
    def get(self, request, *args, **kwargs):
        return self.retrieve(
            request,
            *args,
            **kwargs,
        )

    @extend_schema(tags=["Departments"])
    def patch(self, request, *args, **kwargs):

        department = self.get_object()

        serializer = self.get_serializer(
            department,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = update_department(
            department,
            serializer.validated_data.copy(),
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data
        )

    @extend_schema(tags=["Departments"])
    def put(self, request, *args, **kwargs):

        department = self.get_object()

        serializer = self.get_serializer(
            department,
            data=request.data,
            partial=False,
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = update_department(
            department,
            serializer.validated_data.copy(),
        )

        return Response(
            DepartmentDetailSerializer(
                department
            ).data
        )

    @extend_schema(tags=["Departments"])
    def delete(self, request, *args, **kwargs):

        department = self.get_object()

        delete_department(
            department
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )