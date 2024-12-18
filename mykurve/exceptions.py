"""Exceptions."""


class MyKurveApiException(Exception):
    """Base exception for mykurve API"""


class NotAuthenticated(MyKurveApiException):
    """Not authenticated exception."""


class ApiException(MyKurveApiException):
    """Api error."""


class AuthenticationFailed(MyKurveApiException):
    """Authentication failed."""
