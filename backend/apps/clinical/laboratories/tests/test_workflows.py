"""
Workflow tests for the Laboratories application.
"""

from __future__ import annotations

from apps.clinical.laboratories.constants import (
    LaboratoryOrderStatus,
    LaboratoryResultStatus,
    LaboratoryTestStatus,
)
from apps.clinical.laboratories.services import (
    amend_laboratory_result,
    cancel_laboratory_order,
    cancel_laboratory_test,
    complete_laboratory_test,
    invalidate_laboratory_result,
    record_laboratory_result,
    start_laboratory_test,
    update_laboratory_order,
    verify_laboratory_result,
)
from apps.common.tests.base import BaseTestCase
from apps.core.exceptions import InvalidWorkflowTransition


class LaboratoryWorkflowTestCase(
    BaseTestCase,
):
    """
    End-to-end workflow tests for the Laboratories module.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

        self.test = self.create_laboratory_test(
            laboratory_order=self.order,
        )

        self.result = self.create_laboratory_result(
            laboratory_test=self.test,
        )

        self.provider = self.create_provider()

    def test_complete_laboratory_workflow(
        self,
    ) -> None:
        """
        Complete laboratory workflow.

        Order
            ↓
        Test
            ↓
        Recorded
            ↓
        Verified
            ↓
        Amended
        """

        self.assertEqual(
            self.order.status,
            LaboratoryOrderStatus.ORDERED,
        )

        start_laboratory_test(
            instance=self.test,
        )

        self.test.refresh_from_db()

        self.assertEqual(
            self.test.status,
            LaboratoryTestStatus.IN_PROGRESS,
        )

        complete_laboratory_test(
            instance=self.test,
        )

        self.test.refresh_from_db()

        self.assertEqual(
            self.test.status,
            LaboratoryTestStatus.COMPLETED,
        )

        record_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.status,
            LaboratoryResultStatus.RECORDED,
        )

        verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.status,
            LaboratoryResultStatus.VERIFIED,
        )

        amend_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "notes": "Workflow amendment",
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.status,
            LaboratoryResultStatus.AMENDED,
        )

        self.assertEqual(
            self.result.notes,
            "Workflow amendment",
        )

    def test_cancel_order_workflow(
        self,
    ) -> None:
        """
        Cancelled orders cannot be updated.
        """

        cancel_laboratory_order(
            instance=self.order,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            LaboratoryOrderStatus.CANCELLED,
        )

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            update_laboratory_order(
                instance=self.order,
                validated_data={
                    "clinical_notes": "Updated",
                },
            )

    def test_laboratory_test_workflow(
        self,
    ) -> None:
        """
        Pending → In Progress → Completed.
        """

        start_laboratory_test(
            instance=self.test,
        )

        self.test.refresh_from_db()

        self.assertEqual(
            self.test.status,
            LaboratoryTestStatus.IN_PROGRESS,
        )

        complete_laboratory_test(
            instance=self.test,
        )

        self.test.refresh_from_db()

        self.assertEqual(
            self.test.status,
            LaboratoryTestStatus.COMPLETED,
        )

    def test_cancel_laboratory_test_workflow(
        self,
    ) -> None:
        """
        Pending laboratory test can be cancelled.
        """

        cancel_laboratory_test(
            instance=self.test,
        )

        self.test.refresh_from_db()

        self.assertEqual(
            self.test.status,
            LaboratoryTestStatus.CANCELLED,
        )

    def test_verify_without_recording_workflow(
        self,
    ) -> None:
        """
        Verification without recording should fail.
        """

        self.result.status = LaboratoryResultStatus.AMENDED

        self.result.save()

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            verify_laboratory_result(
                laboratory_result_id=self.result.id,
                verified_by_id=self.provider.id,
            )

    def test_invalidate_result_workflow(
        self,
    ) -> None:
        """
        Laboratory result should be invalidated.
        """

        invalidate_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.status,
            LaboratoryResultStatus.INVALIDATED,
        )

    def test_completed_test_cannot_restart_workflow(
        self,
    ) -> None:
        """
        Completed laboratory tests cannot be restarted.
        """

        start_laboratory_test(
            instance=self.test,
        )

        complete_laboratory_test(
            instance=self.test,
        )

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            start_laboratory_test(
                instance=self.test,
            )

    def test_cancelled_test_cannot_complete_workflow(
        self,
    ) -> None:
        """
        Cancelled laboratory tests cannot be completed.
        """

        cancel_laboratory_test(
            instance=self.test,
        )

        with self.assertRaises(
            InvalidWorkflowTransition,
        ):
            complete_laboratory_test(
                instance=self.test,
            )

    def test_verified_result_workflow(
        self,
    ) -> None:
        """
        Verifying an already verified result is idempotent.
        """

        record_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        result = verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        self.assertEqual(
            result.status,
            LaboratoryResultStatus.VERIFIED,
        )

    def test_verified_result_can_be_amended_workflow(
        self,
    ) -> None:
        """
        Verified result should transition to amended.
        """

        record_laboratory_result(
            laboratory_result_id=self.result.id,
        )

        verify_laboratory_result(
            laboratory_result_id=self.result.id,
            verified_by_id=self.provider.id,
        )

        amend_laboratory_result(
            laboratory_result_id=self.result.id,
            validated_data={
                "notes": "Corrected value",
            },
        )

        self.result.refresh_from_db()

        self.assertEqual(
            self.result.status,
            LaboratoryResultStatus.AMENDED,
        )

    def test_order_contains_test_workflow(
        self,
    ) -> None:
        """
        Laboratory order should own the created test.
        """

        self.assertEqual(
            self.test.laboratory_order,
            self.order,
        )

        self.assertEqual(
            self.order.tests.count(),
            1,
        )

    def test_test_contains_result_workflow(
        self,
    ) -> None:
        """
        Laboratory test should own the created result.
        """

        self.assertEqual(
            self.result.laboratory_test,
            self.test,
        )

        self.assertEqual(
            self.test.result,
            self.result,
        )


__all__ = [
    "LaboratoryWorkflowTestCase",
]
