from .workflow import schedule_order


def schedule(*, order_id, tenant_id, actor_id=None):
    return schedule_order(order_id=order_id, tenant_id=tenant_id, actor_id=actor_id)
