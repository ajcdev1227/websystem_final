import datetime
import os
import random
import shutil
import string
import subprocess
import time
import uuid
import base64

import jwt
from typing import Union
import sys, os, time, uuid
import authlib.jose

import nylas
import sendgrid as sendgrid
from django.contrib.auth import login, logout
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from icalendar import Calendar, Event
from jwt import InvalidSignatureError, ExpiredSignatureError, InvalidAlgorithmError
from nylas import APIClient
from sendgrid import Email, To, Content, Mail

import core.settings
from compliance.models import OfficerTenantAssignment
from core import settings
from home.constants import NYLAS_CLIENT_ID, NYLAS_CLIENT_SECRET, NYLAS_API_SERVER, LOGIN_TOKEN_SECRET, APP_DOMAIN, JITSI_APP_ID, JITSI_API_KEY_ID
import urllib.parse
from django.db import connection

from home.models import Client, CustomUser


_client_table = Client._meta.db_table
_customuser_table = CustomUser._meta.db_table
_officer_tenant_assignment_table = OfficerTenantAssignment._meta.db_table


def generate_short_uuid():
    # Generate a new UUID
    new_uuid = uuid.uuid4()

    # Convert the UUID to a short 6-character string
    short_uuid = str(new_uuid)[:6]

    # Return the short UUID
    return short_uuid


def take_page_screenshot(url: str, save_path: str):
    """
    Takes a screenshot of the provided URL and saves it to the specified path.
    Takes about 10 seconds to complete.
    """

    python = os.path.join(settings.BASE_DIR, 'env', 'Scripts', 'python')
    subprocess.run(
        [python, os.path.join(settings.BASE_DIR, 'screenshot_tool.py'), url, save_path, settings.CHROME_EXECUTABLE])


def send_email(to: str, subject: str, content: str, is_html: bool):
    """
    Sends an email using SendGrid.
    Uses the application's configured sender identity.
    """

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    from_email = Email(settings.SENDGRID_SENDER_IDENTITY)  # Change to your verified sender
    to_email = To(to)  # Change to your recipient
    mime = 'text/plain'
    if is_html:
        mime = 'text/html'
    content_res = Content(mime, content)
    mail = Mail(from_email, to_email, subject, content_res)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)

    if response.status_code > 299:
        raise IOError(
            f'Failed to send email via SendGrid because it returned status code {response.status_code} and headers {response.headers}')


def copy_file(src_file, dst_file):
    shutil.copy2(src_file, dst_file)


def generate_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def base64_encode(string):
    string_bytes = string.encode('utf-8')
    base64_bytes = base64.b64encode(string_bytes)
    uuid = base64_bytes.decode('utf-8')
    return uuid


def base64_decode(base64_str):
    base64_bytes = base64_str.encode('utf-8')
    decoded_bytes = base64.b64decode(base64_bytes)
    original_string = decoded_bytes.decode('utf-8')
    return original_string


def generate_calendar_invite(email):
    # Create the calendar object
    cal = Calendar()

    # Set the event details
    event = Event()
    event.add('summary', 'Example Event')
    event.add('email', email)
    event.add('description', 'This is an example event')
    event.add('dtstart', datetime.datetime(2022, 1, 1, 10, 0, 0))
    event.add('dtend', datetime.datetime(2022, 1, 1, 12, 0, 0))

    # Add the event to the calendar
    cal.add_component(event)

    decode_calendar_invite(cal.to_ical().decode('utf-8'))

    # Return the generated calendar invitation as a string
    return cal.to_ical().decode('utf-8')


def decode_calendar_invite(calendar_invite):
    # Parse the calendar invite string
    cal = Calendar.from_ical(calendar_invite)

    # Extract the event details from the calendar object
    event = cal.walk('VEVENT')[0]
    summary = event.get('summary')
    description = event.get('description')
    dtstart = event.get('dtstart').dt
    dtend = event.get('dtend').dt

    # Print the event details
    print("Summary:", summary)
    print("Description:", description)
    print("Start Date and Time:", dtstart)
    print("End Date and Time:", dtend)


def initialize_nylas_client():
    return APIClient(
        NYLAS_CLIENT_ID,
        NYLAS_CLIENT_SECRET,
        None,
        NYLAS_API_SERVER
    )


def only_alphabets(_string) -> string:
    _only_alphabets = ''.join([char for char in _string if char.isalpha()])
    return _only_alphabets.lower()


def create_login_token(user_email: string) -> string:
    """
    Creates a login token for a user.
    This token can be used to identify a user by email.
    """

    return jwt.encode(
        payload={
            'sub': user_email,
            'exp': int(time.time()) + 60,  # Tokens expire in 60 seconds
        },
        key=LOGIN_TOKEN_SECRET,
        algorithm='HS256',
    )


def decode_login_token(token: string) -> string:
    """
    Decodes a login token, returning the user email encoded in it.
    If it was invalid, it will raise InvalidAlgorithmError, InvalidSignatureError or ExpiredSignatureError.
    """

    return jwt.decode(token, key=LOGIN_TOKEN_SECRET, algorithms=['HS256'])['sub']


def create_auth_url(request: WSGIRequest, next_url: string, app_name: string = None) -> string:
    """
    Creates an auth URL for the current request that redirects to the specified URL.
    The returned URL will be to the auth page with a ?next= query parameter.
    """

    url = f"{request.scheme}://auth.{APP_DOMAIN}/signin?next={urllib.parse.quote(next_url)}"
    if app_name is not None:
        url += '&app=' + urllib.parse.quote(app_name)

    return url
    

def handle_auth_callback_request(request: WSGIRequest, next_url: string) -> Union[HttpResponse, HttpResponseRedirect]:
    """
    Takes in a request and performs logic necessary to act as an auth callback.
    An error message response and HTTP 400 will be returned if the token was invalid.

    If a "next" query parameter is present in the URL, it will redirect to that upon token validation.
    If none is present, the next_url argument will be used as the redirect.
    """
    token = request.GET.get('token')

    if token is None:
        return HttpResponse("Invalid token 1", status=400)

    try:
        email = decode_login_token(token)
    except (InvalidAlgorithmError, InvalidSignatureError, ExpiredSignatureError) as _:
        return HttpResponse("Invalid token 2", status=400)

    user = CustomUser.objects.filter(username=email).first()
    if user is None:
        return HttpResponse("Invalid token 3", status=400)

    login(request, user)

    next_url_param = request.GET.get('next')
    if next_url_param is None:
        return redirect(next_url)
    else:
        return redirect(next_url_param)


def handle_signin_redirect_request(request: WSGIRequest, callback_path: string, app_name: string = None) -> HttpResponseRedirect:
    """
    Handles an application's sign in page that requests get redirected to if they aren't authenticated.
    It returns a redirect to the auth site that will be directed to the specified auth callback path.
    The auth callback path should be a path relative to the current domain, e.g. "/dologin".
    """
    next_url = request.GET.get('next', request.headers.get('referer'))

    cb_url = request.build_absolute_uri(callback_path)
    if next_url is not None:
        if '?' in cb_url:
            cb_url += '&'
        else:
            cb_url += '?'

        cb_url += 'next=' + urllib.parse.quote(next_url)

    return redirect(create_auth_url(request, cb_url, app_name))


def handle_signout_redirect_request(request: WSGIRequest, next_url: string = None) -> HttpResponseRedirect:
    """
    Handles an application's sign out page.
    If next_url is not specified, the referrer URL will be used as the logout redirect URL, if any.
    If there is no next_url and or referrer, the base domain at root path will be used for the redirect.
    """
    logout(request)

    if next_url is None:
        next_url_res = request.headers.get('referer') or request.build_absolute_uri('/')
    else:
        next_url_res = next_url

    return redirect(f"{request.scheme}://auth.{APP_DOMAIN}/signout?next={urllib.parse.quote(next_url_res)}")


def is_req_user_officer(request: WSGIRequest) -> bool:
    """
    Returns whether the user associated with the request is a compliance officer
    """

    return request.user.is_authenticated and request.user.role == 4


class RawPaginator(Paginator):
    """
    Wrapper around Paginator that takes a count parameter and does not perform slicing.
    Useful for paginating resources returned by a raw query.

    Source: https://stackoverflow.com/a/36022955
    """

    def __init__(self, object_list, per_page, count, **kwargs):
        super().__init__(object_list, per_page, **kwargs)
        self.raw_count = count

    def _get_count(self):
        return self.raw_count
    count = property(_get_count)

    def page(self, number):
        number = self.validate_number(number)
        return self._get_page(self.object_list, number, self)


def filter_chars(input_string: string, chars_to_filter: string) -> string:
    """
    Filters out any of the specified characters from a string and returns the filtered version
    """

    translation_table = str.maketrans('', '', chars_to_filter)
    return input_string.translate(translation_table)

def get_tenant_id_by_company_id(company_id: int) -> int:
    """
    Fetches the tenant ID associated with the specified company ID.
    If none was found, None is returned.
    """

    sql = f'''
    select distinct {_client_table}.id from {_client_table}
    join {_customuser_table} on {_customuser_table}.username = {_client_table}.tenant_name
    where {_customuser_table}.company_id = %s
    limit 1
    '''
    params = [company_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    if res is None:
        return None
    else:
        return res[0]


def get_tenant_id_by_user_id(user_id: int) -> int:
    """
    Fetches the tenant ID associated with the specified user ID.
    If none was found, None is returned.
    """

    sql = f'''
    select distinct {_client_table}.id from {_client_table}
    join {_customuser_table} on {_customuser_table}.username = {_client_table}.tenant_name
    where {_customuser_table}.company_id = (select c.company_id from {_customuser_table} c where c.id = %s limit 1)
    limit 1
    '''
    params = [user_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    if res is None:
        return None
    else:
        return res[0]


def get_req_tenant_id(req: WSGIRequest) -> int:
    """
    Fetches the tenant ID associated with the current request's user.
    If the request is not authenticated or the user is not a tenant admin, it will return None.
    """

    if req.user.is_authenticated:
        return get_tenant_id_by_company_id(req.user.company_id)
    else:
        return None


def can_req_user_self_manage_compliance(req: WSGIRequest) -> bool:
    """
    Returns whether the current request's user can do self-managed compliance for his/her tenant.
    If the request is not authenticated, False will be returned.
    """
    if req.user.is_authenticated:
        sql = f'''
        select {_client_table}.enable_self_managed_compliance from {_client_table}
        where {_client_table}.tenant_name = %s
        limit 1
        '''
        params = [req.user.username]

        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            res = cursor.fetchone()

        if res is None:
            return False
        else:
            return res[0]
    else:
        return False


def update_user_enable_self_managed_compliance(username: str, enable: bool):
    """
    Updates whether self-managed compliance is enabled for the user with the specified username's tenant
    """
    sql = f'''
    update {_client_table}
    set enable_self_managed_compliance = %s
    where tenant_name = %s
    '''
    params = [enable, username]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)


def get_customer_ids_for_user_tenant(company_id: int) -> list[int]:
    """
    Gets all customer IDs of users in the same tenant as the user with the specified company ID
    """

    sql = f'''
    select customer_id from {_customuser_table} where company_id = %s
    '''
    params = [company_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    res: list[int] = []

    for row in rows:
        res.append(row[0])

    return res


def get_company_ids_for_officer_assigned_tenant(officer_id: int) -> list[int]:
    """
    Gets all company IDs of tenants assigned to the officer with the specified user ID
    """

    sql = f'''
    select {_customuser_table}.company_id from {_officer_tenant_assignment_table}
    join {_client_table} on {_client_table}.id = {_officer_tenant_assignment_table}.tenant_id
    join {_customuser_table} on {_customuser_table}.username = {_client_table}.tenant_name
    where {_officer_tenant_assignment_table}.officer_id = %s
    '''
    params = [officer_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    res: list[int] = []

    for row in rows:
        res.append(row[0])

    return res


def get_tenants_by_ids(tenant_ids: list[int]) -> list[Client]:
    """
    Returns all tenants with the specified tenant IDs.
    Order is not guaranteed.
    """

    if len(tenant_ids) < 1:
        return []

    sql = f'select * from {_client_table} where id in ('
    params = []

    for tenant_id in tenant_ids:
        sql += '%s, '
        params.append(tenant_id)

    sql = sql[:-2] + ')'

    return Client.objects.raw(sql, params)


def create_nylas_client() -> nylas.APIClient:
    """
    Creates a new Nylas API client using the application's configuration
    """

    return nylas.APIClient(
        os.environ.get("NYLAS_CLIENT_ID"),
        os.environ.get("NYLAS_CLIENT_SECRET"),
        api_server=os.environ.get("NYLAS_API_SERVER") or "https://api.nylas.com"
    )


def create_nylas_client_for_user(user: CustomUser) -> nylas.APIClient:
    """
    Creates a new Nylas API client using the application's configuration, and the user's access token.
    Raises ValueError if the user does not have a Nylas access token associated with it.
    """

    token = user.nylas_access_token

    if token is None or token == '':
        raise ValueError(f'The user with ID {user.id} has no Nylas access token associated with it')

    client = create_nylas_client()
    client.access_token = token

    return client


def meeting_link_for_id(id: str) -> str:
    """
    Creates an instant meeting link for the specified meeting ID
    """

    return f'https://home.{APP_DOMAIN}/meeting/{id}/'


def create_new_meeting() -> str:
    """
    Creates a new instant meeting and returns its ID.
    Use meeting_link_for_id to get the full link to the meeting.
    """

    return generate_random_string(20)


def create_new_meeting_and_return_link() -> str:
    """
    Creates a new instant meeting and returns the full link to it.
    Use create_new_meeting to only get its ID.
    """

    return meeting_link_for_id(create_new_meeting())


class JaaSJwtBuilder:
    """
        The JaaSJwtBuilder class helps with the generation of the JaaS JWT.
    """

    EXP_TIME_DELAY_SEC = 7200
    # Used as a delay for the exp claim value.

    NBF_TIME_DELAY_SEC = 10
    # Used as a delay for the nbf claim value.

    def __init__(self) -> None:
        self.header = { 'alg' : 'RS256' }
        self.userClaims = {}
        self.featureClaims = {}
        self.payloadClaims = {}

    def withDefaults(self):
        """Returns the JaaSJwtBuilder with default valued claims."""
        return self.withExpTime(int(time.time() + JaaSJwtBuilder.EXP_TIME_DELAY_SEC)) \
            .withNbfTime(int(time.time() - JaaSJwtBuilder.NBF_TIME_DELAY_SEC)) \
                .withLiveStreamingEnabled(True) \
                    .withRecordingEnabled(True) \
                        .withOutboundCallEnabled(True) \
                            .withTranscriptionEnabled(True) \
                                .withModerator(True) \
                                    .withRoomName('*') \
                                        .withUserId(str(uuid.uuid4()))

    def withApiKey(self, apiKey):
        """
        Returns the JaaSJwtBuilder with the kid claim(apiKey) set.

        :param apiKey A string as the API Key https://jaas.8x8.vc/#/apikeys
        """
        self.header['kid'] = apiKey
        return self

    def withUserAvatar(self, avatarUrl):
        """
        Returns the JaaSJwtBuilder with the avatar claim set.

        :param avatarUrl A string representing the url to get the user avatar.
        """
        self.userClaims['avatar'] = avatarUrl
        return self

    def withModerator(self, isModerator):
        """
        Returns the JaaSJwtBuilder with the moderator claim set.

        :param isModerator A boolean if set to True, user is moderator and False otherwise.
        """
        self.userClaims['moderator'] = isModerator == True
        return self

    def withUserName(self, userName):
        """
        Returns the JaaSJwtBuilder with the name claim set.

        :param userName A string representing the user's name.
        """
        self.userClaims['name'] = userName
        return self

    def withUserEmail(self, userEmail):
        """
        Returns the JaaSJwtBuilder with the email claim set.

        :param userEmail A string representing the user's email address.
        """
        self.userClaims['email'] = userEmail
        return self

    def withLiveStreamingEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the livestreaming claim set.

        :param isEnabled A boolean if set to True, live streaming is enabled and False otherwise.
        """
        self.featureClaims['livestreaming'] = isEnabled == True
        return self

    def withRecordingEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the recording claim set.

        :param isEnabled A boolean if set to True, recording is enabled and False otherwise.
        """
        self.featureClaims['recording'] = isEnabled == True
        return self

    def withTranscriptionEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the transcription claim set.

        :param isEnabled A boolean if set to True, transcription is enabled and False otherwise.
        """
        self.featureClaims['transcription'] = isEnabled == True
        return self

    def withOutboundCallEnabled(self, isEnabled):
        """
        Returns the JaaSJwtBuilder with the outbound-call claim set.

        :param isEnabled A boolean if set to True, outbound calls are enabled and False otherwise.
        """
        self.featureClaims['outbound-call'] = 'true' if isEnabled == True else 'false'
        return self

    def withExpTime(self, expTime):
        """
        Returns the JaaSJwtBuilder with exp claim set. Use the defaults, you won't have to change this value too much.

        :param expTime Unix time in seconds since epochs plus a delay. Expiration time of the JWT.
        """
        self.payloadClaims['exp'] = expTime
        return self

    def withNbfTime(self, nbfTime):
        """
        Returns the JaaSJwtBuilder with nbf claim set. Use the defaults, you won't have to change this value too much.

        :param nbfTime Unix time in seconds since epochs.
        """
        self.payloadClaims['nbf'] = nbfTime
        return self

    def withRoomName(self, roomName):
        """
        Returns the JaaSJwtBuilder with room claim set.

        :param roomName A string representing the room to join.
        """
        self.payloadClaims['room'] = roomName
        return self

    def withAppID(self, AppId):
        """
        Returns the JaaSJwtBuilder with the sub claim set.

        :param AppId A string representing the unique AppID (previously tenant).
        """
        self.payloadClaims['sub'] = AppId
        return self

    def withUserId(self, userId):
        """
        Returns the JaaSJwtBuilder with the id claim set.

        :param A string representing the user, should be unique from your side.
        """
        self.userClaims['id'] = userId
        return self

    def signWith(self, key):
        """
        Returns a signed JWT.

        :param key A string representing the private key in PEM format.
        """
        context = { 'user': self.userClaims, 'features': self.featureClaims }
        self.payloadClaims['context'] = context
        self.payloadClaims['iss'] = 'chat'
        self.payloadClaims['aud'] = 'jitsi'
        return authlib.jose.jwt.encode(header=self.header, payload=self.payloadClaims, key=key)


def create_jaas_jwt(user_name: str, user_email: str, is_moderator: bool) -> str:
    """
    Creates a new JaaS JWT
    """

    with open(os.path.join(settings.BASE_DIR, 'jaas.pk'), 'r') as reader:
        private_key = reader.read()

    builder = JaaSJwtBuilder()

    token = builder \
        .withDefaults() \
        .withUserName(user_name) \
        .withUserEmail(user_email) \
        .withModerator(is_moderator) \
        .withApiKey(JITSI_API_KEY_ID) \
        .withAppID(JITSI_APP_ID) \
        .signWith(private_key)

    return token.decode()
