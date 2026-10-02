import logging

logger = logging.getLogger(__name__)


def process_recording(*, recording_id) -> None:
    logger.info(
        "telemedicine_recording_processing", extra={"recording_id": str(recording_id)}
    )
