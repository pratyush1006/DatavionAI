from .base import AttendanceRecordBaseSerializer
from .fields import UPDATE_FIELDS


class AttendanceRecordUpdateSerializer(
    AttendanceRecordBaseSerializer,
):
    class Meta(AttendanceRecordBaseSerializer.Meta):
        fields = UPDATE_FIELDS
