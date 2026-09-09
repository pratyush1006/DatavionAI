from __future__ import annotations

"""Coding domain validation rules."""

from typing import Any

from .exceptions import CodingValidationError


def validate_code_value(value: str) -> str:
    """Validate and normalize a coding value."""

    normalized = value.strip().upper() if isinstance(value, str) else ""
    if not normalized:
        raise CodingValidationError("Code value is required.")
    return normalized


def validate_code_system(system: str) -> str:
    """Validate and normalize a supported code system."""

    normalized = system.strip().lower() if isinstance(system, str) else ""
    allowed = {"icd10cm", "icd10pcs", "cpt", "hcpcs", "modifier", "other"}

    if normalized not in allowed:
        raise CodingValidationError("Unsupported coding system.")

    return normalized


def validate_encounter_reference(reference: str) -> str:
    """Validate and normalize the source encounter reference."""

    normalized = reference.strip() if isinstance(reference, str) else ""
    if not normalized:
        raise CodingValidationError("Source encounter reference is required.")
    return normalized


def validate_documentation(documentation: Any) -> dict[str, Any]:
    """Validate Coding documentation as a JSON object."""

    if documentation is None:
        return {}

    if not isinstance(documentation, dict):
        raise CodingValidationError("Documentation must be a JSON object.")

    return documentation


__all__ = (
    "validate_code_system",
    "validate_code_value",
    "validate_documentation",
    "validate_encounter_reference",
)
