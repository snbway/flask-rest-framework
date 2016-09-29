# -*- coding: utf-8 -*-

import status


class APIException(Exception):
    """
    Base class for API exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = str(detail)
        else:
            self.detail = str(self.default_detail)

    def __str__(self):
        return self.detail


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'


class NotAuthenticated(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Authentication credentials were not provided.'


class AuthenticationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Incorrect authentication credentials.'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found.'


class MethodNotAllowed(APIException):
    status = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = 'Method not allowed.'
