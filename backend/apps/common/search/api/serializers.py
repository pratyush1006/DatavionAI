"""
DatavionOS Search API Serializers.
"""

from __future__ import annotations

from rest_framework import serializers


class SearchRequestSerializer(
    serializers.Serializer,
):
    """
    Unified search request.
    """

    query = serializers.CharField(
        required=True,
    )

    mode = serializers.ChoiceField(
        choices=(
            "keyword",
            "semantic",
            "hybrid",
        ),
        default="hybrid",
    )

    provider = serializers.CharField(
        default="pgvector",
        required=False,
    )

    embedding_provider = serializers.CharField(
        default="local",
        required=False,
    )

    tenant_id = serializers.CharField(
        required=False,
        allow_null=True,
    )

    organization_id = serializers.CharField(
        required=False,
        allow_null=True,
    )

    patient_id = serializers.CharField(
        required=False,
        allow_null=True,
    )

    top_k = serializers.IntegerField(
        default=10,
        required=False,
    )

    filters = serializers.JSONField(
        required=False,
        allow_null=True,
    )


class SearchResponseSerializer(
    serializers.Serializer,
):
    """
    Search response serializer.
    """

    items = serializers.ListField()

    total = serializers.IntegerField()

    pagination = serializers.DictField()

    provider = serializers.CharField()

    mode = serializers.CharField()

    metadata = serializers.DictField()


__all__ = (
    "SearchRequestSerializer",
    "SearchResponseSerializer",
)
