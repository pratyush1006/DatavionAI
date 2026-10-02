"""OpenAPI behavior for APIViews without an explicit DRF serializer."""

from __future__ import annotations

import re

from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_serializer_context
from drf_spectacular.types import OpenApiTypes
from rest_framework.generics import GenericAPIView
from rest_framework.serializers import Serializer as DRFSerializer
from rest_framework.views import APIView


class DatavionAutoSchema(AutoSchema):
    """Keep serializer-less JSON APIs in the schema as free-form objects.

    Explicit serializer declarations and ``extend_schema`` annotations retain
    their normal, strongly typed output. For older APIViews that already return
    JSON but have no serializer metadata, a free-form object accurately records
    the media type and keeps the operation available to API clients.
    """

    def get_operation_id(self):
        """Make operation identifiers deterministic when view names collide."""
        base = super().get_operation_id()
        path_identity = re.sub(r"\{([^}]+)\}", r"by_\1", self.path.strip("/"))
        path_identity = re.sub(r"[^A-Za-z0-9]+", "_", path_identity).strip("_")
        return f"{base}_{path_identity}"

    def _get_serializer(self):
        view = self.view
        context = build_serializer_context(view)
        serializer_class = None

        if isinstance(view, GenericAPIView):
            try:
                serializer_class = view.get_serializer_class()
            except Exception:
                return OpenApiTypes.OBJECT
        elif isinstance(view, APIView):
            get_serializer_class = getattr(view, "get_serializer_class", None)
            if callable(get_serializer_class):
                try:
                    serializer_class = get_serializer_class()
                except Exception:
                    return OpenApiTypes.OBJECT
            else:
                serializer_class = getattr(view, "serializer_class", None)

            if serializer_class is None:
                get_serializer = getattr(view, "get_serializer", None)
                if not callable(get_serializer):
                    return OpenApiTypes.OBJECT
                try:
                    get_serializer(context=context)
                except Exception:
                    return OpenApiTypes.OBJECT
                return super()._get_serializer() or OpenApiTypes.OBJECT
        else:
            return super()._get_serializer() or OpenApiTypes.OBJECT

        if serializer_class is None:
            return OpenApiTypes.OBJECT
        if serializer_class is DRFSerializer:
            return OpenApiTypes.OBJECT

        try:
            serializer = serializer_class(context=context)
            getattr(serializer, "fields", None)
        except Exception:
            return OpenApiTypes.OBJECT

        return super()._get_serializer() or OpenApiTypes.OBJECT


__all__ = ("DatavionAutoSchema",)
