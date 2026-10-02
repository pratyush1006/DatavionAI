from rest_framework import serializers


class NonBlankTrimmedCharField(serializers.CharField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data).strip()
        if not value:
            raise serializers.ValidationError("This field cannot be blank.")
        return value
