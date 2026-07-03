from .base import EmployeeBaseSerializer
from .fields import UPDATE_FIELDS


class EmployeeUpdateSerializer(
    EmployeeBaseSerializer,
):
    class Meta(EmployeeBaseSerializer.Meta):
        fields = UPDATE_FIELDS
