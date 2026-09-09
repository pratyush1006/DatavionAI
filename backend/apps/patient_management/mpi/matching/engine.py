"""
Deterministic, explainable MPI identity matching engine.

The engine operates on supplied identity attributes and does not mutate
Patient or MPI records. Persistence, authorization, and merge decisions
remain in the service and workflow layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from apps.patient_management.mpi.constants import (
    MPI_MATCH_CLASS_AUTO,
    MPI_MATCH_CLASS_NO_MATCH,
    MPI_MATCH_CLASS_REVIEW,
    MPI_MATCH_THRESHOLD,
    MPI_REVIEW_THRESHOLD,
)


@dataclass(frozen=True, slots=True)
class MPIMatchResult:
    """Explain the score and classification produced for two identities."""

    score: Decimal
    classification: str
    evidence: dict[str, Any]


def _normalize(value: Any) -> str:
    """Normalize a supplied identity value for deterministic comparison."""

    return "".join(str(value or "").casefold().split())


def calculate_match(
    *,
    left: dict[str, Any],
    right: dict[str, Any],
) -> MPIMatchResult:
    """Calculate an absolute weighted identity match score.

    Missing attributes do not increase the score. This prevents a pair with
    only one or two matching fields from being promoted to a false 1.0000
    match merely because other attributes were absent.
    """

    evidence: dict[str, Any] = {}
    weighted_total = Decimal("0")
    total_weight = Decimal("1.00")

    fields = (
        ("first_name", Decimal("0.20")),
        ("last_name", Decimal("0.20")),
        ("date_of_birth", Decimal("0.25")),
        ("phone", Decimal("0.15")),
        ("email", Decimal("0.10")),
        ("government_identifier", Decimal("0.10")),
    )

    for field, weight in fields:
        left_value = _normalize(left.get(field))
        right_value = _normalize(right.get(field))
        present = bool(left_value and right_value)
        matched = present and left_value == right_value
        evidence[field] = {
            "present_on_both": present,
            "matched": matched,
        }
        if matched:
            weighted_total += weight

    score = (weighted_total / total_weight).quantize(Decimal("0.0001"))

    if score >= Decimal(str(MPI_MATCH_THRESHOLD)):
        classification = MPI_MATCH_CLASS_AUTO
    elif score >= Decimal(str(MPI_REVIEW_THRESHOLD)):
        classification = MPI_MATCH_CLASS_REVIEW
    else:
        classification = MPI_MATCH_CLASS_NO_MATCH

    evidence["classification"] = classification
    evidence["thresholds"] = {
        "match": str(MPI_MATCH_THRESHOLD),
        "review": str(MPI_REVIEW_THRESHOLD),
    }

    return MPIMatchResult(
        score=score,
        classification=classification,
        evidence=evidence,
    )


__all__ = (
    "MPIMatchResult",
    "calculate_match",
)
