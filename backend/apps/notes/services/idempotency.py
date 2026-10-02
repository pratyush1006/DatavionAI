from __future__ import annotations

import hashlib
import json

from apps.notes.models import NoteIdempotencyKey


def request_hash(payload: dict) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


def get_or_create(*, organization, scope, key, payload):
    digest = request_hash(payload)
    obj, created = NoteIdempotencyKey.objects.get_or_create(
        organization=organization,
        scope=scope,
        idempotency_key=key,
        defaults={"request_hash": digest},
    )
    if not created and obj.request_hash != digest:
        raise ValueError("Idempotency key was reused with a different request payload.")
    return obj, created
