"""
HL7 v2 message builders.

Produces minimal, well-formed HL7 v2 pipes-and-hats segments for the most
common clinical interfaces (ADT^A01 admit, ORU^R01 observation result).
Field separators follow the HL7 standard (| component ^ repetition ~).
"""

from __future__ import annotations

from datetime import datetime

FIELD_SEP = "|"
COMPONENT_SEP = "^"
REPETITION_SEP = "~"
ESCAPE_CHAR = "\\"
SUBCOMPONENT_SEP = "&"

MESSAGE_CONTROL_ID = "DATV{ts}"


def _now() -> str:
    return datetime.now().strftime("%Y%m%d%H%M%S")


def _escape(value: str) -> str:
    return (
        value.replace(ESCAPE_CHAR, f"{ESCAPE_CHAR}{ESCAPE_CHAR}")
        .replace(FIELD_SEP, "")
        .replace(COMPONENT_SEP, "")
    )


def build_msh(
    *,
    sending_app: str,
    sending_facility: str,
    message_type: str,
) -> str:
    """Build an HL7 MSH header segment."""

    control_id = MESSAGE_CONTROL_ID.format(ts=_now())
    encoding = (
        f"{FIELD_SEP}{COMPONENT_SEP}{REPETITION_SEP}{ESCAPE_CHAR}{SUBCOMPONENT_SEP}"
    )

    return FIELD_SEP.join(
        [
            "MSH",
            encoding,
            sending_app,
            sending_facility,
            "D ATVION",
            "D ATVION",
            _now(),
            "",
            message_type,
            control_id,
            "P",
            "2.5",
        ]
    )


def build_adt_a01(
    *,
    sending_app: str,
    sending_facility: str,
    patient_id: str,
    patient_name: str,
    gender: str,
) -> str:
    """Build an ADT^A01 (patient admit) message."""

    msh = build_msh(
        sending_app=sending_app,
        sending_facility=sending_facility,
        message_type="ADT^A01",
    )
    pid = FIELD_SEP.join(
        [
            "PID",
            "1",
            patient_id,
            patient_id,
            _escape(patient_name),
            "",
            gender,
        ]
    )
    return "\r".join([msh, pid])


def build_oru_r01(
    *,
    sending_app: str,
    sending_facility: str,
    patient_id: str,
    observation_id: str,
    value: str,
) -> str:
    """Build an ORU^R01 (observation result) message."""

    msh = build_msh(
        sending_app=sending_app,
        sending_facility=sending_facility,
        message_type="ORU^R01",
    )
    pid = FIELD_SEP.join(["PID", "1", patient_id, patient_id])
    obr = FIELD_SEP.join(["OBR", "1", observation_id])
    obx = FIELD_SEP.join(
        [
            "OBX",
            "1",
            "ST",
            observation_id,
            "",
            _escape(value),
        ]
    )
    return "\r".join([msh, pid, obr, obx])


__all__ = [
    "build_adt_a01",
    "build_oru_r01",
]
