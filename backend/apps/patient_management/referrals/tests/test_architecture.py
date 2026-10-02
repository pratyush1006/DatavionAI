"""Static architecture tests for Patient Referrals."""

from __future__ import annotations


def test_canonical_patient_reference() -> None:
    """Ensure the referral model uses the canonical Patient."""

    from apps.patient_management.referrals.models.referral import PatientReferral

    assert (
        PatientReferral._meta.get_field("patient").remote_field.model.__module__
        == "apps.patient_management.patients.models"
    )


def test_referral_lifecycle_is_explicit() -> None:
    """Ensure lifecycle transitions are centrally defined."""

    from apps.patient_management.referrals.constants import REFERRAL_TRANSITIONS

    assert REFERRAL_TRANSITIONS


def test_api_mutations_are_workflow_orchestrated() -> None:
    """Ensure API mutation endpoints invoke workflows instead of services."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    for workflow_name in (
        "ReferralCreationWorkflow",
        "ReferralUpdateWorkflow",
        "ReferralDeletionWorkflow",
        "ReferralLifecycleWorkflow",
        "ReferralRestoreWorkflow",
    ):
        assert workflow_name in text

    assert "PatientReferralService" not in text


def test_filter_layer_is_wired_to_list_api() -> None:
    """Ensure the declared referral filter is actually used by the API."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "PatientReferralFilter(" in text


def test_lifecycle_service_locks_referral() -> None:
    """Ensure concurrent lifecycle mutations serialize on the referral row."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "services" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "select_for_update()" in text


__all__ = ()


def test_mutating_services_lock_rows() -> None:
    """Ensure concurrent update, delete, and restore operations are serialized."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "services" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert text.count("select_for_update()") >= 4


def test_delete_endpoint_returns_content_status() -> None:
    """Ensure DELETE does not return a body with HTTP 204."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "HTTP_204_NO_CONTENT" not in text


def test_update_rejects_protected_fields() -> None:
    """Ensure mutable updates cannot silently mutate protected fields."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "services" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "cannot be changed by referral update" in text


def test_create_handles_duplicate_referral_numbers() -> None:
    """Ensure concurrent duplicate numbers are converted to domain validation."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "services" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "IntegrityError" in text
    assert "already exists in the organization" in text


def test_update_uses_explicit_mutable_field_allowlist() -> None:
    """Ensure updates cannot mutate arbitrary model attributes."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "services" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "MUTABLE_FIELDS" in text
    assert "field not in cls.MUTABLE_FIELDS" in text


def test_detail_api_maps_missing_referrals_to_404() -> None:
    """Ensure direct selector misses are never exposed as server errors."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "HTTP_404_NOT_FOUND" in text
    assert "ObjectDoesNotExist" in text


def test_list_api_enforces_domain_policy() -> None:
    """Ensure collection reads pass through the domain policy layer."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "PatientReferralPolicy.can_list(" in text


def test_transition_api_maps_missing_referrals_to_404() -> None:
    """Ensure transition requests cannot expose selector misses as 500s."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    transition_start = text.index("class PatientReferralTransitionAPIView")
    transition_source = text[transition_start:]

    assert "except ObjectDoesNotExist:" in transition_source
    assert "patient_referral_not_found" in transition_source
    assert "HTTP_404_NOT_FOUND" in transition_source


def test_request_context_does_not_fallback_to_first_organization() -> None:
    """Ensure ambiguous multi-organization context is rejected explicitly."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "api" / "views" / "referral.py"
    text = source.read_text(encoding="utf-8")

    assert "organization_roles" not in text
    assert 'raise RuntimeError("Organization context is required.")' in text


def test_obsolete_workflow_requests_module_is_not_embedded() -> None:
    """Ensure superseded workflow request contracts cannot be reintroduced."""

    from pathlib import Path

    source = Path(__file__).resolve().parents[1] / "workflows" / "requests.py"

    assert not source.exists()
