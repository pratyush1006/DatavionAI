from __future__ import annotations

from apps.clinical.medications.services import (
    create_medication,
    delete_medication,
    restore_medication,
    update_medication,
)


class MedicationWorkflow:
    """Application orchestration boundary for Medication mutations."""

    @staticmethod
    def create(*, organization, validated_data, actor=None):
        return create_medication(
            organization=organization,
            validated_data=validated_data,
            actor=actor,
        )

    @staticmethod
    def update(*, organization, instance, validated_data, actor=None):
        return update_medication(
            organization=organization,
            instance=instance,
            validated_data=validated_data,
            actor=actor,
        )

    @staticmethod
    def delete(*, organization, instance, actor=None):
        return delete_medication(
            organization=organization,
            instance=instance,
            actor=actor,
        )

    @staticmethod
    def restore(*, organization, instance, actor=None):
        return restore_medication(
            organization=organization,
            instance=instance,
            actor=actor,
        )
