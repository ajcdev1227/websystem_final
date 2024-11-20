from typing import Optional

from django.db import connection
from django.http import JsonResponse
from os import getenv

from django.utils.connection import ConnectionProxy
from rest_framework.serializers import Serializer

from home.models import Client, CustomUser

_client_table = Client._meta.db_table
_customuser_table = CustomUser._meta.db_table


VALID_API_KEYS = [key.strip() for key in getenv('INTEGRATION_API_KEYS').split(',') if key.strip() != '']


def api_success_response(status: int = 200, data=None) -> JsonResponse:
    """
    Returns an API success response, optionally with the specified status and data.
    The JSON response data will be the value of `data` if not None.
    """

    if data is None:
        data = {}

    return JsonResponse(data, status=status)


def api_error_response(status: int, msg: str, data=None) -> JsonResponse:
    """
    Returns an API error response with the specified status, and optionally specified extra data.
    The JSON response format is as follows:

    {
        "detail": string,
        "data": any | null,
    }
    """

    return JsonResponse({
        'detail': msg,
        'data': data,
    }, status=status)


def api_bad_request_response(data=None) -> JsonResponse:
    """
    Returns an API Bad Request response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(400, 'Bad Request', data)


def api_unauthorized_response(data=None) -> JsonResponse:
    """
    Returns an API Unauthorized response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(401, 'Unauthorized', data)


def api_forbidden_response(data=None) -> JsonResponse:
    """
    Returns an API Forbidden response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(403, 'Forbidden', data)


def api_not_found_response(data=None) -> JsonResponse:
    """
    Returns an API Not Found response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(404, 'Not Found', data)


def api_method_not_allowed_response(data=None) -> JsonResponse:
    """
    Returns an API Method Not Allowed response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(405, 'Method Not Allowed', data)


def api_internal_error_response(data=None) -> JsonResponse:
    """
    Returns an API Internal Error response, optionally with the specified extra data.
    The API response format is the same as that of `api_error_response`.
    """

    return api_error_response(500, 'Not Found', data)


def api_serializer_validation_error_response(serializer: Serializer) -> JsonResponse:
    """
    Returns an API error containing information about a Serializer's validation error(s).
    The API response format is as follows:

    {
        "detail": string,
        "data": {
            "errors": {
                [key: string]: string[]
            }
        }
    }
    """

    msg = ', '.join([f'{x}: {serializer.errors[x][0]}' for x in serializer.errors.keys()])

    return api_error_response(400, msg, {'errors': serializer.errors})


def is_token_valid(token: str) -> bool:
    """
    Returns whether the provided API token is valid
    """

    return token in VALID_API_KEYS


def fetch_schema_by_customer_id(customer_id: str) -> Optional[str]:
    """
    Fetches a user's schema name based on the provided customer ID
    """

    sql = f'''
    select {_client_table}.schema_name from {_client_table}
    join {_customuser_table} on {_client_table}.tenant_name = {_customuser_table}.username
    where {_customuser_table}.customer_id = %s
    limit 1
    '''
    params = [customer_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    if res is None:
        return None
    else:
        return res[0]


def set_connection_schema(conn: ConnectionProxy, schema: str, include_public: bool = True):
    """
    Sets the schema of the provided connection
    """

    conn.set_schema(schema, include_public=include_public)


def set_connection_schema_by_customer_id(conn: ConnectionProxy, customer_id: str, include_public: bool = True) -> Optional[str]:
    """
    Sets the schema of the provided connection to the schema for the customer with the specified ID.
    If the customer exists, the schema will be set and its name will be returned.
    If the customer does not exist, nothing will be set and None will be returned.
    """

    schema = fetch_schema_by_customer_id(customer_id)

    if schema is None:
        return None

    set_connection_schema(conn, schema, include_public=include_public)

    return schema
