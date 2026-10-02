from django.db import transaction

from ..models import LaboratoryPanelItem, LaboratoryTest
from .audit import audit
from .events import event
from .laboratory import LaboratoryServiceError


@transaction.atomic
def create_test(
    *,
    organization_id,
    code,
    name,
    specimen_type,
    price=0,
    department_id=None,
    actor_id=None,
    **fields,
):
    if not code or not name or not specimen_type:
        raise LaboratoryServiceError("Test code, name and specimen type are required.")
    allowed = {
        "short_name",
        "preparation",
        "instructions",
        "unit",
        "reference_range",
        "critical_range",
        "turnaround_minutes",
        "is_panel",
        "status",
    }
    values = {k: v for k, v in fields.items() if k in allowed}
    obj = LaboratoryTest.objects.create(
        organization_id=organization_id,
        code=code,
        name=name,
        specimen_type=specimen_type,
        price=price,
        department_id=department_id,
        **values,
    )
    audit(organization_id, actor_id, "catalog.test.created", "LaboratoryTest", obj.id)
    event(organization_id, "laboratory.catalog.test.created", "LaboratoryTest", obj.id)
    return obj


@transaction.atomic
def set_test_status(*, organization_id, test_id, status, actor_id=None):
    obj = LaboratoryTest.objects.select_for_update().get(
        id=test_id, organization_id=organization_id, is_deleted=False
    )
    if status not in {"active", "inactive"}:
        raise LaboratoryServiceError("Invalid laboratory test status.")
    obj.status = status
    obj.save(update_fields=["status", "updated_at"])
    audit(
        organization_id,
        actor_id,
        "catalog.test.status_changed",
        "LaboratoryTest",
        obj.id,
        {"status": status},
    )
    return obj


@transaction.atomic
def add_panel_item(*, organization_id, panel_id, test_id, sort_order=0, actor_id=None):
    panel = LaboratoryTest.objects.select_for_update().get(
        id=panel_id, organization_id=organization_id, is_deleted=False, is_panel=True
    )
    test = LaboratoryTest.objects.get(
        id=test_id, organization_id=organization_id, is_deleted=False
    )
    if panel.id == test.id:
        raise LaboratoryServiceError("A laboratory panel cannot contain itself.")
    item, created = LaboratoryPanelItem.objects.get_or_create(
        panel=panel, test=test, defaults={"sort_order": sort_order}
    )
    if not created:
        raise LaboratoryServiceError("Test is already a member of this panel.")
    audit(
        organization_id,
        actor_id,
        "catalog.panel.item_added",
        "LaboratoryPanelItem",
        item.id,
    )
    event(
        organization_id,
        "laboratory.catalog.panel.item_added",
        "LaboratoryPanelItem",
        item.id,
    )
    return item
