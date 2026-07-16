"""
Tests for laboratory order services.
"""

from __future__ import annotations

from decimal import Decimal

from django.utils import timezone

from apps.clinical.laboratories.constants import (
    LaboratoryCategory,
    LaboratoryOrderStatus,
    LaboratoryPriority,
    LaboratoryResultFlag,
    LaboratoryResultStatus,
    LaboratorySpecimenType,
    LaboratoryTestStatus,
)
from apps.clinical.laboratories.services.laboratory_order import (
    cancel_laboratory_order,
    create_laboratory_order,
    update_laboratory_order,
)
from apps.clinical.laboratories.services.laboratory_result import (
    amend_laboratory_result,
    create_laboratory_result,
    invalidate_laboratory_result,
    record_laboratory_result,
    update_laboratory_result,
    verify_laboratory_result,
)
from apps.clinical.laboratories.services.laboratory_test import (
    cancel_laboratory_test,
    complete_laboratory_test,
    create_laboratory_test,
    start_laboratory_test,
    update_laboratory_test,
)
from apps.common.tests.base import BaseTestCase
from apps.core.exceptions import InvalidWorkflowTransition


class LaboratoryOrderServiceTestCase(BaseTestCase):
    """
    Test cases for laboratory order services.
    """

    def setUp(self) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

    def test_create_laboratory_order(self) -> None:
        """
        Laboratory order should be created successfully.
        """

        patient = self.create_patient()
        provider = self.create_provider()
        encounter = self.create_encounter(
            patient=patient,
            provider=provider,
        )

        order = create_laboratory_order(
            validated_data={
                "organization": self.organization,
                "patient": patient,
                "provider": provider,
                "encounter": encounter,
                "order_number": "LAB999999",
                "priority": LaboratoryPriority.ROUTINE,
                "status": LaboratoryOrderStatus.ORDERED,
                "ordered_at": timezone.now(),
                "clinical_notes": "",
                "instructions": "",
            },
        )

        self.assertEqual(
            order.order_number,
            "LAB999999",
        )

    def test_update_priority(self) -> None:
        """
        Priority should be updated.
        """

        update_laboratory_order(
            instance=self.order,
            validated_data={
                "priority": LaboratoryPriority.STAT,
            },
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.priority,
            LaboratoryPriority.STAT,
        )

    def test_update_clinical_notes(self) -> None:
        """
        Clinical notes should be updated.
        """

        update_laboratory_order(
            instance=self.order,
            validated_data={
                "clinical_notes": "Updated notes",
            },
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.clinical_notes,
            "Updated notes",
        )

    def test_update_instructions(self) -> None:
        """
        Instructions should be updated.
        """

        update_laboratory_order(
            instance=self.order,
            validated_data={
                "instructions": "Fasting sample",
            },
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.instructions,
            "Fasting sample",
        )

    def test_update_multiple_fields(self) -> None:
        """
        Multiple editable fields should be updated.
        """

        update_laboratory_order(
            instance=self.order,
            validated_data={
                "priority": LaboratoryPriority.URGENT,
                "clinical_notes": "Urgent case",
                "instructions": "Immediate processing",
            },
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.priority,
            LaboratoryPriority.URGENT,
        )

        self.assertEqual(
            self.order.clinical_notes,
            "Urgent case",
        )

        self.assertEqual(
            self.order.instructions,
            "Immediate processing",
        )

    def test_update_completed_order_raises_exception(self) -> None:
        """
        Completed orders cannot be updated.
        """

        self.order.status = LaboratoryOrderStatus.COMPLETED
        self.order.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_order(
                instance=self.order,
                validated_data={
                    "priority": LaboratoryPriority.STAT,
                },
            )

    def test_update_cancelled_order_raises_exception(self) -> None:
        """
        Cancelled orders cannot be updated.
        """

        self.order.status = LaboratoryOrderStatus.CANCELLED
        self.order.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_order(
                instance=self.order,
                validated_data={
                    "priority": LaboratoryPriority.STAT,
                },
            )

    def test_cancel_order(self) -> None:
        """
        Order should be cancelled.
        """

        cancel_laboratory_order(
            instance=self.order,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            LaboratoryOrderStatus.CANCELLED,
        )

    def test_cancel_already_cancelled_order(self) -> None:
        """
        Cancelling an already cancelled order should be idempotent.
        """

        self.order.status = LaboratoryOrderStatus.CANCELLED
        self.order.save()

        order = cancel_laboratory_order(
            instance=self.order,
        )

        self.assertEqual(
            order.status,
            LaboratoryOrderStatus.CANCELLED,
        )

    def test_cancel_completed_order_raises_exception(self) -> None:
        """
        Completed orders cannot be cancelled.
        """

        self.order.status = LaboratoryOrderStatus.COMPLETED
        self.order.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            cancel_laboratory_order(
                instance=self.order,
            )


###############################################################################
# Laboratory Test
###############################################################################


class LaboratoryTestServiceTestCase(BaseTestCase):
    """
    Test cases for laboratory test services.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

        self.laboratory_test = self.create_laboratory_test(
            laboratory_order=self.order,
        )

    ###########################################################################
    # Create
    ###########################################################################

    def test_create_laboratory_test(
        self,
    ) -> None:
        """
        Laboratory test should be created successfully.
        """

        laboratory_test = create_laboratory_test(
            validated_data={
                "laboratory_order": self.order,
                "code": "CBC001",
                "name": "Complete Blood Count",
                "category": LaboratoryCategory.HEMATOLOGY,
                "specimen_type": LaboratorySpecimenType.BLOOD,
                "priority": LaboratoryPriority.ROUTINE,
                "display_order": 2,
                "status": LaboratoryTestStatus.PENDING,
                "notes": "",
            },
        )

        self.assertEqual(
            laboratory_test.code,
            "CBC001",
        )

    ###########################################################################
    # Update
    ###########################################################################

    def test_update_name(
        self,
    ) -> None:
        """
        Name should be updated.
        """

        update_laboratory_test(
            instance=self.laboratory_test,
            validated_data={
                "name": "Blood Sugar",
            },
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.name,
            "Blood Sugar",
        )

    def test_update_priority(
        self,
    ) -> None:
        """
        Priority should be updated.
        """

        update_laboratory_test(
            instance=self.laboratory_test,
            validated_data={
                "priority": LaboratoryPriority.STAT,
            },
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.priority,
            LaboratoryPriority.STAT,
        )

    def test_update_notes(
        self,
    ) -> None:
        """
        Notes should be updated.
        """

        update_laboratory_test(
            instance=self.laboratory_test,
            validated_data={
                "notes": "Updated notes",
            },
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.notes,
            "Updated notes",
        )

    def test_update_display_order(
        self,
    ) -> None:
        """
        Display order should be updated.
        """

        update_laboratory_test(
            instance=self.laboratory_test,
            validated_data={
                "display_order": 5,
            },
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.display_order,
            5,
        )

    def test_update_multiple_fields(
        self,
    ) -> None:
        """
        Multiple editable fields should be updated.
        """

        update_laboratory_test(
            instance=self.laboratory_test,
            validated_data={
                "name": "Lipid Profile",
                "priority": LaboratoryPriority.URGENT,
                "display_order": 3,
                "notes": "Urgent sample",
            },
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.name,
            "Lipid Profile",
        )

        self.assertEqual(
            self.laboratory_test.priority,
            LaboratoryPriority.URGENT,
        )

        self.assertEqual(
            self.laboratory_test.display_order,
            3,
        )

        self.assertEqual(
            self.laboratory_test.notes,
            "Urgent sample",
        )

    def test_update_completed_test_raises_exception(
        self,
    ) -> None:
        """
        Completed tests cannot be updated.
        """

        self.laboratory_test.status = LaboratoryTestStatus.COMPLETED
        self.laboratory_test.is_active = False
        self.laboratory_test.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_test(
                instance=self.laboratory_test,
                validated_data={
                    "name": "Updated",
                },
            )

    def test_update_cancelled_test_raises_exception(
        self,
    ) -> None:
        """
        Cancelled tests cannot be updated.
        """

        self.laboratory_test.status = LaboratoryTestStatus.CANCELLED
        self.laboratory_test.is_active = False

        self.laboratory_test.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_test(
                instance=self.laboratory_test,
                validated_data={
                    "name": "Updated",
                },
            )
        ###########################################################################

    # Workflow
    ###########################################################################

    def test_start_laboratory_test(
        self,
    ) -> None:
        """
        Pending laboratory test should start successfully.
        """

        start_laboratory_test(
            instance=self.laboratory_test,
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.status,
            LaboratoryTestStatus.IN_PROGRESS,
        )

    def test_start_already_started_test(
        self,
    ) -> None:
        """
        Starting an already started test should be idempotent.
        """

        self.laboratory_test.status = LaboratoryTestStatus.IN_PROGRESS

        self.laboratory_test.save()

        laboratory_test = start_laboratory_test(
            instance=self.laboratory_test,
        )

        self.assertEqual(
            laboratory_test.status,
            LaboratoryTestStatus.IN_PROGRESS,
        )

    def test_start_completed_test_raises_exception(
        self,
    ) -> None:
        """
        Completed tests cannot be started.
        """

        self.laboratory_test.status = LaboratoryTestStatus.COMPLETED

        self.laboratory_test.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            start_laboratory_test(
                instance=self.laboratory_test,
            )

    def test_complete_laboratory_test(
        self,
    ) -> None:
        """
        In-progress laboratory test should complete successfully.
        """

        self.laboratory_test.status = LaboratoryTestStatus.IN_PROGRESS

        self.laboratory_test.save()

        complete_laboratory_test(
            instance=self.laboratory_test,
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.status,
            LaboratoryTestStatus.COMPLETED,
        )

    def test_complete_already_completed_test(
        self,
    ) -> None:
        """
        Completing an already completed test should be idempotent.
        """

        self.laboratory_test.status = LaboratoryTestStatus.COMPLETED

        self.laboratory_test.save()

        laboratory_test = complete_laboratory_test(
            instance=self.laboratory_test,
        )

        self.assertEqual(
            laboratory_test.status,
            LaboratoryTestStatus.COMPLETED,
        )

    def test_complete_pending_test_raises_exception(
        self,
    ) -> None:
        """
        Pending tests cannot be completed.
        """

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            complete_laboratory_test(
                instance=self.laboratory_test,
            )

    def test_cancel_laboratory_test(
        self,
    ) -> None:
        """
        Laboratory test should be cancelled.
        """

        cancel_laboratory_test(
            instance=self.laboratory_test,
        )

        self.laboratory_test.refresh_from_db()

        self.assertEqual(
            self.laboratory_test.status,
            LaboratoryTestStatus.CANCELLED,
        )

    def test_cancel_already_cancelled_test(
        self,
    ) -> None:
        """
        Cancelling an already cancelled test should be idempotent.
        """

        self.laboratory_test.status = LaboratoryTestStatus.CANCELLED

        self.laboratory_test.save()

        laboratory_test = cancel_laboratory_test(
            instance=self.laboratory_test,
        )

        self.assertEqual(
            laboratory_test.status,
            LaboratoryTestStatus.CANCELLED,
        )

    def test_cancel_completed_test_raises_exception(
        self,
    ) -> None:
        """
        Completed tests cannot be cancelled.
        """

        self.laboratory_test.status = LaboratoryTestStatus.COMPLETED

        self.laboratory_test.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            cancel_laboratory_test(
                instance=self.laboratory_test,
            )


###############################################################################
# Laboratory Result Services
###############################################################################


class LaboratoryResultServiceTestCase(
    BaseTestCase,
):
    """
    Test cases for laboratory result services.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.result = self.create_laboratory_result()

        self.provider = self.create_provider()

    ###########################################################################
    # Create
    ###########################################################################

    def test_create_laboratory_result(
        self,
    ) -> None:
        """
        Laboratory result should be created successfully.
        """

        laboratory_test = self.create_laboratory_test()

        result = create_laboratory_result(
            validated_data={
                "laboratory_test": laboratory_test,
                "result_value_numeric": 14.2,
                "result_value_text": "",
                "unit": "g/dL",
                "reference_range": "12-16",
                "abnormal_flag": LaboratoryResultFlag.NORMAL,
                "status": LaboratoryResultStatus.RECORDED,
                "resulted_at": timezone.now(),
                "verified_by": None,
                "verified_at": None,
                "notes": "",
            },
        )

        self.assertEqual(
            result.result_value_numeric,
            14.2,
        )

    ###########################################################################
    # Update
    ###########################################################################

    def test_update_numeric_result(
        self,
    ) -> None:
        """
        Numeric result should be updated.
        """

        update_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "result_value_numeric": 15.5,
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.result_value_numeric,
            15.5,
        )

    def test_update_text_result(
        self,
    ) -> None:
        """
        Text result should be updated.
        """

        update_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "result_value_text": "Reactive",
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.result_value_text,
            "Reactive",
        )

    def test_update_notes(
        self,
    ) -> None:
        """
        Notes should be updated.
        """

        update_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "notes": "Updated notes",
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.notes,
            "Updated notes",
        )

    def test_update_abnormal_flag(
        self,
    ) -> None:
        """
        Abnormal flag should be updated.
        """

        update_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "abnormal_flag": LaboratoryResultFlag.HIGH,
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.abnormal_flag,
            LaboratoryResultFlag.HIGH,
        )

    def test_update_multiple_fields(
        self,
    ) -> None:
        """
        Multiple editable fields should be updated.
        """

        update_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "result_value_numeric": 18.2,
                "unit": "mg/dL",
                "reference_range": "10-20",
                "notes": "Updated",
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.result_value_numeric,
            Decimal("18.2"),
        )

        self.assertEqual(
            self.result.unit,
            "mg/dL",
        )

        self.assertEqual(
            self.result.reference_range,
            "10-20",
        )

        self.assertEqual(
            self.result.notes,
            "Updated",
        )

    def test_update_final_result_raises_exception(
        self,
    ) -> None:
        """
        Final results cannot be updated.
        """

        self.result.status = LaboratoryResultStatus.FINAL

        self.result.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_result(
                laboratory_result_id=self.result.id,
                validated_data={
                    "notes": "Should fail",
                },
            )

    ###########################################################################
    # Workflow
    ###########################################################################

    def test_record_laboratory_result(
        self,
    ) -> None:
        """
        Recording should be idempotent.
        """

        result = record_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.RECORDED,
        )

    def test_verify_laboratory_result(
        self,
    ) -> None:
        """
        Laboratory result should be verified.
        """

        result = verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.VERIFIED,
        )

        self.assertEqual(
            result.verified_by,
            self.provider,
        )

    def test_verify_already_verified_result(
        self,
    ) -> None:
        """
        Verifying an already verified result should be idempotent.
        """

        self.result.status = LaboratoryResultStatus.VERIFIED

        self.result.verified_by = self.provider

        self.result.save()

        result = verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.VERIFIED,
        )

    def test_amend_laboratory_result(
        self,
    ) -> None:
        """
        Verified laboratory result should be amended.
        """

        self.result.status = LaboratoryResultStatus.VERIFIED

        self.result.verified_by = self.provider

        self.result.save()

        result = amend_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "notes": "Amended",
            },
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.AMENDED,
        )

    def test_amend_unverified_result_raises_exception(
        self,
    ) -> None:
        """
        Only verified results can be amended.
        """

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            amend_laboratory_result(
                laboratory_result_id=self.result.id,
                validated_data={
                    "notes": "Fail",
                },
            )

    def test_invalidate_laboratory_result(
        self,
    ) -> None:
        """
        Laboratory result should be invalidated.
        """

        result = invalidate_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.INVALIDATED,
        )

    def test_invalidate_already_invalidated_result(
        self,
    ) -> None:
        """
        Invalidating an already invalidated result should be idempotent.
        """

        self.result.status = LaboratoryResultStatus.INVALIDATED

        self.result.save()

        result = invalidate_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.INVALIDATED,
        )


__all__ = [
    "LaboratoryOrderServiceTestCase",
    "LaboratoryTestServiceTestCase",
]
