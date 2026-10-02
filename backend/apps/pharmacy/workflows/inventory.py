from dataclasses import dataclass

from apps.core.workflows import BaseWorkflow, WorkflowResult
from apps.pharmacy.services.inventory import dispense_stock, receive_stock, return_stock


@dataclass(frozen=True)
class ReceiveStockRequest:
    organization_id: object
    batch: object
    quantity: object
    actor_id: object = None
    reference_id: object = None


class ReceiveStockWorkflow(BaseWorkflow):
    name = "pharmacy.inventory.receive"

    def execute(self, context, request):
        result = receive_stock(
            organization=context.organization,
            batch=request.batch,
            quantity=request.quantity,
            actor_id=request.actor_id,
            reference_id=request.reference_id,
        )
        return WorkflowResult.success(result)


@dataclass(frozen=True)
class DispenseStockRequest:
    organization_id: object
    batch: object
    quantity: object
    actor_id: object = None
    reference_id: object = None


class DispenseStockWorkflow(BaseWorkflow):
    name = "pharmacy.inventory.dispense"

    def execute(self, context, request):
        result = dispense_stock(
            organization=context.organization,
            batch=request.batch,
            quantity=request.quantity,
            actor_id=request.actor_id,
            reference_id=request.reference_id,
        )
        return WorkflowResult.success(result)


@dataclass(frozen=True)
class ReturnStockRequest:
    organization_id: object
    batch: object
    quantity: object
    restockable: bool
    actor_id: object = None
    reference_id: object = None


class ReturnStockWorkflow(BaseWorkflow):
    name = "pharmacy.inventory.return"

    def execute(self, context, request):
        result = return_stock(
            organization=context.organization,
            batch=request.batch,
            quantity=request.quantity,
            restockable=request.restockable,
            actor_id=request.actor_id,
            reference_id=request.reference_id,
        )
        return WorkflowResult.success(result)
