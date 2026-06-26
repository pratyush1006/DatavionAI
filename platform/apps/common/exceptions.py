from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Standardize API error responses.
    """

    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "message": response.data.get(
                "detail",
                "Validation Error",
            ),
            "errors": response.data,
        }

    return response
