from .appointments import slots
from .catalog import tests
from .events import outbox_summary
from .laboratories import laboratories
from .orders import orders
from .reports import reports
from .results import results

__all__ = (
    "laboratories",
    "tests",
    "slots",
    "orders",
    "results",
    "reports",
    "outbox_summary",
)
