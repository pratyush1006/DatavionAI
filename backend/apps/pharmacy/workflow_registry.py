from apps.core.workflows import workflow_registry
from apps.pharmacy.workflows import (
    DispenseStockWorkflow,
    ReceiveStockWorkflow,
    ReturnStockWorkflow,
)

PHARMACY_WORKFLOWS = {
    "pharmacy.inventory.receive": ReceiveStockWorkflow,
    "pharmacy.inventory.dispense": DispenseStockWorkflow,
    "pharmacy.inventory.return": ReturnStockWorkflow,
}


def register_pharmacy_workflows():
    for name, workflow in PHARMACY_WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_pharmacy_workflows()
