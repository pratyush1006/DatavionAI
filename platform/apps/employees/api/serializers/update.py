from rest_framework import serializers

from apps.employees.api.serializers.base import EmployeeBaseSerializer
from apps.employees.api.serializers.fields import UPDATE_FIELDS


class EmployeeUpdateSerializer(
    EmployeeBaseSerializer,
):
    """
    Serializer for updating an existing employee.
    """

    class Meta(EmployeeBaseSerializer.Meta):
        fields = UPDATE_FIELDS
