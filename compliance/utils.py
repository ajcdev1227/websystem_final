import string

import wagtail.models
from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import RawQuerySet

from compliance.models import Case, OfficerTenantAssignment
from django.db import connection

from home.models import Client, CustomUser
from home.utils import get_req_tenant_id, get_tenant_id_by_company_id, get_tenant_id_by_user_id

_case_table = Case._meta.db_table
_client_table = Client._meta.db_table
_customuser_table = CustomUser._meta.db_table
_officer_tenant_assignment_table = OfficerTenantAssignment._meta.db_table


def get_cases_count_for_user_id(user_id: int, status: string = None, not_statuses: list[str] = [], search_query: string = None) -> int:
    """
    Fetches the total number of cases (optionally with the specified status) associated with the specified user (CustomUser) ID.
    This is not the same as fetching cases assigned to an officer user, this fetches cases associated with the tenant that the user belongs to.
    To fetch cases assigned to an officer, use `get_cases_count_assigned_to_officer`.

    If search_query is not None and not empty, the results will be filtered by the specified plaintext query.
    """

    sql = f'''
    select count(*) from {_case_table}
    join {_client_table} on {_client_table}.id = {_case_table}.tenant_id
    join {_customuser_table} on {_customuser_table}.username = {_client_table}.tenant_name
    where {_customuser_table}.id = %s
    '''
    params = [user_id]

    if status is not None:
        sql += f'\nand {_case_table}.status = %s'
        params.append(status)

    for ns in not_statuses:
        sql += f'\nand {_case_table}.status != %s'
        params.append(ns)

    if search_query is not None and search_query != '':
        sql += f'\nand to_tsvector(\'english\', {_case_table}.resource_title || \' \' || {_case_table}.resource_key) @@ plainto_tsquery(%s)'
        params.append(search_query)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    return res[0]


def get_cases_count_assigned_to_officer(officer_user_id: int, status: string = None, not_statuses: list[str] = [], search_query: string = None) -> int:
    """
    Fetches the total number of cases (optionally with the specified status) assigned to the specified compliance officer user (CustomUser) ID.
    If search_query is not None and not empty, the results will be filtered by the specified plaintext query.
    """

    sql = f'''
    select count(*) from {_officer_tenant_assignment_table}
    join {_client_table} on {_client_table}.id = {_officer_tenant_assignment_table}.tenant_id
    join {_case_table} on {_case_table}.tenant_id = {_client_table}.id
    where {_officer_tenant_assignment_table}.officer_id = %s
    '''
    params = [officer_user_id]

    if status is not None:
        sql += f'\nand {_case_table}.status = %s'
        params.append(status)

    for ns in not_statuses:
        sql += f'\nand {_case_table}.status != %s'
        params.append(ns)

    if search_query is not None and search_query != '':
        sql += f'\nand to_tsvector(\'english\', {_case_table}.resource_title || \' \' || {_case_table}.resource_key) @@ plainto_tsquery(%s)'
        params.append(search_query)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    return res[0]


def get_cases_for_user_id_by_status(user_id: int, status: string, not_statuses: list[str], offset: int, limit: int, search_query: string = None) -> RawQuerySet:
    """
    Fetches cases (optionally with the specified status) associated with the specified user (CustomUser) ID.
    This is not the same as fetching cases assigned to an officer user, this fetches cases associated with the tenant that the user belongs to.
    To fetch cases assigned to an officer, use `get_cases_assigned_to_officer`.

    If search_query is not None and not empty, the results will be filtered by the specified plaintext query.

    Cases are ordered by their creation date, descending.
    """

    sql = f'''
    select distinct {_case_table}.* from {_case_table}
    join {_client_table} on {_client_table}.id = {_case_table}.tenant_id
    join {_customuser_table} on {_customuser_table}.username = {_client_table}.tenant_name
    where {_customuser_table}.id = %s
    '''
    params = [user_id]

    Case.objects.filter()

    if status is not None:
        sql += f'\nand {_case_table}.status = %s'
        params.append(status)

    if search_query is not None and search_query != '':
        sql += f'\nand to_tsvector(\'english\', {_case_table}.resource_title || \' \' || {_case_table}.resource_key) @@ plainto_tsquery(%s)'
        params.append(search_query)

    for ns in not_statuses:
        sql += f'\nand {_case_table}.status != %s'
        params.append(ns)

    sql += f'''
    order by {_case_table}.created_ts desc
    offset (%s) limit (%s)
    '''

    params.append(offset)
    params.append(limit)

    return Case.objects.raw(sql, params)


def get_cases_assigned_to_officer(officer_user_id: int, status: string, not_statuses: list[str], offset: int, limit: int, search_query: string = None) -> RawQuerySet:
    """
    Fetches cases (optionally with the specified status) assigned to the specified compliance officer user (CustomUser) ID.
    If search_query is not None and not empty, the results will be filtered by the specified plaintext query.

    Cases are ordered by their creation date, descending.
    """

    sql = f'''
    select distinct {_case_table}.* from {_officer_tenant_assignment_table}
    join {_client_table} on {_client_table}.id = {_officer_tenant_assignment_table}.tenant_id
    join {_case_table} on {_case_table}.tenant_id = {_client_table}.id
    where {_officer_tenant_assignment_table}.officer_id = %s
    '''
    params = [officer_user_id]

    if status is not None:
        sql += f'\nand {_case_table}.status = %s'
        params.append(status)

    if search_query is not None and search_query != '':
        sql += f'\nand to_tsvector(\'english\', {_case_table}.resource_title || \' \' || {_case_table}.resource_key) @@ plainto_tsquery(%s)'
        params.append(search_query)

    for ns in not_statuses:
        sql += f'\nand {_case_table}.status != %s'
        params.append(ns)

    sql += f'''
    order by {_case_table}.created_ts desc
    offset (%s) limit (%s)
    '''

    params.append(offset)
    params.append(limit)

    return Case.objects.raw(sql, params)


def submit_wagtail_page_revision_to_compliance(
        user: CustomUser,
        revision: wagtail.models.Revision,
        page: wagtail.models.Page
):
    """
    Submits a Wagtail page revision to compliance
    """

    # Construct resource key (object ID + revision)
    resource_key = str(revision.object_id)

    # Check for existing pending case and update its updated_ts column if it does exist
    existing_case = Case.objects.filter(resource_key=resource_key, status='pending').first()

    rev_json = serializers.serialize('json', [revision], ensure_ascii=False)

    if existing_case is None:
        Case.objects.create(
            resource_title=page.title,
            resource_key=resource_key,
            type='cms',
            status='pending',
            resource_snapshot=rev_json,
            tenant_id=get_tenant_id_by_company_id(user.company_id)
        ).save()
    else:
        existing_case.resource_title = page.title
        existing_case.resource_snapshot = rev_json
        existing_case.save()


def get_schema_for_case_id(case_id: int) -> string:
    """
    Fetches the schema name associated with the tenant who created the case with the specified ID.
    If the case does not exist, None will be returned.
    """
    sql = f'''
    select {_client_table}.schema_name from {_case_table}
    join {_client_table} on {_client_table}.id = {_case_table}.tenant_id
    where {_case_table}.id = %s
    '''
    params = [case_id]

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        res = cursor.fetchone()

    if res is None:
        return None
    else:
        return res[0]


class ComplianceException(Exception):
    """
    Exception raised when something compliance-related goes wrong
    """
    pass


def publish_case(case: Case):
    """
    Takes a compliance case and publishes it on Wagtail.

    Note some possible edge cases:
     - The page doesn't exist anymore
     - The page type changed

    The above conditions may cause trouble for this function.

    The case will not be modified. It is up to the caller to change the case's status and save it.

    This function will raise ComplianceException if anything specific to its logic goes wrong.
    """

    case_schema = get_schema_for_case_id(case.id)

    # Deserialize case revision
    revision = None
    for rev in serializers.deserialize('json', case.resource_snapshot):
        revision = rev.object
        break

    if revision is None:
        raise ComplianceException(
            f'Error: Could not extract page data from case. Please contact support to resolve this issue.')

    content_type_class = revision.content_type.model_class()
    content_type_table = f'"{case_schema}".{content_type_class._meta.db_table}'
    wagtail_page_table = f'"{case_schema}".{wagtail.models.Page._meta.db_table}'

    page_id = int(revision.object_id)

    with connection.cursor() as cursor:
        cursor.execute(
            f'select id from {wagtail_page_table} where id = %s',
            [page_id],
        )
        if cursor.fetchone() is None:
            raise ComplianceException(
                'No matching page for case was found. Please contact support to resolve this issue.')

    # Replace page body
    with connection.cursor() as cursor:
        _body = revision.content['body']
        _id = page_id
        cursor.execute(
            f'''
            insert into {content_type_table} (page_ptr_id, body)
            values (%s, %s)
            on conflict (page_ptr_id)
            do update set body = %s
            ''',
            [_id, _body, _body],
        )

    # Update page metadata and go live
    with connection.cursor() as cursor:
        _content = revision.content
        cursor.execute(
            f'''
            update {wagtail_page_table} set
                path = %s,
                depth = %s,
                numchild = %s,
                title = %s,
                slug = %s,
                live = true,
                url_path = %s,
                seo_title = %s,
                show_in_menus = %s,
                search_description = %s,
                go_live_at = %s,
                expire_at = %s,
                content_type_id = %s,
                locked = false,
                latest_revision_created_at = now(),
                last_published_at = now(),
                locked_at = null,
                locked_by_id = null,
                translation_key = %s
            where id = %s
            ''',
            [
                _content['path'],
                _content['depth'],
                _content['numchild'],
                _content['title'],
                _content['slug'],
                _content['url_path'],
                _content['seo_title'],
                _content['show_in_menus'],
                _content['search_description'],
                _content['go_live_at'],
                _content['expire_at'],
                revision.content_type_id,
                _content['translation_key'],
                page_id,
            ]
        )
