"""
Tests for laboratory selectors.
"""

from __future__ import annotations

from apps.clinical.laboratories.constants import (
    LaboratoryCategory,
    LaboratoryOrderStatus,
    LaboratoryPriority,
    LaboratoryResultFlag,
    LaboratoryResultStatus,
    LaboratorySpecimenType,
    LaboratoryTestStatus,
)
from apps.clinical.laboratories.selectors.laboratory_order import (
    count_patient_laboratory_orders,
    exists_order_number,
    get_laboratory_order,
    list_completed_laboratory_orders,
    list_encounter_laboratory_orders,
    list_laboratory_orders,
    list_patient_laboratory_orders,
    list_pending_laboratory_orders,
)
from apps.clinical.laboratories.selectors.laboratory_result import (
    count_patient_laboratory_results,
    exists_laboratory_result,
    get_laboratory_result,
    list_critical_laboratory_results,
    list_encounter_laboratory_results,
    list_flagged_laboratory_results,
    list_laboratory_results,
    list_laboratory_test_results,
    list_patient_laboratory_results,
    list_pending_laboratory_results,
    list_provider_verified_results,
    list_status_laboratory_results,
    list_verified_laboratory_results,
)
from apps.clinical.laboratories.selectors.laboratory_test import (
    count_laboratory_order_tests,
    exists_laboratory_test,
    get_laboratory_test,
    list_category_laboratory_tests,
    list_completed_laboratory_tests,
    list_laboratory_order_tests,
    list_laboratory_tests,
    list_pending_laboratory_tests,
    list_priority_laboratory_tests,
    list_specimen_laboratory_tests,
    list_status_laboratory_tests,
)
from apps.common.tests.base import BaseTestCase

###############################################################################
# Laboratory Order
###############################################################################


class LaboratoryOrderSelectorTestCase(BaseTestCase):
    """
    Test cases for laboratory order selectors.
    """

    def setUp(self) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

    def test_list_laboratory_orders(self) -> None:
        """
        Should return all laboratory orders.
        """

        queryset = list_laboratory_orders()

        self.assertIn(
            self.order,
            queryset,
        )

    def test_get_laboratory_order(self) -> None:
        """
        Should return laboratory order by primary key.
        """

        order = get_laboratory_order(
            pk=self.order.pk,
        )

        self.assertEqual(
            order,
            self.order,
        )

    def test_list_patient_laboratory_orders(self) -> None:
        """
        Should return laboratory orders for a patient.
        """

        queryset = list_patient_laboratory_orders(
            patient_id=self.order.patient.id,
        )

        self.assertIn(
            self.order,
            queryset,
        )

    def test_list_encounter_laboratory_orders(self) -> None:
        """
        Should return laboratory orders for an encounter.
        """

        queryset = list_encounter_laboratory_orders(
            encounter_id=self.order.encounter.id,
        )

        self.assertIn(
            self.order,
            queryset,
        )

    def test_list_pending_laboratory_orders(self) -> None:
        """
        Should return pending laboratory orders.
        """

        queryset = list_pending_laboratory_orders()

        self.assertIn(
            self.order,
            queryset,
        )

    def test_list_completed_laboratory_orders(self) -> None:
        """
        Should return completed laboratory orders.
        """

        self.order.status = LaboratoryOrderStatus.COMPLETED

        self.order.save()

        queryset = list_completed_laboratory_orders()

        self.assertIn(
            self.order,
            queryset,
        )

    def test_exists_order_number_returns_true(self) -> None:
        """
        Existing order number should return True.
        """

        self.assertTrue(
            exists_order_number(
                organization_id=self.organization.id,
                order_number=self.order.order_number,
            ),
        )

    def test_exists_order_number_returns_false(self) -> None:
        """
        Unknown order number should return False.
        """

        self.assertFalse(
            exists_order_number(
                organization_id=self.organization.id,
                order_number="INVALID123",
            ),
        )

    def test_count_patient_laboratory_orders(self) -> None:
        """
        Should return total laboratory orders for a patient.
        """

        count = count_patient_laboratory_orders(
            patient_id=self.order.patient.id,
        )

        self.assertEqual(
            count,
            1,
        )


###############################################################################
# Laboratory Test
###############################################################################


class LaboratoryTestSelectorTestCase(BaseTestCase):
    """
    Test cases for laboratory test selectors.
    """

    def setUp(self) -> None:
        super().setUp()

        self.order = self.create_laboratory_order()

        self.laboratory_test = self.create_laboratory_test(
            laboratory_order=self.order,
        )

    def test_list_laboratory_tests(self) -> None:
        """
        Should return all laboratory tests.
        """

        queryset = list_laboratory_tests()

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_get_laboratory_test(self) -> None:
        """
        Should return laboratory test by primary key.
        """

        laboratory_test = get_laboratory_test(
            pk=self.laboratory_test.pk,
        )

        self.assertEqual(
            laboratory_test,
            self.laboratory_test,
        )

    def test_list_laboratory_order_tests(self) -> None:
        """
        Should return laboratory tests belonging to an order.
        """

        queryset = list_laboratory_order_tests(
            laboratory_order_id=self.order.id,
        )

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_pending_laboratory_tests(self) -> None:
        """
        Should return pending laboratory tests.
        """

        queryset = list_pending_laboratory_tests()

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_completed_laboratory_tests(self) -> None:
        """
        Should return completed laboratory tests.
        """

        self.laboratory_test.status = LaboratoryTestStatus.COMPLETED

        self.laboratory_test.save()

        queryset = list_completed_laboratory_tests()

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_status_laboratory_tests(self) -> None:
        """
        Should return laboratory tests filtered by status.
        """

        queryset = list_status_laboratory_tests(
            status=LaboratoryTestStatus.PENDING,
        )

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_category_laboratory_tests(self) -> None:
        """
        Should return laboratory tests filtered by category.
        """

        queryset = list_category_laboratory_tests(
            category=LaboratoryCategory.HEMATOLOGY,
        )

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_priority_laboratory_tests(self) -> None:
        """
        Should return laboratory tests filtered by priority.
        """

        queryset = list_priority_laboratory_tests(
            priority=LaboratoryPriority.ROUTINE,
        )

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_list_specimen_laboratory_tests(self) -> None:
        """
        Should return laboratory tests filtered by specimen type.
        """

        queryset = list_specimen_laboratory_tests(
            specimen_type=LaboratorySpecimenType.BLOOD,
        )

        self.assertIn(
            self.laboratory_test,
            queryset,
        )

    def test_exists_laboratory_test(self) -> None:
        """
        Existing laboratory test should return True.
        """

        self.assertTrue(
            exists_laboratory_test(
                laboratory_order_id=self.order.id,
                code=self.laboratory_test.code,
            ),
        )

    def test_count_laboratory_order_tests(self) -> None:
        """
        Should return total laboratory tests for an order.
        """

        count = count_laboratory_order_tests(
            laboratory_order_id=self.order.id,
        )

        self.assertEqual(
            count,
            1,
        )


class LaboratoryResultSelectorTestCase(
    BaseTestCase,
):
    """
    Test cases for laboratory result selectors.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.result = self.create_laboratory_result()

    ###########################################################################
    # Core
    ###########################################################################

    def test_list_laboratory_results(
        self,
    ) -> None:
        """
        Should return all laboratory results.
        """

        queryset = list_laboratory_results()

        self.assertIn(
            self.result,
            queryset,
        )

    def test_get_laboratory_result(
        self,
    ) -> None:
        """
        Should return laboratory result by primary key.
        """

        result = get_laboratory_result(
            pk=self.result.pk,
        )

        self.assertEqual(
            result,
            self.result,
        )

    ###########################################################################
    # Relationships
    ###########################################################################

    def test_list_laboratory_test_results(
        self,
    ) -> None:
        """
        Should return results for a laboratory test.
        """

        queryset = list_laboratory_test_results(
            laboratory_test_id=self.result.laboratory_test.id,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_patient_laboratory_results(
        self,
    ) -> None:
        """
        Should return results for a patient.
        """

        queryset = list_patient_laboratory_results(
            patient_id=self.result.laboratory_test.laboratory_order.patient.id,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_encounter_laboratory_results(
        self,
    ) -> None:
        """
        Should return results for an encounter.
        """

        queryset = list_encounter_laboratory_results(
            encounter_id=self.result.laboratory_test.laboratory_order.encounter.id,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_provider_verified_results(
        self,
    ) -> None:
        """
        Should return results verified by a provider.
        """

        provider = self.create_provider()

        self.result.verified_by = provider
        self.result.save()

        queryset = list_provider_verified_results(
            provider_id=provider.id,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    ###########################################################################
    # Filters
    ###########################################################################

    def test_list_status_laboratory_results(
        self,
    ) -> None:
        """
        Should filter by status.
        """

        queryset = list_status_laboratory_results(
            status=self.result.status,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_verified_laboratory_results(
        self,
    ) -> None:
        """
        Should return verified laboratory results.
        """

        self.result.status = LaboratoryResultStatus.VERIFIED

        self.result.save()

        queryset = list_verified_laboratory_results()

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_pending_laboratory_results(
        self,
    ) -> None:
        """
        Should return pending laboratory results.
        """

        self.result.status = LaboratoryResultStatus.RECORDED

        self.result.save()

        queryset = list_pending_laboratory_results()

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_flagged_laboratory_results(
        self,
    ) -> None:
        """
        Should filter by abnormal flag.
        """

        queryset = list_flagged_laboratory_results(
            flag=self.result.abnormal_flag,
        )

        self.assertIn(
            self.result,
            queryset,
        )

    def test_list_critical_laboratory_results(
        self,
    ) -> None:
        """
        Should return critical laboratory results.
        """

        self.result.abnormal_flag = LaboratoryResultFlag.CRITICAL

        self.result.save()

        queryset = list_critical_laboratory_results()

        self.assertIn(
            self.result,
            queryset,
        )

    ###########################################################################
    # Aggregate
    ###########################################################################

    def test_exists_laboratory_result_returns_true(
        self,
    ) -> None:
        """
        Existing laboratory result should return True.
        """

        self.assertTrue(
            exists_laboratory_result(
                laboratory_test_id=self.result.laboratory_test.id,
            ),
        )

    def test_exists_laboratory_result_returns_false(
        self,
    ) -> None:
        """
        Unknown laboratory test should return False.
        """

        self.assertFalse(
            exists_laboratory_result(
                laboratory_test_id=999999,
            ),
        )

    def test_count_patient_laboratory_results(
        self,
    ) -> None:
        """
        Should return total laboratory results for a patient.
        """

        count = count_patient_laboratory_results(
            patient_id=self.result.laboratory_test.laboratory_order.patient.id,
        )

        self.assertEqual(
            count,
            1,
        )


__all__ = [
    "LaboratoryOrderSelectorTestCase",
    "LaboratoryTestSelectorTestCase",
    "LaboratoryResultSelectorTestCase",
]
