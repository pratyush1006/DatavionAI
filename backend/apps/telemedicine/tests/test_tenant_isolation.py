import pytest

from apps.telemedicine.selectors import SessionSelector


@pytest.mark.django_db
def test_session_selector_is_tenant_scoped(session, other_organization):
    assert (
        SessionSelector.queryset(organization_id=other_organization.pk)
        .filter(pk=session.pk)
        .exists()
        is False
    )
