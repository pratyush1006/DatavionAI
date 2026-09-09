import pytest

from apps.telemedicine.constants import SessionStatus
from apps.telemedicine.services import SessionService


@pytest.mark.django_db
def test_session_lifecycle_is_enforced(session):
    SessionService.transition(
        session_id=session.session_id,
        target_status=SessionStatus.CONFIRMED,
        organization_id=session.organization_id,
    )
    session.refresh_from_db()
    assert session.status == SessionStatus.CONFIRMED

    SessionService.prepare(
        session_id=session.session_id,
        organization_id=session.organization_id,
    )
    session.refresh_from_db()
    assert session.status == SessionStatus.READY
    assert session.connection_id
    assert session.connection_url


@pytest.mark.django_db
def test_invalid_transition_is_rejected(session):
    with pytest.raises(ValueError):
        SessionService.transition(
            session_id=session.session_id,
            target_status=SessionStatus.COMPLETED,
            organization_id=session.organization_id,
        )
