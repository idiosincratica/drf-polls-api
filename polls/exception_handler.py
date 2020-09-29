from rest_framework.views import exception_handler, set_rollback
from rest_framework.exceptions import APIException
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    """Makes error codes available in response"""

    if isinstance(exc, APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        data = exc.get_full_details()

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return exception_handler(exc, context)
