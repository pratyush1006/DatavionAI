from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


class BaseListCreateAPIView(ListCreateAPIView):
    """
    Base class for list/create endpoints.

    Future:
    - Audit logging
    - Metrics
    - Organization filtering
    - Standard responses
    """

    pass


class BaseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Base class for retrieve/update/delete endpoints.

    Future:
    - Soft delete
    - Audit logging
    - Metrics
    """

    pass
