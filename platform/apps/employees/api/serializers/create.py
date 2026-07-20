from rest_framework import serializers

from apps.employees.api.serializers.base import EmployeeBaseSerializer
from apps.employees.api.serializers.fields import CREATE_FIELDS


class EmployeeCreateSerializer(
    EmployeeBaseSerializer,
):
    """
    Serializer for creating a new employee.
    """

    class Meta(EmployeeBaseSerializer.Meta):
        fields = CREATE_FIELDS
