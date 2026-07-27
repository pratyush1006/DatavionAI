"""
Reusable API renderers for the DatavionOS framework.

Provides platform-level response renderers:

- JSON API responses
- CSV exports
- Healthcare interoperability formats
- AI response formats

Business transformation logic belongs to
feature applications.
"""

from __future__ import annotations

import csv
import io
import json
from typing import Any

from rest_framework.renderers import BaseRenderer, JSONRenderer


class DatavionJSONRenderer(
    JSONRenderer,
):
    """
    Default JSON renderer.

    Used for standard DatavionOS APIs.
    """


class DatavionCSVRenderer(
    BaseRenderer,
):
    """
    CSV export renderer.

    Used for:

    - Reports
    - Analytics exports
    - Bulk data extraction
    """

    media_type = "text/csv"

    format = "csv"

    def render(
        self,
        data: Any,
        accepted_media_type=None,
        renderer_context=None,
    ) -> bytes:

        if not data:
            return b""

        output = io.StringIO()

        if isinstance(data, list):
            writer = csv.DictWriter(
                output,
                fieldnames=data[0].keys(),
            )

            writer.writeheader()

            writer.writerows(
                data,
            )

        else:
            writer = csv.writer(
                output,
            )

            writer.writerow(
                data.keys(),
            )

            writer.writerow(
                data.values(),
            )

        return output.getvalue().encode(
            "utf-8",
        )


class DatavionFHIRRenderer(
    BaseRenderer,
):
    """
    FHIR JSON renderer.

    Intended for healthcare interoperability:

    - Patient resources
    - Encounter resources
    - Observation resources
    - Medication resources

    Actual FHIR mapping belongs to
    healthcare applications.
    """

    media_type = "application/fhir+json"

    format = "fhir"

    def render(
        self,
        data: Any,
        accepted_media_type=None,
        renderer_context=None,
    ) -> bytes:

        return json.dumps(
            data,
            default=str,
        ).encode(
            "utf-8",
        )


class DatavionHL7Renderer(
    BaseRenderer,
):
    """
    HL7 message renderer.

    Provides transport representation only.

    HL7 generation/parsing logic belongs
    to integration modules.
    """

    media_type = "application/hl7-v2"

    format = "hl7"

    def render(
        self,
        data: Any,
        accepted_media_type=None,
        renderer_context=None,
    ) -> bytes:

        if isinstance(
            data,
            str,
        ):
            return data.encode(
                "utf-8",
            )

        return json.dumps(
            data,
            default=str,
        ).encode(
            "utf-8",
        )


class DatavionAIResponseRenderer(
    BaseRenderer,
):
    """
    AI response renderer.

    Used for:

    - AI assistant responses
    - Agent outputs
    - RAG responses
    - Model metadata
    """

    media_type = "application/vnd.datavion.ai+json"

    format = "ai"

    def render(
        self,
        data: Any,
        accepted_media_type=None,
        renderer_context=None,
    ) -> bytes:

        payload = {
            "type": "ai_response",
            "data": data,
        }

        return json.dumps(
            payload,
            default=str,
        ).encode(
            "utf-8",
        )


__all__ = (
    "DatavionJSONRenderer",
    "DatavionCSVRenderer",
    "DatavionFHIRRenderer",
    "DatavionHL7Renderer",
    "DatavionAIResponseRenderer",
)
