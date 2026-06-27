from rest_framework.pagination import PageNumberPagination

from apps.common.constants import (
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
)


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination used across all list endpoints.
    """

    page_size = DEFAULT_PAGE_SIZE

    page_size_query_param = "page_size"

    max_page_size = MAX_PAGE_SIZE

    page_query_param = "page"

    last_page_strings = ("last",)

    invalid_page_message = "The requested page is invalid."
