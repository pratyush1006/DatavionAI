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
from collections.abc import Mapping, Sequence
from typing import Any, TypeAlias

from rest_framework.renderers import BaseRenderer, JSONRenderer

JSONPrimitive: TypeAlias = str | int | float | bool | None
JSONValue: TypeAlias = JSONPrimitive | list["JSONValue"] | dict[str, "JSONValue"]

_ENCODING = "utf-8"
_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@")


def _json_bytes(data: JSONValue) -> bytes:
    """Serialize JSON-compatible data to UTF-8 bytes."""
    return json.dumps(
        data,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode(_ENCODING)


def _csv_value(value: object) -> object:
    """
    Protect exported CSV values against spreadsheet formula injection.
    """

    if isinstance(value, str) and value.startswith(_CSV_FORMULA_PREFIXES):
        return f"'{value}"

    return value


class DatavionJSONRenderer(JSONRenderer):
    """
    Default JSON renderer.

    Used for standard DatavionOS APIs.
    """


class DatavionCSVRenderer(BaseRenderer):
    """
    CSV export renderer.

    Used for:

    - Reports
    - Analytics exports
    - Bulk data extraction
    """

    media_type = "text/csv"
    format = "csv"
    charset = _ENCODING

    def render(
        self,
        data: object,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, object] | None = None,
    ) -> bytes:
        del accepted_media_type, renderer_context

        if not data:
            return b""

        output = io.StringIO(newline="")

        if isinstance(data, Sequence) and not isinstance(data, (str, bytes, bytearray)):
            rows = [row for row in data if isinstance(row, Mapping)]

            if not rows:
                return b""

            writer: Any = csv.DictWriter(
                output,
                fieldnames=[str(key) for key in rows[0].keys()],
            )

            writer.writeheader()

            for row in rows:
                writer.writerow(
                    {str(key): _csv_value(value) for key, value in row.items()},
                )

        elif isinstance(data, Mapping):
            csv_writer = csv.writer(output)

            csv_writer.writerow(list(data.keys()))
            csv_writer.writerow(
                [_csv_value(value) for value in data.values()],
            )

        else:
            csv_writer = csv.writer(output)
            csv_writer.writerow([_csv_value(data)])

        return output.getvalue().encode(_ENCODING)


class DatavionFHIRRenderer(BaseRenderer):
    """
    FHIR JSON renderer.

    Intended for healthcare interoperability.

    Actual FHIR resource transformation belongs
    to healthcare applications.
    """

    media_type = "application/fhir+json"
    format = "fhir"
    charset = _ENCODING

    def render(
        self,
        data: JSONValue,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, object] | None = None,
    ) -> bytes:
        del accepted_media_type, renderer_context
        return _json_bytes(data)


class DatavionHL7Renderer(BaseRenderer):
    """
    HL7 message renderer.

    Provides transport representation only.

    HL7 generation/parsing belongs to
    integration modules.
    """

    media_type = "application/hl7-v2"
    format = "hl7"
    charset = _ENCODING

    def render(
        self,
        data: str | JSONValue,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, object] | None = None,
    ) -> bytes:
        del accepted_media_type, renderer_context

        if isinstance(data, str):
            return data.encode(_ENCODING)

        return _json_bytes(data)


class DatavionAIResponseRenderer(BaseRenderer):
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
    charset = _ENCODING

    def render(
        self,
        data: JSONValue,
        accepted_media_type: str | None = None,
        renderer_context: Mapping[str, object] | None = None,
    ) -> bytes:
        del accepted_media_type, renderer_context

        return _json_bytes(
            {
                "type": "ai_response",
                "data": data,
            },
        )


__all__ = (
    "DatavionJSONRenderer",
    "DatavionCSVRenderer",
    "DatavionFHIRRenderer",
    "DatavionHL7Renderer",
    "DatavionAIResponseRenderer",
)
