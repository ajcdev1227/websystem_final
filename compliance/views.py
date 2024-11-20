import datetime
import urllib.parse
from math import ceil

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from wagtail.models import Revision

from compliance.models import VALID_CASE_STATUSES, Case, OfficerTenantAssignment
from compliance.utils import get_cases_count_assigned_to_officer, \
    get_cases_assigned_to_officer, get_cases_for_user_id_by_status, get_cases_count_for_user_id, publish_case, \
    ComplianceException
from crm import fetch_all_crm_compliance_cases, CrmComplianceCase, fetch_crm_compliance_case_by_id, crm_case_to_case, \
    approve_crm_compliance_case, reject_crm_compliance_case, fetch_crm_case_item
from home.decorators import unauthenticated_user
from home.utils import handle_auth_callback_request, handle_signin_redirect_request, handle_signout_redirect_request, \
    RawPaginator, is_req_user_officer, can_req_user_self_manage_compliance, \
    get_company_ids_for_officer_assigned_tenant, get_tenants_by_ids
from home.models import Client, CustomUser


# Create your views here.


@unauthenticated_user
def sign_in(request: WSGIRequest):
    return handle_signin_redirect_request(request, '/dologin', 'compliance')


def dologin(request: WSGIRequest):
    return handle_auth_callback_request(request, '/')


# NOTE, this is using a function from home.utils, to handle global logout.
def sign_out(request: WSGIRequest) -> HttpResponseRedirect:
    return handle_signout_redirect_request(request)


# ===================================== SIGN UP PAGE =========================================
def sign_up(request: WSGIRequest):
    pass


# ======================================= LISTINGS ===========================================

def listings_page_logic(request: WSGIRequest, page_type: str) -> HttpResponse:
    is_officer = is_req_user_officer(request)

    user: CustomUser = request.user
    user_id = user.id

    # TODO Revert this
    can_user_self_manage = can_req_user_self_manage_compliance(request)
    #can_user_self_manage = True

    if request.method == "POST":
        action = request.POST.get('action')

        # Fetch case
        case_id = request.POST.get('case-uuid')

        crm_case: CrmComplianceCase = None

        # Check ID type
        if case_id.startswith('crm:'):
            crm_case = fetch_crm_compliance_case_by_id(int(case_id[4:]))

            case = crm_case_to_case(crm_case)

            # TODO Validate this later
            can_manage_case = True
        else:
            case = Case.objects.filter(uuid=case_id).first()

            if can_user_self_manage:
                user_tenant = Client.objects.filter(tenant_name=user.username).first()

                can_manage_case = case.tenant_id == user_tenant.id
            elif is_officer:
                can_manage_case = OfficerTenantAssignment.objects.filter(
                    tenant_id=case.tenant_id,
                    officer_id=user_id,
                ).exists()
            else:
                can_manage_case = False

        # Check if an action can be performed on the case by the user
        if case is not None and case.status == 'pending' and can_manage_case:
            if case.type == 'cms':
                if action == 'approve':
                    try:
                        publish_case(case)
                    except ComplianceException as e:
                        return HttpResponse(str(e), status=500)

                    case.status = 'approved'
                    case.approved_ts = datetime.datetime.now()
                    case.reviewed_by = user
                    case.save()

                    # TODO Show message about it being successfully approved and is now live

                elif action == 'reject':
                    # Get reason, or None if empty
                    reason = request.POST.get('reason', '').strip()
                    if reason == '':
                        reason = None

                    case.status = 'rejected'
                    case.rejected_ts = datetime.datetime.now()
                    case.officer_notes = reason
                    case.reviewed_by = user
                    case.save()

                    # TODO Show message about the case being rejected

            elif case.type == 'crm':
                if action == 'approve':
                    approve_crm_compliance_case(crm_case)

                elif action == 'reject':
                    reject_crm_compliance_case(crm_case, note = request.POST.get('reason', '').strip())

            else:
                return HttpResponse(
                    f'Error: Unknown case type "{case.type}". Please contact support to resolve this issue.',
                    status=500)

    # Presentation code

    if page_type == 'archive':
        default_case_status = None
        case_not_statuses = ['pending']
    else:
        # Default page type is queue
        page_type = 'queue'
        default_case_status = 'pending'
        case_not_statuses = []

    case_status = request.GET.get('status', default_case_status)

    # Invalid status will remove case status filter altogether (e.g. using "any" to show all)
    if case_status not in VALID_CASE_STATUSES:
        case_status = None

    query = request.GET.get('q', '').strip()

    # Get all related CRM cases
    # TODO Rework all of this when feasible
    if is_officer:
        company_ids = [str(x) for x in get_company_ids_for_officer_assigned_tenant(user.id)]
    else:
        company_ids = [str(user.company_id)]

    crm_cases = fetch_all_crm_compliance_cases()
    # TODO Uncomment this once done testing
    crm_cases: list[CrmComplianceCase] = list(filter(lambda x: x.acx_customer_id in company_ids and (case_status is None or x.status == case_status), crm_cases))

    # Fetch total pending cases
    if is_officer:
        total_cases = get_cases_count_assigned_to_officer(user_id, case_status, case_not_statuses, query)
    else:
        total_cases = get_cases_count_for_user_id(user_id, case_status, case_not_statuses, query)

    total_cases += len(crm_cases)

    # TODO Change this to a reasonable number later
    page_size = 999

    # Figure out page number
    page = int(request.GET.get('page', 1))

    total_pages = ceil(total_cases / page_size)

    if page > total_pages:
        page = total_pages

    if page < 1:
        page = 1

    offset = (page - 1) * page_size

    if is_officer:
        cases: list[Case] = list(get_cases_assigned_to_officer(user_id, case_status, case_not_statuses, offset, page_size, query))
    else:
        cases: list[Case] = list(get_cases_for_user_id_by_status(user_id, case_status, case_not_statuses, offset, page_size, query))

    # Fetch tenants for cases because they're not set up
    case_tenant_ids = [x.tenant_id for x in cases]
    case_tenants = get_tenants_by_ids(case_tenant_ids)
    for case in cases:
        for ct in case_tenants:
            if ct.id == case.tenant_id:
                case.tenant = ct
                break

    # Add cases from CRM
    for crm_case in crm_cases:
        cases.append(crm_case_to_case(crm_case))

    # Process officer notes in cases to URL-encode them.
    # This is necessary for putting them into JavaScript safely.
    # We would base64 encode them, but the browser's default decoder can't handle unicode properly.
    for case in cases:
        if case.officer_notes is None:
            case.officer_notes = ''
        else:
            case.officer_notes = urllib.parse.quote(case.officer_notes)

    paginator = RawPaginator(cases, page_size, total_cases)

    context = {
        'posts': paginator.page(page),
        'query': query,
        'total_cases': total_cases,
        'can_manage_cases': (page_type == 'queue') and (is_officer or can_user_self_manage),
        'page_type': page_type,
    }
    return render(request, 'compliance/compliance.html', context)


@login_required(login_url='/signin')
def dashboard(request: WSGIRequest) -> HttpResponse:
    return listings_page_logic(request, 'queue')


@login_required(login_url='/signin')
def archive(request: WSGIRequest) -> HttpResponse:
    return listings_page_logic(request, 'archive')


def preview_page_logic(request: WSGIRequest, uuid: str, is_embed: bool) -> HttpResponse:
    # TODO IMPORTANT SECURITY PROBLEM TO ADDRESS: Validate that the user is allowed to preview this
    # TODO IMPORTANT SECURITY PROBLEM TO ADDRESS: Put preview on separate domain to avoid malicious JavaScript

    # Hack to avoid preview problems
    request.META['DISABLE_X_FRAME_OPTIONS'] = True

    title = 'No Title Available'
    iframe_src = '/preview/' + uuid + '/embed'
    headers = {}
    html = ''

    if uuid.startswith('crm:'):
        crm_case = fetch_crm_compliance_case_by_id(int(uuid[4:]))

        crm_item = fetch_crm_case_item(crm_case)

        if is_embed:
            html = crm_item.body
            headers['Content-Security-Policy'] = "default-src 'self';"
        else:
            if crm_item.subject is None:
                title = crm_case.type
            else:
                title = crm_item.subject
    else:
        case = Case.objects.filter(uuid=uuid).first()

        if is_embed:
            # TODO Figure out how to do Wagtail preview here

            revs = list(Revision.objects.all())

            # TODO Remove this
            print(revs)

            html = 'Preview cannot be shown at the moment. Please contact support.'
        else:
            title = case.resource_title

    # If it didn't return by now, it was either invalid or is a template that needs to be rendered
    if is_embed:
        return HttpResponse(
            html,
            status=404,
            headers=headers,
        )
    else:
        return render(request, 'compliance/preview.html', {'title': title, 'iframe_src': iframe_src})


@login_required(login_url="/signin")
def preview(request: WSGIRequest, uuid: str) -> HttpResponse:
    return preview_page_logic(request, uuid, is_embed=False)


@login_required(login_url="/signin")
def preview_embed(request: WSGIRequest, uuid: str) -> HttpResponse:
    return preview_page_logic(request, uuid, is_embed=True)
