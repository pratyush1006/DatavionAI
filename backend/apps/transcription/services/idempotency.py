from __future__ import annotations

import hashlib
import json

from apps.transcription.models import TranscriptionIdempotencyKey


def request_hash(payload: dict) -> str:
    raw = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), default=str
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def get_or_create(*, organization, scope: str, key: str, payload: dict):
    digest = request_hash(payload)
    obj, created = TranscriptionIdempotencyKey.objects.get_or_create(
        organization=organization,
        scope=scope,
        idempotency_key=key,
        defaults={"request_hash": digest},
    )
    if not created and obj.request_hash != digest:
        raise ValueError("Idempotency key was reused with a different request payload.")
    return obj, created
