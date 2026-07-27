"""
Telemedicine session service.
"""

from __future__ import annotations

import uuid
from collections.abc import Mapping
from typing import Any

from django.db import transaction
from django.utils import timezone

from apps.platform.accounts.models import User
from apps.telemedicine.constants import SessionStatus
from apps.telemedicine.models import TelemedicineSession


class SessionService:
    """
    Application service responsible for telemedicine session operations.

    This service is the single entry point for all telemedicine session
    lifecycle operations and provides a centralized location for future
    business rules such as:

    - Notification dispatch
    - Screen sharing logs
    - Post-consultation note generation
    - Domain events
    - External integrations
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> TelemedicineSession:
        """
        Create a new telemedicine session.
        """

        session = TelemedicineSession(
            **validated_data,
        )

        if not session.session_id:
            session.session_id = str(uuid.uuid4())

        session.full_clean()

        session.save()

        return session

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: TelemedicineSession,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> TelemedicineSession:
        """
        Update an existing telemedicine session.
        """

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def start(
        *,
        instance: TelemedicineSession,
        performed_by: User | None = None,
    ) -> TelemedicineSession:
        """
        Start a telemedicine session.
        """

        instance.status = SessionStatus.IN_PROGRESS
        instance.actual_start = timezone.now()

        instance.save(
            update_fields=[
                "status",
                "actual_start",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def end(
        *,
        instance: TelemedicineSession,
        performed_by: User | None = None,
    ) -> TelemedicineSession:
        """
        End a telemedicine session.
        """

        instance.status = SessionStatus.COMPLETED
        instance.actual_end = timezone.now()

        instance.save(
            update_fields=[
                "status",
                "actual_end",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def cancel(
        *,
        instance: TelemedicineSession,
        performed_by: User | None = None,
    ) -> TelemedicineSession:
        """
        Cancel a telemedicine session.
        """

        instance.status = SessionStatus.CANCELLED

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[TelemedicineSession]:
        """
        Create multiple telemedicine sessions.
        """

        sessions: list[TelemedicineSession] = []

        for validated_data in validated_data_list:
            session = TelemedicineSession(
                **validated_data,
            )

            if not session.session_id:
                session.session_id = str(uuid.uuid4())

            session.full_clean()

            session.save()

            sessions.append(session)

        return sessions


create_session = SessionService.create
update_session = SessionService.update
start_session = SessionService.start
end_session = SessionService.end
cancel_session = SessionService.cancel


__all__ = [
    "SessionService",
    "cancel_session",
    "create_session",
    "end_session",
    "start_session",
    "update_session",
]
