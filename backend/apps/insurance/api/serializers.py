from rest_framework import serializers


def serializer_for(model):
    class InsuranceSerializer(serializers.ModelSerializer):
        class Meta:
            model = None
            fields = "__all__"
            read_only_fields = (
                "id",
                "created_at",
                "updated_at",
                "is_deleted",
                "deleted_at",
                "deleted_by_id",
            )

    InsuranceSerializer.Meta.model = model
    InsuranceSerializer.__name__ = f"{model.__name__}Serializer"
    return InsuranceSerializer
