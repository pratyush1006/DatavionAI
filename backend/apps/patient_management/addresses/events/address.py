"""Patient Address event payload."""

from __future__ import annotations


class AddressEvent:
    def __init__(self, address_id, event_type):
        self.address_id = address_id
        self.event_type = event_type
