"""
Organization summary serializer.
"""

from rest_framework import serializers

from apps.organizations.models import Organization


class OrganizationSummarySerializer(
    serializers.ModelSerializer,
):
    class Meta:
        model = Organization

        fields = (
            "id",
            "uuid",
            "name",
            "code",
            "organization_type",
        )

        read_only_fields = fields
