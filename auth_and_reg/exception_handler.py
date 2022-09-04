from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError


def base_exception_handler(exc, context):
    response = exception_handler(exc, context)
    message = "Server error"
    try:
        message = list(response.data.values())[0]
        while type(message) == list:
            message = message[0]
    except AttributeError:
        try:
            message = response.data.values()
        except AttributeError:
            pass

    try:
        response.data = {"error": str(message)}
    except AttributeError:
        pass

    return response
