import pytest

from apps.core.workflows import WorkflowContext, workflow_registry
from apps.telemedicine.constants import SessionStatus


@pytest.mark.django_db
def test_telemedicine_workflow_uses_core_kernel(session, user):
    context = WorkflowContext.create(
        tenant_id=session.organization.tenant_id,
        actor_id=user.pk,
        workflow_name="telemedicine.session.confirm",
    )
    workflow_class = workflow_registry.get("telemedicine.session.confirm")
    result = workflow_class(
        payload={
            "session_id": session.session_id,
            "organization_id": session.organization_id,
        }
    ).execute(context=context)
    assert result.success is True
    session.refresh_from_db()
    assert session.status == SessionStatus.CONFIRMED
