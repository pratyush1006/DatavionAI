"""
Scrub Result services.
"""

from __future__ import annotations

from apps.revenue_cycle.claim_scrubbing.models import ClaimScrubResult
from apps.revenue_cycle.components import RcmService

create_scrub = None
update_scrub = None
delete_scrub = None


class ClaimScrubResultService(RcmService):
    """
    Write-side operations for scrub result records.
    """

    model = ClaimScrubResult


create_scrub = ClaimScrubResultService.create
update_scrub = ClaimScrubResultService.update
delete_scrub = ClaimScrubResultService.delete


__all__ = [
    "ClaimScrubResultService",
    "create_scrub",
    "delete_scrub",
    "update_scrub",
]
