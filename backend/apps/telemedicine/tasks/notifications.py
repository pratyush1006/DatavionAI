import logging

logger = logging.getLogger(__name__)


def notify_session_change(*, session_id, event_name: str) -> None:
    logger.info(
        "telemedicine_notification",
        extra={"session_id": str(session_id), "event": event_name},
    )
