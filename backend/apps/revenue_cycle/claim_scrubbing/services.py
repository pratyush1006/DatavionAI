"""Transactional claim scrubbing services."""

from __future__ import annotations

from django.db import transaction
from django.utils import timezone

from apps.revenue_cycle.claim_scrubbing.constants import ScrubStatus
from apps.revenue_cycle.claim_scrubbing.events import (
    claim_scrub_completed,
    claim_scrub_created,
)
from apps.revenue_cycle.claim_scrubbing.exceptions import InvalidScrubTransition
from apps.revenue_cycle.claim_scrubbing.models import ClaimScrub, ClaimScrubFinding
from apps.revenue_cycle.claim_scrubbing.selectors import (
    get_scrub_for_update,
    list_active_rules,
)

_ALLOWED = {
    ScrubStatus.PENDING: {ScrubStatus.RUNNING},
    ScrubStatus.RUNNING: {ScrubStatus.PASSED, ScrubStatus.FAILED},
    ScrubStatus.FAILED: {ScrubStatus.OVERRIDDEN, ScrubStatus.PENDING},
    ScrubStatus.PASSED: set(),
    ScrubStatus.OVERRIDDEN: set(),
}


def _schedule(event):
    """Publish a domain event after the surrounding transaction commits."""

    transaction.on_commit(event)


def create_scrub(
    *,
    organization,
    patient,
    claim_reference: str,
    idempotency_key: str,
    input_snapshot: dict,
    user,
):
    """Create an idempotent claim scrub aggregate."""

    with transaction.atomic():
        scrub, created = ClaimScrub.objects.get_or_create(
            organization=organization,
            idempotency_key=idempotency_key,
            defaults={
                "patient": patient,
                "claim_reference": claim_reference,
                "input_snapshot": input_snapshot,
                "created_by": user,
            },
        )
        if created:
            _schedule(
                lambda: claim_scrub_created(
                    scrub_id=str(scrub.id), organization_id=str(organization.id)
                )
            )
        return scrub, created


def run_scrub(*, organization_id: str, tenant_id: str, scrub_id: str) -> ClaimScrub:
    """Execute deterministic active rules under a row lock."""

    with transaction.atomic():
        scrub = get_scrub_for_update(
            organization_id=organization_id,
            tenant_id=tenant_id,
            scrub_id=scrub_id,
        )
        if scrub.status != ScrubStatus.PENDING:
            raise InvalidScrubTransition("Only pending scrubs can be started.")
        scrub.status = ScrubStatus.RUNNING
        scrub.started_at = timezone.now()
        scrub.save(update_fields=("status", "started_at", "updated_at"))
        scrub.findings.all().delete()
        blocking = False
        for rule in list_active_rules(
            organization_id=organization_id, tenant_id=tenant_id
        ):
            value = scrub.input_snapshot.get(rule.field_name)
            message = _evaluate_rule(
                rule=rule, value=value, snapshot=scrub.input_snapshot
            )
            if message:
                ClaimScrubFinding.objects.create(
                    scrub=scrub,
                    rule=rule,
                    field_name=rule.field_name,
                    message=message,
                    severity=rule.severity,
                    is_blocking=rule.is_blocking,
                    observed_value=value,
                )
                blocking = blocking or rule.is_blocking
        scrub.status = ScrubStatus.FAILED if blocking else ScrubStatus.PASSED
        scrub.completed_at = timezone.now()
        scrub.save(update_fields=("status", "completed_at", "updated_at"))
        _schedule(
            lambda: claim_scrub_completed(
                scrub_id=str(scrub.id),
                organization_id=str(scrub.organization_id),
                status=scrub.status,
            )
        )
        return scrub


def _evaluate_rule(*, rule, value, snapshot: dict) -> str | None:
    """Evaluate one deterministic scrub rule against the snapshot."""

    if rule.rule_type == "required" and value in (None, "", []):
        return rule.configuration.get("message", f"{rule.field_name} is required.")
    if rule.rule_type == "format" and value not in (None, ""):
        expected = rule.configuration.get("equals")
        if expected is not None and value != expected:
            return rule.configuration.get(
                "message", f"{rule.field_name} has an invalid value."
            )
    if rule.rule_type == "range" and value is not None:
        minimum = rule.configuration.get("min")
        maximum = rule.configuration.get("max")
        if minimum is not None and value < minimum:
            return rule.configuration.get(
                "message", f"{rule.field_name} is below the permitted range."
            )
        if maximum is not None and value > maximum:
            return rule.configuration.get(
                "message", f"{rule.field_name} exceeds the permitted range."
            )
    if rule.rule_type == "codeset" and value not in (None, ""):
        allowed = rule.configuration.get("allowed", [])
        if allowed and value not in allowed:
            return rule.configuration.get(
                "message", f"{rule.field_name} is not an allowed code."
            )
    if rule.rule_type == "consistency":
        other_field = rule.configuration.get("other_field")
        if other_field and value != snapshot.get(other_field):
            return rule.configuration.get(
                "message", f"{rule.field_name} is inconsistent with {other_field}."
            )
    return None


def override_scrub(
    *, organization_id: str, tenant_id: str, scrub_id: str, reason: str
) -> ClaimScrub:
    """Override a failed scrub with an auditable reason."""

    with transaction.atomic():
        scrub = get_scrub_for_update(
            organization_id=organization_id, tenant_id=tenant_id, scrub_id=scrub_id
        )
        if scrub.status != ScrubStatus.FAILED:
            raise InvalidScrubTransition("Only failed scrubs can be overridden.")
        scrub.status = ScrubStatus.OVERRIDDEN
        scrub.override_reason = reason.strip()
        scrub.save(update_fields=("status", "override_reason", "updated_at"))
        return scrub


__all__ = ("create_scrub", "run_scrub", "override_scrub")
