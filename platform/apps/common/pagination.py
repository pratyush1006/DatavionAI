from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination used across all list endpoints.
    """

    page_size = 20

    page_size_query_param = "page_size"

    max_page_size = 100

    page_query_param = "page"

    last_page_strings = ("last",)

    invalid_page_message = "The requested page is invalid."
