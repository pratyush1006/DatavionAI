from .base import AttendanceRecordBaseSerializer
from .fields import WRITE_FIELDS


class AttendanceRecordCreateSerializer(
    AttendanceRecordBaseSerializer,
):
    class Meta(AttendanceRecordBaseSerializer.Meta):
        fields = WRITE_FIELDS
