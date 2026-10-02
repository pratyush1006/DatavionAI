from django.conf import settings


def imaging_health():
    return {
        "service": "imaging",
        "status": "ok",
        "redis_configured": bool(getattr(settings, "REDIS_URL", "")),
    }
