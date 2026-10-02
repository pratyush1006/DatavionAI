"""Document access application service."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.documents.models import Document, DocumentAccess


@transaction.atomic
def create_document_access(
    *,
    document: Document,
    user: Any,
    permission: str,
    expires_at: datetime | None = None,
) -> DocumentAccess:
    """Grant or reactivate one logical permission for a document."""
    if document.pk is None:
        raise ValidationError("Document must be persisted before granting access.")
    if user is None or getattr(user, "pk", None) is None:
        raise ValidationError("A persisted user is required.")
    permission = str(permission or "").strip()
    if not permission:
        raise ValidationError("Permission is required.")
    if expires_at is not None and expires_at <= timezone.now():
        raise ValidationError("Access expiration must be in the future.")
    locked_document = Document.objects.select_for_update().get(pk=document.pk)
    access = (
        DocumentAccess.objects.select_for_update()
        .filter(document=locked_document, user=user, permission=permission)
        .first()
    )
    if access is None:
        access = DocumentAccess(
            document=locked_document,
            user=user,
            permission=permission,
            expires_at=expires_at,
            is_active=True,
        )
    else:
        access.is_active = True
        access.expires_at = expires_at
    access.full_clean()
    access.save()
    return access


@transaction.atomic
def revoke_document_access(access: DocumentAccess) -> DocumentAccess:
    """Revoke access without deleting its history."""
    if access.pk is None:
        raise ValidationError("Access record must be persisted before revocation.")
    locked = (
        DocumentAccess.objects.select_for_update()
        .select_related("document")
        .get(pk=access.pk)
    )
    Document.objects.select_for_update().get(pk=locked.document_id)
    if locked.is_active:
        locked.is_active = False
        locked.save(update_fields=("is_active", "updated_at"))
    return locked


def check_document_access(
    *, document: Document, user: Any, permission: str | None = None
) -> bool:
    """Return whether current, non-expired access exists."""
    if document.pk is None or user is None or getattr(user, "pk", None) is None:
        return False
    qs = DocumentAccess.objects.filter(
        document_id=document.pk, user=user, is_active=True
    )
    if permission is not None:
        permission = str(permission).strip()
        if not permission:
            return False
        qs = qs.filter(permission=permission)
    now = timezone.now()
    return (
        qs.filter(expires_at__isnull=True).exists()
        or qs.filter(expires_at__gt=now).exists()
    )


__all__ = ("check_document_access", "create_document_access", "revoke_document_access")
