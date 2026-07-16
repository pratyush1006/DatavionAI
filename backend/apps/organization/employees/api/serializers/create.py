from .base import EmployeeBaseSerializer
from .fields import WRITE_FIELDS


class EmployeeCreateSerializer(
    EmployeeBaseSerializer,
):
    class Meta(EmployeeBaseSerializer.Meta):
        fields = WRITE_FIELDS
