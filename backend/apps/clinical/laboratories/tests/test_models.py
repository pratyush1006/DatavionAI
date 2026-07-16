"""
Tests for the Laboratory models.
"""

from __future__ import annotations

from apps.clinical.laboratories.constants import (
    DEFAULT_LABORATORY_ORDER_STATUS,
    DEFAULT_LABORATORY_PRIORITY,
    DEFAULT_LABORATORY_RESULT_FLAG,
    DEFAULT_LABORATORY_RESULT_STATUS,
    DEFAULT_LABORATORY_TEST_STATUS,
    LaboratoryOrderStatus,
    LaboratoryResultStatus,
    LaboratoryTestStatus,
)
from apps.clinical.laboratories.models import (
    LaboratoryOrder,
    LaboratoryResult,
    LaboratoryTest,
)
from apps.common.tests.base import BaseTestCase

###############################################################################
# Laboratory Order
###############################################################################


class LaboratoryOrderModelTestCase(BaseTestCase):
    """
    Test cases for the LaboratoryOrder model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

    def test_laboratory_order_creation(self) -> None:
        """
        Laboratory order should be created successfully.
        """

        self.assertEqual(
            self.order.organization,
            self.organization,
        )

        self.assertEqual(
            self.order.patient,
            self.order.patient,
        )

        self.assertEqual(
            self.order.provider,
            self.order.provider,
        )

        self.assertEqual(
            self.order.encounter,
            self.order.encounter,
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the order title.
        """

        self.assertEqual(
            str(self.order),
            self.order.title,
        )

    def test_title_property(self) -> None:
        """
        Title property should return the formatted title.
        """

        expected = (
            f"{self.order.order_number} | "
            f"{self.order.patient.full_name} | "
            f"{self.order.ordered_at:%Y-%m-%d %H:%M}"
        )

        self.assertEqual(
            self.order.title,
            expected,
        )

    def test_default_priority(self) -> None:
        """
        Default priority should be applied.
        """

        self.assertEqual(
            self.order.priority,
            DEFAULT_LABORATORY_PRIORITY,
        )

    def test_default_status(self) -> None:
        """
        Default status should be applied.
        """

        self.assertEqual(
            self.order.status,
            DEFAULT_LABORATORY_ORDER_STATUS,
        )

    def test_default_optional_fields(self) -> None:
        """
        Optional fields should default to blank.
        """

        self.assertEqual(
            self.order.clinical_notes,
            "",
        )

        self.assertEqual(
            self.order.instructions,
            "",
        )

    def test_is_active_property(self) -> None:
        """
        Active orders should return True.
        """

        self.assertTrue(
            self.order.is_active,
        )

    def test_is_completed_property(self) -> None:
        """
        Completed orders should return True.
        """

        self.order.status = LaboratoryOrderStatus.COMPLETED

        self.assertTrue(
            self.order.is_completed,
        )

    def test_is_cancelled_property(self) -> None:
        """
        Cancelled orders should return True.
        """

        self.order.status = LaboratoryOrderStatus.CANCELLED

        self.assertTrue(
            self.order.is_cancelled,
        )

    def test_meta_ordering(self) -> None:
        """
        Model should use configured ordering.
        """

        self.assertEqual(
            LaboratoryOrder._meta.ordering,
            ("-ordered_at",),
        )

    def test_meta_table_name(self) -> None:
        """
        Model should use configured database table.
        """

        self.assertEqual(
            LaboratoryOrder._meta.db_table,
            "laboratory_orders",
        )

    def test_foreign_key_relationships(self) -> None:
        """
        Foreign key relationships should be valid.
        """

        self.assertEqual(
            self.order.organization.id,
            self.organization.id,
        )

        self.assertIsNotNone(
            self.order.patient,
        )

        self.assertIsNotNone(
            self.order.provider,
        )

        self.assertIsNotNone(
            self.order.encounter,
        )


###############################################################################
# Laboratory Test
###############################################################################


class LaboratoryTestModelTestCase(BaseTestCase):
    """
    Test cases for the LaboratoryTest model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

        self.test = self.create_laboratory_test(
            laboratory_order=self.order,
        )

    def test_laboratory_test_creation(self) -> None:
        """
        Laboratory test should be created successfully.
        """

        self.assertEqual(
            self.test.laboratory_order,
            self.order,
        )

        self.assertEqual(
            self.test.name,
            "Complete Blood Count",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the title.
        """

        self.assertEqual(
            str(self.test),
            self.test.title,
        )

    def test_title_property(self) -> None:
        """
        Title should return formatted value.
        """

        expected = f"{self.order.order_number} | {self.test.name}"

        self.assertEqual(
            self.test.title,
            expected,
        )

    def test_default_priority(self) -> None:
        """
        Default priority should be applied.
        """

        self.assertEqual(
            self.test.priority,
            DEFAULT_LABORATORY_PRIORITY,
        )

    def test_default_status(self) -> None:
        """
        Default status should be applied.
        """

        self.assertEqual(
            self.test.status,
            DEFAULT_LABORATORY_TEST_STATUS,
        )

    def test_is_pending_property(self) -> None:
        """
        Pending property should return True.
        """

        self.assertTrue(
            self.test.is_pending,
        )

    def test_is_in_progress_property(self) -> None:
        """
        In-progress property should return True.
        """

        self.test.status = LaboratoryTestStatus.IN_PROGRESS

        self.assertTrue(
            self.test.is_in_progress,
        )

    def test_is_completed_property(self) -> None:
        """
        Completed property should return True.
        """

        self.test.status = LaboratoryTestStatus.COMPLETED

        self.assertTrue(
            self.test.is_completed,
        )

    def test_is_cancelled_property(self) -> None:
        """
        Cancelled property should return True.
        """

        self.test.status = LaboratoryTestStatus.CANCELLED

        self.assertTrue(
            self.test.is_cancelled,
        )

    def test_meta_ordering(self) -> None:
        """
        Model should use configured ordering.
        """

        self.assertEqual(
            LaboratoryTest._meta.ordering,
            (
                "display_order",
                "name",
            ),
        )

    def test_meta_table_name(self) -> None:
        """
        Model should use configured database table.
        """

        self.assertEqual(
            LaboratoryTest._meta.db_table,
            "laboratory_tests",
        )

    def test_foreign_key_relationship(self) -> None:
        """
        Laboratory test should belong to a laboratory order.
        """

        self.assertEqual(
            self.test.laboratory_order.id,
            self.order.id,
        )


class LaboratoryResultModelTestCase(BaseTestCase):
    """
    Test cases for the LaboratoryResult model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.result = self.create_laboratory_result()

    ###########################################################################
    # Creation
    ###########################################################################

    def test_laboratory_result_creation(
        self,
    ) -> None:
        """
        Laboratory result should be created successfully.
        """

        self.assertEqual(
            self.result.laboratory_test,
            self.result.laboratory_test,
        )

    ###########################################################################
    # Representation
    ###########################################################################

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the result title.
        """

        self.assertEqual(
            str(self.result),
            self.result.title,
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title should be formatted correctly.
        """

        expected = (
            f"{self.result.laboratory_test.name}"
            f" | "
            f"{self.result.laboratory_test.laboratory_order.order_number}"
        )

        self.assertEqual(
            self.result.title,
            expected,
        )

    ###########################################################################
    # Defaults
    ###########################################################################

    def test_default_status(
        self,
    ) -> None:
        """
        Default status should be applied.
        """

        self.assertEqual(
            self.result.status,
            DEFAULT_LABORATORY_RESULT_STATUS,
        )

    def test_default_abnormal_flag(
        self,
    ) -> None:
        """
        Default abnormal flag should be applied.
        """

        self.assertEqual(
            self.result.abnormal_flag,
            DEFAULT_LABORATORY_RESULT_FLAG,
        )

    def test_default_optional_fields(
        self,
    ) -> None:
        """
        Optional fields should default correctly.
        """

        self.assertEqual(
            self.result.result_value_text,
            "",
        )

        self.assertEqual(
            self.result.notes,
            "",
        )

        self.assertIsNone(
            self.result.verified_by,
        )

        self.assertIsNone(
            self.result.verified_at,
        )

    ###########################################################################
    # Properties
    ###########################################################################

    def test_is_recorded_property(
        self,
    ) -> None:
        """
        Recorded property should return True.
        """

        self.result.status = LaboratoryResultStatus.RECORDED

        self.assertTrue(
            self.result.is_recorded,
        )

    def test_is_verified_property(
        self,
    ) -> None:
        """
        Verified property should return True.
        """

        self.result.status = LaboratoryResultStatus.VERIFIED

        self.assertTrue(
            self.result.is_verified,
        )

    def test_is_final_property(
        self,
    ) -> None:
        """
        Final property should return True.
        """

        self.result.status = LaboratoryResultStatus.FINAL

        self.assertTrue(
            self.result.is_final,
        )

    def test_is_amended_property(
        self,
    ) -> None:
        """
        Amended property should return True.
        """

        self.result.status = LaboratoryResultStatus.AMENDED

        self.assertTrue(
            self.result.is_amended,
        )

    def test_is_invalidated_property(
        self,
    ) -> None:
        """
        Invalidated property should return True.
        """

        self.result.status = LaboratoryResultStatus.INVALIDATED

        self.assertTrue(
            self.result.is_invalidated,
        )

    def test_is_active_property(
        self,
    ) -> None:
        """
        Active property should return False for final results.
        """

        self.result.status = LaboratoryResultStatus.FINAL

        self.assertFalse(
            self.result.is_active,
        )

    ###########################################################################
    # Meta
    ###########################################################################

    def test_meta_ordering(
        self,
    ) -> None:
        """
        Model should use configured ordering.
        """

        self.assertEqual(
            LaboratoryResult._meta.ordering,
            ("-resulted_at",),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        Model should use configured database table.
        """

        self.assertEqual(
            LaboratoryResult._meta.db_table,
            "laboratory_results",
        )

    ###########################################################################
    # Relationships
    ###########################################################################

    def test_relationships(
        self,
    ) -> None:
        """
        Relationships should be valid.
        """

        self.assertIsNotNone(
            self.result.laboratory_test,
        )

        self.assertEqual(
            self.result.laboratory_test.pk,
            self.result.laboratory_test.pk,
        )


__all__ = [
    "LaboratoryOrderModelTestCase",
    "LaboratoryTestModelTestCase",
    "LaboratoryResultModelTestCase",
]
