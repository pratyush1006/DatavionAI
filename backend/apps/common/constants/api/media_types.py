"""
DatavionAI API Media Type Constants.

Centralized MIME types, content types, serialization formats, character
encodings, compression algorithms, and file extensions used throughout
the DatavionAI platform.

This module is framework-agnostic and should be the single source of truth
for content negotiation.

Design Principles
-----------------
- Immutable constants
- No business logic
- No HTTP headers
- No request/response keys
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Character Encodings
###############################################################################

CHARSET_UTF8: Final[str] = "utf-8"

CHARSET_UTF16: Final[str] = "utf-16"

CHARSET_UTF32: Final[str] = "utf-32"

CHARSET_ASCII: Final[str] = "ascii"

CHARSET_LATIN1: Final[str] = "latin-1"

DEFAULT_CHARSET: Final[str] = CHARSET_UTF8

SUPPORTED_CHARSETS: Final[tuple[str, ...]] = (
    CHARSET_UTF8,
    CHARSET_UTF16,
    CHARSET_UTF32,
    CHARSET_ASCII,
    CHARSET_LATIN1,
)

###############################################################################
# Content Types
###############################################################################

CONTENT_TYPE_JSON: Final[str] = "application/json"

CONTENT_TYPE_XML: Final[str] = "application/xml"

CONTENT_TYPE_YAML: Final[str] = "application/yaml"

CONTENT_TYPE_TEXT: Final[str] = "text/plain"

CONTENT_TYPE_HTML: Final[str] = "text/html"

CONTENT_TYPE_CSV: Final[str] = "text/csv"

CONTENT_TYPE_FORM: Final[str] = "application/x-www-form-urlencoded"

CONTENT_TYPE_MULTIPART: Final[str] = "multipart/form-data"

CONTENT_TYPE_BINARY: Final[str] = "application/octet-stream"

CONTENT_TYPE_PDF: Final[str] = "application/pdf"

CONTENT_TYPE_ZIP: Final[str] = "application/zip"

CONTENT_TYPE_GZIP: Final[str] = "application/gzip"

###############################################################################
# Image Types
###############################################################################

IMAGE_PNG: Final[str] = "image/png"

IMAGE_JPEG: Final[str] = "image/jpeg"

IMAGE_GIF: Final[str] = "image/gif"

IMAGE_WEBP: Final[str] = "image/webp"

IMAGE_BMP: Final[str] = "image/bmp"

IMAGE_SVG: Final[str] = "image/svg+xml"

###############################################################################
# Audio Types
###############################################################################

AUDIO_MP3: Final[str] = "audio/mpeg"

AUDIO_WAV: Final[str] = "audio/wav"

AUDIO_OGG: Final[str] = "audio/ogg"

AUDIO_AAC: Final[str] = "audio/aac"

###############################################################################
# Video Types
###############################################################################

VIDEO_MP4: Final[str] = "video/mp4"

VIDEO_WEBM: Final[str] = "video/webm"

VIDEO_MOV: Final[str] = "video/quicktime"

###############################################################################
# Office Documents
###############################################################################

APPLICATION_DOCX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

APPLICATION_XLSX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

APPLICATION_PPTX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
)

###############################################################################
# Serialization Formats
###############################################################################


class SerializationFormat(StrEnum):
    """
    Supported serialization formats.
    """

    JSON = "json"

    XML = "xml"

    YAML = "yaml"

    CSV = "csv"

    PDF = "pdf"


DEFAULT_SERIALIZATION_FORMAT: Final[str] = SerializationFormat.JSON.value

SUPPORTED_SERIALIZATION_FORMATS: Final[tuple[str, ...]] = (
    SerializationFormat.JSON.value,
    SerializationFormat.XML.value,
    SerializationFormat.YAML.value,
    SerializationFormat.CSV.value,
    SerializationFormat.PDF.value,
)

###############################################################################
# Compression
###############################################################################


class CompressionAlgorithm(StrEnum):
    """
    Supported compression algorithms.
    """

    IDENTITY = "identity"

    GZIP = "gzip"

    BROTLI = "br"

    DEFLATE = "deflate"


DEFAULT_COMPRESSION: Final[str] = CompressionAlgorithm.IDENTITY.value

SUPPORTED_COMPRESSION: Final[tuple[str, ...]] = (
    CompressionAlgorithm.IDENTITY.value,
    CompressionAlgorithm.GZIP.value,
    CompressionAlgorithm.BROTLI.value,
    CompressionAlgorithm.DEFLATE.value,
)

###############################################################################
# Transfer Encoding
###############################################################################

TRANSFER_ENCODING_CHUNKED: Final[str] = "chunked"

TRANSFER_ENCODING_IDENTITY: Final[str] = "identity"

###############################################################################
# File Extensions
###############################################################################

EXT_JSON: Final[str] = ".json"

EXT_XML: Final[str] = ".xml"

EXT_YAML: Final[str] = ".yaml"

EXT_CSV: Final[str] = ".csv"

EXT_PDF: Final[str] = ".pdf"

EXT_ZIP: Final[str] = ".zip"

EXT_TXT: Final[str] = ".txt"

###############################################################################
# Defaults
###############################################################################

DEFAULT_CONTENT_TYPE: Final[str] = CONTENT_TYPE_JSON

DEFAULT_ACCEPT: Final[str] = CONTENT_TYPE_JSON

DEFAULT_RESPONSE_CONTENT_TYPE: Final[str] = CONTENT_TYPE_JSON

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "SerializationFormat",
    "CompressionAlgorithm",
)
