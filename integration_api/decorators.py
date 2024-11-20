from typing import Optional

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework.serializers import Serializer

from .utils import api_unauthorized_response, is_token_valid, api_bad_request_response, \
    api_serializer_validation_error_response, api_error_response


def requires_api_auth(function=None):
    """
    Requires that a valid API bearer token is provided by the request.
    The token must be present in the `Authorization` header, and it must be prefixed with "Bearer ".

    See the `is_token_valid` function for details on how the token is validated.
    """

    def wrapper(request: WSGIRequest, *args, **kwargs) -> JsonResponse:
        header: Optional[str] = request.headers.get('authorization')

        if header is None:
            return api_unauthorized_response()

        if not header.startswith('Bearer '):
            return api_unauthorized_response()

        token = header[7:]

        if not is_token_valid(token):
            return api_unauthorized_response()

        return function(request, *args, **kwargs)

    return wrapper


def body_validation_serializer(serializer_class: type[Serializer] = None):
    """
    Requires that the request body for this Django REST API handler is valid according to the specified Serializer class.
    The class inheriting from Serializer must be passed in, not an instance of it.

    The validated body will be assigned as a field named `validated_body` on the request.
    The serialized instance used will be assigned as a field named `serializer` on the request.

    Example:
        @body_validation_serializer(MySerializer)
        def post(request: WSGIRequest) -> JsonResponse:
            return api_success_response({'name': request.validated_body['name']})
    """

    def decorator(function=None):
        def wrapper(request: WSGIRequest, *args, **kwargs) -> JsonResponse:
            if not hasattr(request, 'data') or request.data is None:
                return api_error_response(400, 'Expected body')

            serializer = serializer_class(data=request.data)
            if not serializer.is_valid():
                return api_serializer_validation_error_response(serializer)

            request.validated_body = serializer.validated_data
            request.serializer = serializer

            return function(request, *args, **kwargs)

        return wrapper

    return decorator
