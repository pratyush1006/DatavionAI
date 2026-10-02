from __future__ import annotations

from celery import shared_task
from django.db import OperationalError

from apps.telemedicine.services import SessionService


@shared_task(
    bind=True,
    autoretry_for=(OperationalError,),
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    max_retries=3,
)
def provision_session_room(
    self,
    *,
    session_id: str,
    organization_id: str,
) -> dict[str, str | None]:
    """Provision a video room through the canonical session service.

    Provider and business logic remain in SessionService.prepare().
    Transient database operational failures are retried; domain validation
    and provider configuration errors are intentionally not retried.
    """
    session = SessionService.prepare(
        session_id=session_id,
        organization_id=organization_id,
    )
    return {
        "session_id": str(session.session_id),
        "organization_id": str(session.organization_id),
        "status": str(session.status),
        "connection_id": session.connection_id,
        "connection_url": session.connection_url,
        "provider_name": session.provider_name,
    }
