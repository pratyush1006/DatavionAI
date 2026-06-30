"""
Custom pagination classes used across Datavion APIs.
"""

from rest_framework.pagination import PageNumberPagination


class DatavionPagination(PageNumberPagination):
    """
    Default pagination for Datavion API endpoints.
    """

    page_size: int = 20
    page_size_query_param: str = "page_size"
    max_page_size: int = 100
    page_query_param: str = "page"
