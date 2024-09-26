from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, ValidationError) and response is not None:
        response.status_code = HTTP_422_UNPROCESSABLE_ENTITY

    return response
