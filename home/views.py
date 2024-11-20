import requests
import glob
import hashlib
import hmac
import json
import os
import re
import time
import subprocess

import facebook
from core import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponse, \
    HttpResponseBadRequest
from django.shortcuts import render, redirect
from django_tenants.utils import schema_context
from django.urls import reverse
# from django.utils import timezone
from django.utils import timezone as django_timezone
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from icalendar import Calendar, Event
from nylas import APIClient
from pytz import timezone
from datetime import datetime, timedelta, date
from dotenv import load_dotenv
from rest_framework import serializers


from adminapp.models import AvailableTime
from core.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from home.constants import COMPLIANCE_STATUS, NYLAS_CLIENT_SECRET, NYLAS_CLIENT_ID, APP_DOMAIN, APP_HOST, CRM_ROOT, \
    JITSI_API_KEY_ID
from home.decorators import approved_required
from home.forms import DateTimeForm, CompanyForm, CustomUserForm, WebsiteSettingsForm
from home.models import (
    CustomUser, Company, Pages,
    Slug, Submission, ScheduleMeeting,
    Article, Client, Domain,
    TenantUser, Meetings, EventType, EventBooking
)
from wagtailcms.models import WebsiteSettings
from virtual_calendar.models.calendar_profiles import CalendarProfile

load_dotenv()  # take environment variables from .env.

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


# =====================================  USER SIGN IN PAGE =========================================
from home.utils import generate_short_uuid, take_page_screenshot, send_email, base64_encode, generate_calendar_invite, \
    generate_random_string, initialize_nylas_client, only_alphabets, \
    handle_auth_callback_request, create_auth_url, create_login_token, handle_signin_redirect_request, \
    handle_signout_redirect_request, create_nylas_client_for_user, create_new_meeting_and_return_link, \
    create_new_meeting, meeting_link_for_id, create_jaas_jwt


def dologin(request):
    return handle_auth_callback_request(request, '/')


def docmslogin(request):
    return handle_auth_callback_request(request, '/cms/')


def sign_in(request):
    return handle_signin_redirect_request(request, '/dologin')


# ===================================== SIGN UP PAGE =========================================
def sign_up(request):
    if request.method == "GET":
        return render(request, 'auth/signup.html')
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        phonenumber = request.POST.get('phonenumber')
        company = request.POST.get('company')
        c_members = request.POST.get('c_members')
        customer_id = generate_short_uuid()
        hash_password = make_password(password)

        user = CustomUser(
            email=email,
            username=email,
            display_name=username,
            password=hash_password,
            phonenumber=phonenumber,
            c_members=c_members,
            customer_id=customer_id,
            is_superuser=1,
        )
        user.save()

        tenant_identifier = f"{only_alphabets(username)}-{customer_id}"
        tenant = Client(
            schema_name=tenant_identifier,
            tenant_name=user.username,
            domain_url=f'{tenant_identifier}.{APP_DOMAIN}',
            domain_host=f'{tenant_identifier}.{APP_HOST}',
            paid_until='2100-12-05',
            on_trial=True
        )
        tenant.save()

        user.domain_url = f'{tenant_identifier}.{APP_DOMAIN}'
        user.save()

        domain = Domain(
            domain=tenant.domain_host,
            tenant=tenant,
            is_primary=True
        )
        domain.save()

        tenant_user = TenantUser(
            user=user,
            tenant=tenant,
            is_active=True
        )
        tenant_user.save()

        user = authenticate(username=email, password=password)

        if user is not None:
            direct_url = f"{request.scheme}://{user.tenantuser.tenant.domain_url}"
            # login(request, user)
            return JsonResponse({
                "data": {
                    'tenant_url': direct_url
                },
                "message": "",
                "status": "success"
            }, status=200)
        else:
            return JsonResponse({
                "data": 1,
                "message": "",
                "status": "errors"
            }, status=200)


# ===================================== Tenant USER LOGOUT ================================================
@login_required(login_url='/signin')
def sign_out(request):
    return handle_signout_redirect_request(request)


# ===================================== DASHBOARD PAGE ================================================
# @approved_required # required for new onboarding users nylas
@login_required(login_url='/signin')
def dashboard(request):
    # url = send_post_request(request.user.company.id, request.user.email)
    # return redirect(url)
    return render(request, 'pages-green/dashboard.html', {'title': 'Dashboard'})


# ===================================== WEBSITE PAGE ================================================
@login_required(login_url='/signin')
def website(request):
    return render(request, 'pages/wesite.html', {'title': 'Website Engine'})


# === BOOKING PAGE === #
# def user_booking_page(request,unique_identifier):
#     try:
#         user_profile = UserProfile.objects.get(unique_identifier=unique_identifier)
#         user = user_profile.user
#         visible_meetings = user.user_meetings.filter(is_hidden=False)
#         context = {
#             'user': user,
#             'visible_meetings': visible_meetings
#         }
#         return render(request, 'pages/booking_page.html', context)
#     except UserProfile.DoesNotExist:
#         return HttpResponseNotFound("User not found")
#
# def booking_calendar(request):
#     pass


# FOR CRM ACCOUNT PROVISIONING
def send_post_request(acx_customer_id,email_input):
    ACX_KEY = os.getenv('ACX_KEY', None)
    php_url =  CRM_ROOT + '/scripts/_acx-user-login.php'
    query_string = {
        "acx_customer_id": acx_customer_id,
        "email": email_input,
        "acx_key":ACX_KEY
    }
    response = requests.post(php_url, data=query_string).json()['tk']
    token_acx = response['token_acx']
    user_id_acx = response['user_id_acx']
    url = f"{CRM_ROOT}/login-acx.php?token_acx={token_acx}&user_id_acx={user_id_acx}"
    return url


# ===================================== CONTACTS PAGE ================================================
@login_required(login_url='/signin')
def contacts(request):
    url = send_post_request(request.user.company.id, request.user.email)
    return redirect(url)
    # return render(request, 'pages/contacts.html', {'title': 'Contact Management'})


# ===================================== GROUPS PAGE ================================================
@login_required(login_url='/signin')
def groups(request):
    return render(request, 'pages/groups.html')


# ===================================== EMAIL PAGE ================================================
@login_required(login_url='/signin')
def email(request):
    return render(request, 'pages/email.html')


# ===================================== FORM PAGE ================================================
@login_required(login_url='/signin')
def forms(request):
    return render(request, 'pages/forms.html')


# ===================================== CHAT PAGE ================================================
@login_required(login_url='/signin')
def chat(request):
    return render(request, 'pages/chat.html')


# ===================================== MEETINGS PAGE ================================================
@login_required(login_url='/signin')
def meetings(request):
    return render(request, 'pages/meeting.html')


# This is for the /bookings page for each user's tenant
@login_required(login_url='/signin')
def meeting_bookings(request: WSGIRequest) -> HttpResponse:
    user: CustomUser = request.user
    context = get_base_meetings_context(request)

    # Set variable for current time
    current_time = django_timezone.now()

    # Filter it by the user and the end time being less than current time, and order it by the booked from latest
    past_bookings = EventBooking.objects.filter(event_type__user=user, end_ts__lte=current_time).order_by("-pk")

    # Filter it by user and the end time being greater than current time, and order it by the booked from latest
    upcoming_bookings = EventBooking.objects.filter(event_type__user=user, end_ts__gte=current_time).order_by("-pk")

    for booking in past_bookings:
        if booking.meeting_id:
            booking.meeting_link = meeting_link_for_id(booking.meeting_id)
        else:
            # if you dont have an ID you can go into Events and make an event / meeting
            booking.meeting_link = ''

    for booking in upcoming_bookings:
        if booking.meeting_id:
            booking.meeting_link = meeting_link_for_id(booking.meeting_id)
        else:
            booking.meeting_link = ''

    context.update(
        {
            "past_bookings": past_bookings,
            "upcoming_bookings": upcoming_bookings,
        }
    )

    return render(request, "pages/meeting_bookings.html", context=context)


@login_required(login_url='/signin')
def meeting_details(request: WSGIRequest, slug) -> HttpResponse:
    context = get_base_meetings_context(request)

    # Fetch user's bookings
    booking = EventType.objects.filter(slug=slug).first()

    context['self'] = booking

    return render(request, "pages/meeting_details.html", context=context)


@login_required(login_url='/signin')
def meeting_availability(request):
    return render(request,"pages/meeting_availability.html", context=get_base_meetings_context(request))


# ===================================== compliance PAGE ================================================
@login_required(login_url='/signin')
def compliance(request):
    if request.method == "GET":
        user_id = request.user.id
        compliance_list = Submission.objects.filter(submitter_id=user_id) \
            .filter(Q(status=COMPLIANCE_STATUS['pending']) | Q(status=COMPLIANCE_STATUS['denied'])).order_by('-id')
        query = request.GET.get('q')
        if query:
            compliance_list = Submission.objects \
                .filter(submitter_id=user_id) \
                .filter(~Q(status=None)) \
                .filter(slug__contains=query) \
                .order_by('-id')

        paginator = Paginator(compliance_list, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'posts': posts
        }
        return render(request, 'pages/compliance.html', context)


# ===================================== archive PAGE ================================================
@login_required(login_url='/signin')
def archive(request):
    if request.method == "GET":
        user_id = request.user.id

        Submission.objects.filter(submitter_id=user_id) \
            .filter(status=COMPLIANCE_STATUS["approved"]).update(checked=1)

        compliance_list = Submission.objects.filter(submitter_id=user_id) \
            .filter(status=COMPLIANCE_STATUS["approved"]).order_by('-approved_ts')
        query = request.GET.get('q')
        if query:
            compliance_list = Submission.objects \
                .filter(submitter_id=user_id) \
                .filter(~Q(status=None)) \
                .filter(slug__contains=query) \
                .order_by('-approved_ts')

        paginator = Paginator(compliance_list, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'posts': posts
        }
        return render(request, 'pages/archive.html', context)


# ===================================== settings PAGE ================================================
@login_required(login_url='/signin')
def settingss(request):
    return render(request, 'pages/settings.html')


# ===================================== editor list PAGE ================================================
@login_required(login_url='/signin')
def editor_list(request):
    # queue_list = Pages.objects.filter(user=request.user).order_by('-id')
    # query = request.GET.get('q')
    # if query:
    #     queue_list = Pages.objects \
    #         .filter(user=request.user) \
    #         .filter(page_name__contains=query) \
    #         .order_by('-id')
    #
    # paginator = Paginator(queue_list, 15)
    # page = request.GET.get('page')
    #
    # try:
    #     posts = paginator.page(page)
    # except PageNotAnInteger:
    #     posts = paginator.page(1)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    #
    # context = {
    #     'posts': posts,
    # }
    return render(request, 'pages/editor-list.html', {})


# ===================================== Get Page List ajax ================================================
@login_required(login_url='/signin')
def getpagelist(request):
    queue_list = Pages.objects.filter(user=request.user).order_by('order').values('id', 'parent_id', 'level', 'page_name')
    page_list = []
    for page in queue_list:
        page_list.append({
            'id': page['id'],
            'parent_id': page['parent_id'],
            'level': page['level'],
            'title': page['page_name'],
        })
    return JsonResponse({'page_list': page_list}, status=200)


@login_required(login_url='/signin')
def updatepath(request):
    dataLeft = request.POST.get('dataLeft')
    pages = json.loads(dataLeft)
    i = 0
    for page in pages:
        Pages.objects.filter(id=page['id']).update(parent_id=page['parent_id'], level=page['level'], order=i)
        i = i + 1

    return JsonResponse({}, status=200)


@login_required(login_url='/signin')
def remove_page(request):
    page_id = request.POST.get('page_id')
    submission = Submission.objects.filter(page_id=page_id).first()
    file_path = settings.STATIC_DIR + submission.draft_file_endpoint
    if os.path.isfile(file_path):
        os.remove(file_path)
        submission.delete()

    Pages.objects.filter(Q(id=page_id) | Q(parent_id=page_id)).delete()
    return JsonResponse({}, status=200)


def build_tree(data, parent_id):
    tree = []
    for item in data:
        if item['parent_id'] == parent_id:
            children = build_tree(data, item['id'])
            if children:
                item['children'] = children
            tree.append(item)
    return tree


@login_required(login_url='/signin')
def temppage(request):
    queue_list = Pages.objects.filter(user=request.user).order_by('order').values('id', 'parent_id', 'level',
                                                                                  'page_name')
    page_list = []
    for page in queue_list:
        page_list.append({
            'id': page['id'],
            'parent_id': page['parent_id'],
            'level': page['level'],
            'title': page['page_name'],
        })
    context = {
        "page_list": build_tree(page_list, 0)
    }
    return render(request, 'pages/temppage.html', context)


# ===================================== Create a PAGE ================================================
@login_required(login_url='/signin')
def create_page(request):
    if request.method == "POST":
        page_name = request.POST.get('page_name')
        user = request.user
        cnt_page = Pages.objects.count()
        Pages.objects.create(user=user, page_name=page_name, order=cnt_page)
        messages.add_message(request, messages.SUCCESS, 'Created successfully')
        return HttpResponseRedirect('/editor-list')


# ===================================== Editor PAGE ================================================
@login_required(login_url='/signin')
def editor(request, slug=None):
    page = Pages.objects.filter(id=slug).first()
    context = {
        "page": page,
        "submission_cnt": page.submissions.count()
    }
    return render(request, 'pages/editor.html', context)


# ===================================== Builder PAGE ================================================
@login_required(login_url='/signin')
def builder(request, page_id):
    context = {
        "page_id": page_id
    }
    return render(request, 'pages/builder.html', context)


@login_required(login_url='/signin')
def page(request, slug):
    submission = Submission.objects.filter(page_id=slug).first()

    queue_list = Pages.objects.filter(user=request.user).order_by('order').values('id', 'parent_id', 'level',
                                                                                  'page_name')
    page_list = []
    for page in queue_list:
        page_list.append({
            'id': page['id'],
            'parent_id': page['parent_id'],
            'level': page['level'],
            'title': page['page_name'],
        })

    context = {
        'submission': submission,
        "page_list": build_tree(page_list, 0)
    }

    return render(request, 'pages/temppage.html', context)


@login_required(login_url='/signin')
def vvvebjs(request, page_id):
    html_files = glob.glob(
        os.path.join(settings.STATIC_DIR, 'saved-pages/' + str(request.user.id) + '/*.html')) + glob.glob(
        os.path.join(settings.STATIC_DIR, 'demo/*.html')) + glob.glob(
        os.path.join(settings.STATIC_DIR, 'demo/*/*.html'))
    pages = []
    for path in html_files:
        if os.path.basename(path) in ['new-page-blank-template.html', 'editor.html']:
            continue
        filename, ext = os.path.splitext(os.path.basename(path))
        splited_path = os.path.dirname(path).split('\\')
        folder = splited_path[-2]
        subfolder = splited_path[-1]
        if filename == 'index' and subfolder:
            filename = subfolder
        url = os.path.join(settings.STATIC_URL, os.path.relpath(path, settings.STATIC_DIR)).replace('\\', '/')
        if os.path.dirname(os.path.dirname(path)) == settings.MEDIA_ROOT:
            url = os.path.join(settings.MEDIA_URL, os.path.relpath(path, settings.MEDIA_ROOT)).replace('\\', '/')
        name = filename.capitalize()

        pages.append({
            'name': name,
            'file': filename,
            'title': name,
            'url': url,
            'folder': folder,
        })
    page = Pages.objects.filter(id=page_id).first()
    context = {
        'pages': pages,
        'page_id': page_id,
        'page': page
    }
    return render(request, 'page-builder.html', context)


@csrf_exempt
@login_required(login_url='/signin')
def save_vvveb_page(request, page_id):
    MAX_FILE_LIMIT = 1024 * 1024 * 2  # 2 Megabytes max html file size

    def draft_file_endpoint(file_name):
        file_name = '/saved-pages/' + str(request.user.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name))) + ".html"
        file_name = file_name.replace('\\', '/')
        return file_name

    def sanitize_file_name(file_name):
        file_name = re.sub(r'^/static/', '/', file_name)
        # file_name = settings.MEDIA_ROOT + '/saved-pages/' + str(request.user.id) + '/' + re.sub(r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)) + '_' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = settings.STATIC_DIR + '/saved-pages/' + str(request.user.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)))
        file_name = file_name.replace('\\', '/')
        return file_name


    def transform_html(html: str) -> str:
        return html.replace('../../', '/static/')

    if request.method == 'POST':
        html = ''
        if 'startTemplateUrl' in request.POST and request.POST['startTemplateUrl']:
            start_template_url = sanitize_file_name(request.POST.get('startTemplateUrl'))
            with open(start_template_url, 'r') as f:
                html = f.read()
        elif 'html' in request.POST:
            html = request.POST.get('html')[:MAX_FILE_LIMIT]

        html = transform_html(html)

        file_name = sanitize_file_name(request.POST.get('file', ''))

        try:
            root_directory = settings.STATIC_DIR + '/saved-pages/'
            subprocess.run(["icacls", root_directory, "/reset", "/t"], check=True)
            for dirpath, dirnames, filenames in os.walk(root_directory):
                # Modify the permissions of the current directory (parent)
                os.chmod(dirpath, 0o777)
                # Modify the permissions of all child directories
                for dirname in dirnames:
                    dir_path = os.path.join(dirpath, dirname)
                    os.chmod(dir_path, 0o777)

            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name + '.html', 'w', encoding='utf-8') as f:
                f.write(html)

            old_html = ''
            if 'old_html' in request.POST and request.POST['old_html']:
                old_html = transform_html(request.POST.get('old_html')[:MAX_FILE_LIMIT])
                with open(file_name + '_old.html', 'w', encoding='utf-8') as f:
                    f.write(old_html)

            filename, ext = os.path.splitext(os.path.basename(file_name + '.html'))
            slug = Slug.objects.create(filename=filename, author=request.user)

            # Create new unapproved submission entry
            new_submission = Submission()
            new_submission.slug = filename  # <-- TODO We should have a better slug later
            new_submission.old_version = old_html
            new_submission.new_version = html
            new_submission.submitter_id = request.user.id
            new_submission.draft_file_endpoint = draft_file_endpoint(request.POST.get('file', ''))
            new_submission.page_id = page_id
            new_submission.save()

            sub_view_old_url = new_submission.get_view_url(True, request)
            sub_view_new_url = new_submission.get_view_url(False, request)
            # sub_screenshot_old_url = new_submission.get_screenshot_url(True, request)
            # sub_screenshot_new_url = new_submission.get_screenshot_url(False, request)
            sub_screenshot_old_url = "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=500&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4MTg1MDM0NA&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=500"
            sub_screenshot_new_url = "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=500&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4MTg1MDM0NA&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=500"
            Submission.objects.filter(id=new_submission.id).update(sub_view_new_url=sub_view_new_url,
                                                                   sub_view_old_url=sub_view_old_url,
                                                                   sub_screenshot_new_url=sub_screenshot_new_url,
                                                                   sub_screenshot_old_url=sub_screenshot_old_url)
            try:
                # Screenshot submission (old and new versions)
                sub_id_str = str(new_submission.id)
                sub_old_url = request.build_absolute_uri('/submission/view?id=' + sub_id_str + '&old=1')
                sub_new_url = request.build_absolute_uri('/submission/view?id=' + sub_id_str + '&old=0')
                screenshot_dir = os.path.join(settings.MEDIA_ROOT, 'submission-screenshots')
                take_page_screenshot(sub_old_url, os.path.join(screenshot_dir, sub_id_str + '.old.png'))
                take_page_screenshot(sub_new_url, os.path.join(screenshot_dir, sub_id_str + '.new.png'))

            except Exception as e:
                print(e)
                # return HttpResponseServerError(
                # For site administrator: Failed to screenshot page. Check logs and ensure that you have Chrome/Chromium installed')

            messages.success(request, f'Saved {filename} Page Successfully.')
            response = {
                "flag": "save",
                "data": f'File saved: {file_name}'
            }
            return HttpResponse(
                json.dumps(response),
                status=200
            )
        except Exception as e:
            print(e)
            return HttpResponseServerError(
                f'Error saving file {file_name}\n Possible causes are missing write permission or incorrect file path!')
    return HttpResponseServerError('Invalid request method')


@login_required(login_url='/signin')
def vvvebjs_edit(request, page_id):
    html_files = glob.glob(
        os.path.join(settings.STATIC_DIR, 'saved-pages/' + str(request.user.id) + '/*.html')) + glob.glob(
        os.path.join(settings.STATIC_DIR, 'demo/*.html')) + glob.glob(
        os.path.join(settings.STATIC_DIR, 'demo/*/*.html'))
    pages = []
    for path in html_files:
        if os.path.basename(path) in ['new-page-blank-template.html', 'editor.html']:
            continue
        filename, ext = os.path.splitext(os.path.basename(path))
        splited_path = os.path.dirname(path).split('\\')
        folder = splited_path[-2]
        subfolder = splited_path[-1]
        if filename == 'index' and subfolder:
            filename = subfolder
        url = os.path.join(settings.STATIC_URL, os.path.relpath(path, settings.STATIC_DIR)).replace('\\', '/')
        if os.path.dirname(os.path.dirname(path)) == settings.MEDIA_ROOT:
            url = os.path.join(settings.MEDIA_URL, os.path.relpath(path, settings.MEDIA_ROOT)).replace('\\', '/')
        name = filename.capitalize()

        pages.append({
            'name': name,
            'file': filename,
            'title': name,
            'url': url,
            'folder': folder,
        })
    submission = Submission.objects.filter(submitter_id=request.user.id).filter(page_id=page_id).order_by('-id').first()
    context = {
        'pages': pages,
        'submission': submission
    }
    return render(request, 'page-builder-edit.html', context)


@csrf_exempt
@login_required(login_url='/signin')
def update_save_vvveb_page(request, page_id):
    MAX_FILE_LIMIT = 1024 * 1024 * 2  # 2 Megabytes max html file size

    def draft_file_endpoint(file_name):
        file_name = '/saved-pages/' + str(request.user.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name))) + ".html"
        file_name = file_name.replace('\\', '/')
        return file_name

    def sanitize_file_name(file_name):
        file_name = re.sub(r'^/static/', '/', file_name)
        # file_name = settings.MEDIA_ROOT + '/saved-pages/' + str(request.user.id) + '/' + re.sub(r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)) + '_' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = settings.STATIC_DIR + '/saved-pages/' + str(request.user.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)))
        file_name = file_name.replace('\\', '/')
        print(file_name)
        return file_name

    def transform_html(html: str) -> str:
        return html.replace('../../', '/static/')

    if request.method == 'POST':
        html = ''
        if 'startTemplateUrl' in request.POST and request.POST['startTemplateUrl']:
            start_template_url = sanitize_file_name(request.POST.get('startTemplateUrl'))
            with open(start_template_url, 'r') as f:
                html = f.read()
        elif 'html' in request.POST:
            html = request.POST.get('html')[:MAX_FILE_LIMIT]

        html = transform_html(html)

        file_name = sanitize_file_name(request.POST.get('file', ''))

        try:
            root_directory = settings.STATIC_DIR + '/saved-pages/'
            subprocess.run(["icacls", root_directory, "/reset", "/t"], check=True)
            for dirpath, dirnames, filenames in os.walk(root_directory):
                # Modify the permissions of the current directory (parent)
                os.chmod(dirpath, 0o777)
                # Modify the permissions of all child directories
                for dirname in dirnames:
                    dir_path = os.path.join(dirpath, dirname)
                    os.chmod(dir_path, 0o777)

            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name + '.html', 'w', encoding='utf-8') as f:
                f.write(html)

            old_html = ''
            if 'old_html' in request.POST and request.POST['old_html']:
                old_html = transform_html(request.POST.get('old_html')[:MAX_FILE_LIMIT])
                with open(file_name + '_old.html', 'w', encoding='utf-8') as f:
                    f.write(old_html)

            filename, ext = os.path.splitext(os.path.basename(file_name + '.html'))
            slug = Slug.objects.create(filename=filename, author=request.user)

            submission = Submission.objects.filter(submitter_id=request.user.id) \
                .filter(page_id=page_id)

            if submission.exists():
                submission.update(slug=filename, old_version=old_html, new_version=html,
                                  draft_file_endpoint=draft_file_endpoint(request.POST.get('file', '')))
            else:
                # Create new unapproved submission entry
                new_submission = Submission()
                new_submission.slug = filename  # <-- TODO We should have a better slug later
                new_submission.old_version = old_html
                new_submission.new_version = html
                new_submission.submitter_id = request.user.id
                new_submission.draft_file_endpoint = draft_file_endpoint(request.POST.get('file', ''))
                new_submission.page_id = page_id
                new_submission.save()

                sub_view_old_url = new_submission.get_view_url(True, request)
                sub_view_new_url = new_submission.get_view_url(False, request)
                # sub_screenshot_old_url = new_submission.get_screenshot_url(True, request)
                # sub_screenshot_new_url = new_submission.get_screenshot_url(False, request)
                sub_screenshot_old_url = "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=500&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4MTg1MDM0NA&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=500"
                sub_screenshot_new_url = "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?crop=entropy&cs=tinysrgb&fit=crop&fm=jpg&h=500&ixid=MnwxfDB8MXxyYW5kb218MHx8fHx8fHx8MTY4MTg1MDM0NA&ixlib=rb-4.0.3&q=80&utm_campaign=api-credit&utm_medium=referral&utm_source=unsplash_source&w=500"
                Submission.objects.filter(id=new_submission.id).update(sub_view_new_url=sub_view_new_url,
                                                                       sub_view_old_url=sub_view_old_url,
                                                                       sub_screenshot_new_url=sub_screenshot_new_url,
                                                                       sub_screenshot_old_url=sub_screenshot_old_url)

            try:
                # Screenshot submission (old and new versions)
                sub_id_str = str(new_submission.id)
                sub_old_url = request.build_absolute_uri('/submission/view?id=' + sub_id_str + '&old=1')
                sub_new_url = request.build_absolute_uri('/submission/view?id=' + sub_id_str + '&old=0')
                screenshot_dir = os.path.join(settings.MEDIA_ROOT, 'submission-screenshots')
                take_page_screenshot(sub_old_url, os.path.join(screenshot_dir, sub_id_str + '.old.png'))
                take_page_screenshot(sub_new_url, os.path.join(screenshot_dir, sub_id_str + '.new.png'))

            except Exception as e:
                print(e)
                # return HttpResponseServerError(
                #     'For site administrator: Failed to screenshot page. Check logs and ensure that you have Chrome/Chromium installed')

            response = {
                "flag": "update",
                "data": f'File saved: {file_name}'
            }
            return HttpResponse(
                json.dumps(response),
                status=200
            )
        except Exception as e:
            print(e)
            return HttpResponseServerError(
                f'Error saving file {file_name}\n Possible causes are missing write permission or incorrect file path!')
    return HttpResponseServerError('Invalid request method')


@login_required(login_url='/signin')
def subitForReview(request, page_id):  # Publish
    user = request.user
    username = f"{user.first_name} {user.last_name}"
    submission = Submission.objects.filter(submitter_id=request.user.id).filter(page_id=page_id)
    submission.update(status=COMPLIANCE_STATUS["pending"])
    submission = submission.first()

    email_subject = f'{user.email} has made changes to page ({submission.slug})'
    message = render_to_string('email/publish.html', {
        'name': username,
        'domain': f'home.{APP_DOMAIN}',
        'slug': submission.slug,
        'link': submission.sub_view_new_url
    })

    try:
        send_email(
            user.email,
            email_subject,
            message,
            is_html=True,
        )
        messages.success(request, 'Sent to compliance, please check the compliance tab.')
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        messages.success(request, str(e))
        return redirect(request.META.get('HTTP_REFERER'))


def submission_version_officer_viewer(request: WSGIRequest, id, old) -> HttpResponse:
    sub_id = str(id)
    is_old_param = str(old)
    if is_old_param is None:
        is_old_param = '0'
    is_old = is_old_param == '1' or is_old_param.lower() == 'true'

    sub = Submission.objects.filter(id=sub_id).first()

    if sub is None:
        return HttpResponseBadRequest('Invalid submission ID provided')

    if is_old:
        return HttpResponse(sub.old_version)
    else:
        return HttpResponse(sub.new_version)


def submission_version_viewer(request):
    # TODO DON'T USE SEQUENTIAL IDS, USE SOMETHING RANDOMLY GENERATED
    # We're only doing this right now to save time.
    # It's a security vulnerability otherwise!

    sub_id = int(request.GET.get('id'))
    is_old_param = request.GET.get('old')
    submission = Submission.objects.filter(id=sub_id).first()
    context = {
        "old_path": "submission/officer/view/{0}/{1}".format(sub_id, 1),
        "new_path": "submission/officer/view/{0}/{1}".format(sub_id, 0),
        "submission": submission
    }
    # submission_version_officer_viewer
    return render(request, "pages/viewer.html", context)


def statusChange(request):
    status = request.POST.get('status')
    sub_id = request.POST.get('id')

    comment = request.POST.get('comment')
    if comment is None:
        comment = ""

    if status == COMPLIANCE_STATUS['approved']:
        Submission.objects.filter(id=sub_id).update(status=status, approved_ts=datetime.now(),
                                                    approval_officer_note=comment, checked=0)
    else:
        Submission.objects.filter(id=sub_id).update(status=status, denied_ts=datetime.now(),
                                                    approval_officer_note=comment, checked=0)

    if status == COMPLIANCE_STATUS['approved']:
        messages.success(request, 'Thank you! The page will be live shortly.')
    else:
        messages.success(request, 'Changed Status Successfully.')

    referer_url = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer_url)


@login_required(login_url='/signin')
def view_reason(request, submission_id):
    submission = Submission.objects.filter(id=submission_id).first()
    page = Pages.objects.filter(id=submission.page_id).first()
    context = {
        "submission": submission,
        "page_name": page.page_name
    }
    return render(request, "pages/reason_viewer.html", context)


@login_required(login_url='/signin')
def success(request):
    user = request.user

    # meeting = ScheduleMeeting.objects.filter(creator=user)
    # if meeting.exists():
    #     return redirect('/')

    cnt_admin = CustomUser.objects.filter(Q(role=1) | Q(role=2)).count()
    rest = user.id % cnt_admin
    group = rest + 1
    ScheduleMeeting.objects.update_or_create(
        creator_id=user.id,
        defaults={
            "group": group,
        })
    return render(request, "auth/success.html")


@login_required(login_url='/signin')
def nylas_auth(request):
    user = request.user
    redirect_url = os.getenv('APP_NYLAS_REDIRECT_URL')
    client = APIClient(NYLAS_CLIENT_ID, NYLAS_CLIENT_SECRET)
    return redirect(client.authentication_url(redirect_url, user.email, scopes=["calendar"], state=None))


@login_required(login_url='/signin')
def login_callback(request):
    user = request.user
    client = APIClient(NYLAS_CLIENT_ID, NYLAS_CLIENT_SECRET, None, "https://api.nylas.com")
    code = request.GET.get('code')
    user.nylas_access_token = client.token_for_code(code)

    client.access_token = user.nylas_access_token
    calendars = list(filter(lambda x: not x.read_only, client.calendars.all()))
    real_calendar = None
    for calendar in calendars:
        if calendar.is_primary:
            real_calendar = calendar
    if real_calendar is None:
        real_calendar = calendars[0]

    user.calendar_id = real_calendar.id
    user.save()
    return redirect('/schedulecall')


@login_required(login_url='/signin')
def schedulecall(request):
    user: CustomUser = request.user
    meeting = ScheduleMeeting.objects.filter(creator=user).first()
    partner = CustomUser.objects.filter(group=meeting.group).first()
    nylas = create_nylas_client_for_user(user)
    event = nylas.events.create()
    event.title = "System Design testing"
    event.description = "Welcome to the event"
    # Get today’s date
    today = date.today()
    # Today’s date at 12:00:00 am
    START_TIME = int(datetime(today.year, today.month, today.day, 23, 20, 0).timestamp())
    # Today’s date at 11:59:59 pm
    END_TIME = int(datetime(today.year, today.month, today.day, 23, 30, 0).timestamp())
    event.when = {
        'start_time': START_TIME,
        'end_time': END_TIME,
    }
    event.calendar_id = user.calendar_id
    event.participants = [{"email": email} for email in f"{partner.email}, {request.user.email}".split(", ")]
    event.save(notify_participants=True)
    return render(request, "auth/schedulecall.html")


@login_required(login_url='/signin')
def chooseschedule(request):
    user = request.user

    meeting = ScheduleMeeting.objects.get(creator=user)
    if meeting.status != "":
        return redirect('/')
    dates = ScheduleMeeting.objects.filter(group=meeting.group).values_list('date', flat=True)
    y_m_d_list = []
    date_list = list(dates)
    for item in date_list:
        if item is not None:
            year = item.year
            month = item.month
            date = item.day
            y_m_d_list.append({
                "year": year,
                "month": month,
                "date": date
            })

    form = DateTimeForm()
    context = {
        "form": form,
        "dates": json.dumps(y_m_d_list),
        "scheduled_date": meeting.date
    }
    return render(request, 'auth/chooseschedule.html', context)


@login_required(login_url='/signin')
def meetingwait(request):
    meeting = ScheduleMeeting.objects.filter(creator_id=request.user.id)

    if not meeting.exists():
        print('found you s')
        return redirect('/success')

    meeting = meeting.first()
    if meeting.status != 'SCHEDULED' and meeting.status != 'MEETING NOW':
        return redirect('/')
    context = {
        "schedule": meeting,
        'meeting_link': meeting.meeting_link
    }
    return render(request, 'auth/meetingwait.html', context)


@login_required(login_url='/signin')
def meeting(request, meeting_link):
    meeting = ScheduleMeeting.objects.get(meeting_link=meeting_link)

    if meeting.lock_meeting != "Debug":
        meeting_start_time = datetime.combine(meeting.date, meeting.time)
        current_time = datetime.now()
        if current_time < meeting_start_time:
            time_difference = meeting_start_time - current_time
            days = time_difference.days
            seconds = time_difference.seconds
            hours = seconds // 3600
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60

            print("Remaining time: {} hours, {} minutes, {} seconds".format(hours, minutes, seconds))

            messages.error(request, "Remaining time: {} days {} hours, {} minutes, {} seconds.\
                                   \n Please wait until the meeting is ready"
                           .format(days, hours, minutes, seconds))
            return redirect('/meetingwait')

    meeting.status = "MEETING NOW"
    meeting.save()
    context = {
        "meeting_link": meeting_link,
    }
    return render(request, 'pages/meeting.html', context)


@login_required(login_url='/signin')
def enterdetail(request):
    global meeting
    if request.method == 'GET':
        user = request.user
        meeting = ScheduleMeeting.objects.filter(creator=user).first()
        context = {
            "user": user,
            "schedule": meeting
        }
        return render(request, 'auth/enterdetail.html', context)
    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        if form.is_valid():
            # Process the form data
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            local_timezone = form.cleaned_data['timezone']
            timezone_str = "EST"
            available_times = form.cleaned_data['available_times']
            tz = timezone(timezone_str)
            aware_datetime = tz.localize(datetime.combine(date, time))
            meeting_start_datetime = datetime.combine(date, time)
            meeting_end_datetime = meeting_start_datetime + timedelta(minutes=60)
            current_time = datetime.now()
            if current_time >= meeting_start_datetime:
                messages.error(request, "The meeting time needs to be scheduled for a time that is later \
                                        than the current time")
                return redirect(request.META.get('HTTP_REFERER'))
            # Perform additional actions with the data

            converted_start_time = tz.localize(meeting_start_datetime).astimezone(timezone(local_timezone))
            converted_end_time = tz.localize(meeting_end_datetime).astimezone(timezone(local_timezone))
            meeting, created = ScheduleMeeting.objects.update_or_create(
                creator_id=request.user.id,
                defaults={
                    "date": date,
                    "time": converted_start_time.time(),
                    "timezone": local_timezone,
                    "aware_datetime": aware_datetime,
                    "end_time": converted_end_time.time()
                }
            )

            AvailableTime.objects.filter(Q(group=meeting.group) & Q(date=meeting.date)).update(times=available_times)

            return redirect('/enterdetail')
        else:
            messages.error(request, "You have to choose the scheduled datetime.")
            return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/signin')
def confirmed(request):
    if request.method == "GET":
        user = request.user
        meeting = ScheduleMeeting.objects.filter(creator=user).first()
        context = {
            "meeting": meeting,
        }
        return render(request, "auth/confirmed.html", context)
    if request.method == "POST":
        user = request.user
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        meeting_link = generate_random_string(20)
        meeting, created = ScheduleMeeting.objects.update_or_create(
            creator=user,
            defaults={
                "name": name,
                "email": email,
                "content": description,
                "meeting_link": meeting_link,
            }
        )

        user = request.user
        nylas = APIClient(
            os.environ.get("NYLAS_CLIENT_ID"),
            os.environ.get("NYLAS_CLIENT_SECRET"),
            api_server=os.environ.get("NYLAS_API_SERVER") or "https://api.nylas.com"
        )
        nylas.access_token = user.nylas_access_token
        calendars = list(filter(lambda x: not x.read_only, nylas.calendars.all()))
        real_calendar = None
        for calendar in calendars:
            if calendar.is_primary:
                real_calendar = calendar
        if real_calendar is None:
            real_calendar = calendars[0]

        event = nylas.events.create()

        event.title = name
        event.description = description
        # Get today’s date
        today = date.today()
        # Today’s date at 12:00:00 am
        START_TIME = int(datetime(today.year, today.month, today.day, 23, 20, 0).timestamp())
        # Today’s date at 11:59:59 pm
        END_TIME = int(datetime(today.year, today.month, today.day, 23, 30, 0).timestamp())
        event.when = {
            'start_time': START_TIME,
            'end_time': END_TIME,
        }
        event.calendar_id = real_calendar.id
        print(real_calendar.id)
        event.participants = [{"email": email} for email in "testemail@gmail.com".split(", ")]
        event.save(notify_participants=True)
        return redirect('/confirmed')


@login_required(login_url='/signin')
def schedulemeeting(request):
    if request.method == "POST":
        meeting_id = request.POST.get('meeting_id')
        meeting = ScheduleMeeting.objects.get(id=meeting_id)
        meeting.status = 'SCHEDULED'
        meeting.save()
        email_subject = "Your WebSystem Live Onboarding"
        message = render_to_string('email/schedule_meeting.html', {
            'meeting': meeting,
            'domain': f'home.{APP_DOMAIN}',
            'schema': request.scheme
        })
        # Add the sending email code here
        try:
            send_email(
                request.user.email,
                email_subject,
                message,
                is_html=True,
            )
            messages.success(request, 'Please check your email for meeting time.')
        except Exception as e:
            print(e)
            messages.success(request, str(e))
            return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/')


@login_required(login_url='/signin')
def getavailabletime(request):
    if request.method == 'POST':
        user = request.user
        date = request.POST.get('date')
        time = AvailableTime.objects.filter(Q(date=date) & Q(group=user.meeting.group))
        if time.exists():
            time = time.values()[0]
        else:
            time = None

        response = {
            "message": "",
            "status": "success",
            "data": time
        }
        return JsonResponse(response, status=200)


@login_required(login_url='/signin')
def settingsgear(request):
    user = request.user
    customer = CustomUser.objects.filter(email=user.email).first()
    website_settings = WebsiteSettings.load(request_or_site=request)
    company = Company.objects.filter(pk=customer.company.pk).first()

    if request.method == "POST":
        user_form = CustomUserForm(request.POST, instance=customer)
        settings_form = WebsiteSettingsForm(request.POST, instance=website_settings)
        company_form = CompanyForm(request.POST, instance=company)

        if user_form.is_valid():
            user_form.save()
            print("User form should be saved")
        else:
            print("The user Form:", user_form.errors)

        if settings_form.is_valid():
            settings_form.save()
        else:
            print("The settings Form:", settings_form.errors)

        if company_form.is_valid():
            company_form.save()

        return redirect(reverse("settingsgear"))

    else:
        user_form = CustomUserForm(instance=customer)
        settings_form = WebsiteSettingsForm(instance=website_settings)
        company_form = CompanyForm(instance=company)

    context = {
        "user": customer,
        "user_form": user_form,
        'settings_form': settings_form,
        'company_form': company_form
    }

    return render(request, "pages/settingsgear.html", context)

    #return HttpResponseRedirect(f"{request.scheme}://{user.domain_url}/settingsgear")


@login_required(login_url='/signin')
def socialsystem(request):
    if not 'access_token' in request.session:

        queue_list = Article.objects.order_by('-id')
        query = request.GET.get('q')
        if query:
            queue_list = Article.objects \
                .filter(title__contains=query) \
                .order_by('-id')

        paginator = Paginator(queue_list, 10)
        page = request.GET.get('page')

        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context = {
            "articles": articles,
            'title': 'Social Management'
        }
        return render(request, "pages/articles.html", context)
    else:
        return redirect("/obtain_access_token")


# ================================CMS==================================
@login_required(login_url='/signin')
def cms(request):
    return render(request, 'pages/cms.html')


# =========================Create a view for obtaining the Access Token======================
@login_required(login_url='/signin')
def obtain_access_token(request):
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    oauth_args = {
        'client_id': FACEBOOK_APP_ID,
        'redirect_uri': redirect_uri,
    }
    login_url = facebook.GraphAPI().get_auth_url(FACEBOOK_APP_ID, redirect_uri)
    return redirect(login_url)


# ===================Create a callback view to handle the authorization code==================
@login_required(login_url='/signin')
def callback(request):
    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    print("-----------------------------")
    print(redirect_uri)
    print("-----------------------")
    print(code)
    print("-----------------------")
    if code:
        graph = facebook.GraphAPI()
        access_token = graph.get_access_token_from_code(code, redirect_uri, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET)
        # Store the access token in session or database
        request.session['access_token'] = access_token["access_token"]

    return redirect('/socialsystem')


# ===================Post an article using the Access Token==================
@login_required(login_url='/signin')
def post_article(request):
    if request.method == 'POST':
        try:
            """
            article_title = request.POST.get("title")
            article_link = request.POST.get("link")
            article_link = "https://example.com"
            access_token = request.session['access_token']
            print("=============access token=====================")
            print(access_token)
            print("=======================")
            graph = facebook.GraphAPI(access_token)
            graph.put_object("me", "feed", message=article_title)
    
            # page_info = graph.get_object(id=102150979641902, fields="access_token")
            # page_token = page_info['access_token']
            print("=============page token=====================")
            # print(page_token)
            print("=======================")
            """
            title = request.POST.get('title')
            content = request.POST.get('content')
            file = ''
            if request.FILES.get("file"):
                file = request.FILES.get("file")
                fs = FileSystemStorage()
                time = datetime.now().strftime('%Y%m%d%H%M%S')
                filename1 = time + file.name
                filename_url = fs.save('img/article/' + filename1, file)
                uploaded_file_url = fs.url(filename_url)
                file = filename1

            article = Article.objects.create(
                user=request.user,
                title=title,
                content=content,
                file=file
            )
            messages.success(request, "Posted Successfully.")
            return redirect(request.META.get('HTTP_REFERER'))
        except Exception as e:
            messages.error(request, "Failed {}".format(str(e)))
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'pages/socialsystem.html')


# ===================View an article==================
@login_required(login_url='/signin')
def article(request, id):
    art = Article.objects.filter(id=id).first()
    context = {
        "article": art
    }
    return render(request, 'pages/article.html', context)


@login_required(login_url='/signin')
def pending(request):
    meeting = ScheduleMeeting.objects.get(creator=request.user)
    if meeting.status != 'END':
        return redirect('/')
    return render(request, 'auth/pending.html')


def calendar_view(request):
    # Create a new calendar
    cal = Calendar()

    # Set some properties for the calendar
    cal.add('prodid', '-//Your Organization//Example//EN')
    cal.add('version', '2.0')

    # Create an event and add it to the calendar
    event = Event()
    event.add('summary', 'Event Summary')
    event.add('dtstart', datetime.now())
    event.add('dtend', datetime.now() + timedelta(minutes=60))
    cal.add_component(event)

    # Generate the iCalendar data
    cal_data = cal.to_ical()

    # Create the HTTP response
    response = HttpResponse(content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="calendar.ics"'
    response.write(cal_data)

    return response


@login_required(login_url='/signin')
def tv(request):
    context = {}
    return render(request, 'pages/tv.html', context)


@csrf_exempt
def nylas_webhook(request):
    query_params = request.GET
    challenge = False
    for key, value in query_params.items():
        if key == "challenge":
            challenge = True
    if request.method == "GET" and challenge:
        return request.GET.get('challenge')

    print(request.GET.get('challenge'))
    is_genuine = verify_signature(
        message=request.GET.get('challenge'),
        key=NYLAS_CLIENT_SECRET.encode("utf8"),
        signature=request.headers.get("X-Nylas-Signature"),
    )
    if not is_genuine:
        return "Signature verification failed!", 401

    # Alright, we have a genuine webhook notification from Nylas!
    # Let's find out what it says...
    data = request.body
    print(data)
    for delta in data["deltas"]:
        # Processing the data might take awhile, or it might fail.
        # As a result, instead of processing it right now, we'll push a task
        # onto the Celery task queue, to handle it later. That way,
        # we've got the data saved, and we can return a response to the
        # Nylas webhook notification right now.
        process_delta.delay(delta)

    # Now that all the `process_delta` tasks have been queued, we can
    # return an HTTP response to Nylas, to let them know that we processed
    # the webhook notification successfully.
    return "Deltas have been queued", 200


def verify_signature(message, key, signature):
    """
    This function will verify the authenticity of a digital signature.
    For security purposes, Nylas includes a digital signature in the headers
    of every webhook notification, so that clients can verify that the
    webhook request came from Nylas and no one else. The signing key
    is your OAuth client secret, which only you and Nylas know.
    """
    digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def process_delta(delta):
    """
    This is the part of the code where you would process the information
    from the webhook notification. Each delta is one change that happened,
    and might require fetching message IDs, updating your database,
    and so on.

    However, because this is just an example project, we'll just print
    out information about the notification, so you can see what
    information is being sent.
    """
    kwargs = {
        "type": delta["type"],
        "date": datetime.utcfromtimestamp(delta["date"]),
        "object_id": delta["object_data"]["id"],
    }
    print(" * {type} at {date} with ID {object_id}".format(**kwargs))


@login_required(login_url='/signin')
def cms_auth(request):
    user = request.user
    token = create_login_token(user.email)
    return HttpResponseRedirect(f"{request.scheme}://{user.domain_url}/docmslogin?token={token}")


@login_required(login_url='/signin')
def a(request):
    return redirect('/')


# -------------------------------------  Green View ---------------------------------------------------------

# ===================================== AI TOOL PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def ai_tool(request):
    return render(request, 'pages-green/ai-tool.html', {'title': 'AI Tool'})


# ===================================== AUTOMATIONS PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def automations(request):
    return render(request, 'pages-green/automations.html', {'title': 'Automations'})


# ===================================== MEETINGS PAGE ================================================
meeting_types = ['Personal Meetings', 'Consultations', 'Instant Meetings', 'Schedular']


def get_base_meetings_context(request: WSGIRequest) -> dict:
    user: CustomUser = request.user

    calendar_profile: CalendarProfile = CalendarProfile.objects.filter(user=user).first()

    # Create a profile if none exists
    if calendar_profile is None:
        calendar_profile = CalendarProfile.objects.create(
            user=user,
            title=user.display_name,
        )

    link_root = user.domain_url + '/' + calendar_profile.url

    return {
        'profile': calendar_profile,
        'link_root': link_root,
    }


# @approved_required
@login_required(login_url='/signin')
def meetings(request):
    user: CustomUser = request.user

    event_types = EventType.objects.filter(user=user)

    context = get_base_meetings_context(request)

    context['event_types'] = event_types
    context['LOCATION_CHOICES'] = EventType.LOCATION_CHOICES

    return render(request, 'pages/meetings.html', context)


class CreateEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64, allow_blank=False)
    slug = serializers.CharField(max_length=64, allow_blank=False)
    location = serializers.ChoiceField(choices=EventType.LOCATION_CHOICES)
    description = serializers.CharField(max_length=2048, allow_blank=True)
    duration = serializers.IntegerField(min_value=1)


def create_new_event_type(request: WSGIRequest) -> JsonResponse:
    """
    API endpoint to manage event types
    """

    print("Trying to create a new event type")

    if request.method == 'POST':
        print("The method is post")
        body_val = CreateEventSerializer(data=json.loads(request.body))

        if not body_val.is_valid():
            return JsonResponse({'message': ', '.join([f'{x}: {body_val.errors[x][0]}' for x in body_val.errors.keys()])}, status=400)

        body = body_val.validated_data

        slug = body['slug']

        # Verify that slug is in the correct format
        if re.search("^[a-zA-Z0-9-]+$", slug) is None:
            return JsonResponse({'message': 'Slug must only contain letters, numbers and dashes'}, status=400)

        if EventType.objects.filter(user=request.user, slug=slug).exists():
            return JsonResponse({'message': 'Event with this slug already exists. Try another.'}, status=409)

        # All is well, create event type
        EventType.objects.create(
            user=request.user,
            title=body['title'],
            slug=slug,
            description=body['description'],
            location=body['location'],
            duration_minutes=body['duration'],
        )

        print("The method should be close te the end")

        return JsonResponse({'slug': slug}, status=200)
    else:
        return JsonResponse({'message': 'Unsupported method'}, status=405)


def render_public_events_page(request: WSGIRequest, profile: CalendarProfile) -> HttpResponse:
    # Fetch event types for profile
    event_types = EventType.objects.filter(user_id=profile.user_id, is_hidden=False)

    return render(request, 'pages/calendar-public/events.html', context={
        'profile': profile,
        'event_types': event_types,
    })


class CreateBookingSerializer(serializers.Serializer):
    start_ts = serializers.DateTimeField()
    name = serializers.CharField(max_length=200, allow_blank=False)
    email = serializers.EmailField()



def generate_jaas_meeting_link(api_key, room_name, options={}):
    endpoint = "https://jaas.8x8.vc/api/meeting"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": room_name,
        "properties": options
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['roomUrl']
    else:
        print("Failed to generate JaaS meeting link:", response.text)
        return None

# # Example usage:
# api_key = os.environ.get('JITSI_APP_ID')
# room_name = generate_random_string()
# options = {
#     "startWithVideoMuted": True,
#     "startWithAudioMuted": True
# }
#
# meeting_link = generate_jaas_meeting_link(api_key, room_name, options)
# print("JaaS Custom Meeting Link:", meeting_link)


def render_public_events_event_type_page(request: WSGIRequest, profile: CalendarProfile, event_type: EventType) -> HttpResponse:
    if request.headers.get('Accept', '*/*') == 'application/json':
        # This is an API call

        action = request.GET.get('action')
        
        if request.method == 'POST' and action == 'book':
            body_val = CreateBookingSerializer(data=json.loads(request.body))

            if not body_val.is_valid():
                return JsonResponse(
                    {'message': ', '.join([f'{x}: {body_val.errors[x][0]}' for x in body_val.errors.keys()])},
                    status=400,
                )

            body = body_val.validated_data

            name = body['name']
            email = body['email']

            start_ts: datetime = body['start_ts']
            end_ts: datetime = body['start_ts'] + timedelta(minutes=event_type.duration_minutes)

            # TODO There will be different types later, but create an instant meeting ID for all of them right now
            instant_meeting_id = create_new_meeting()

            booking = EventBooking.objects.create(
                event_type=event_type,
                start_ts=start_ts,
                end_ts=end_ts,
                scheduler_name=name,
                scheduler_email=email,
                meeting_id=instant_meeting_id,
            )

            meeting_url = meeting_link_for_id(instant_meeting_id)

            email_template_html = render_to_string('email/meeting_booked.html', context={
                'meeting_url': meeting_url,
                'event_type': event_type,
                'name': name,
                'email': email,
                'start_ts': start_ts,
            })

            send_email(email, subject="Your Meeting is now Scheduled!", content=email_template_html, is_html=True)
            # Event Title, Time, To Who, THe Meeting URL
            # still working on dropdown btw
            # Create event on host's calendar with NylasTrue
            nylas = create_nylas_client_for_user(profile.user)
            event = nylas.events.create()
            event.title = f'{event_type.title} ({name})'
            event.description = meeting_url + '\n\n' + event_type.description
            event.participants = [{'name': name, 'email': email}]
            event.when = {'start_time': int(time.mktime(start_ts.timetuple())), 'end_time': int(time.mktime(end_ts.timetuple()))}
            event.calendar_id = profile.user.calendar_id
            event.save(notify_participants='true')

            return JsonResponse({})
        else:
            return JsonResponse({'message': f'Unknown action {request.method} "{action}"'}, status=400)
    else:
        return render(request, 'pages/calendar-public/event-booking.html', context={
            'profile': profile,
            'event_type': event_type,
        })


# on older system this is called def get_consultant_events_from_nylas(access_token):
def get_events_from_nylas(access_token):
    nylas = APIClient(
        os.environ.get("NYLAS_CLIENT_ID"),
        os.environ.get("NYLAS_CLIENT_SECRET"),
        access_token
    )

    current_timestamp = int(time.time())
    events = nylas.events.where(starts_after=current_timestamp,limit=20)

    for event in events:
        print("Title ->",event)

    return events


# on older system it is called get_consultant_meetings(schema_name)

def get_consultation_meetings(schema_name):
    consultations=[]

    with schema_context(schema_name):
        consultations = list(Meetings.objects.filter(meeting_type=2).values())
    return consultations

@login_required(login_url='/signin')
@approved_required
def meetings_create(request):
    selected_meeting_type = meeting_types[0]
    if request.method=='POST' and request.POST.get('meeting_type'):
        selected_meeting_type = request.POST.get('meeting_type')
    meeting_types_instance = meeting_types.copy()
    meeting_types_instance.remove(selected_meeting_type)
    meeting_types_instance.insert(0,selected_meeting_type)

    user = request.user
    schema_name = user.tenantuser.tenant.schema_name

    consultations = get_consultation_meetings(schema_name)
    print(consultations)

    context = {
        'meeting_types_instance':meeting_types_instance,
        'meeting_types':meeting_types,
        'title':'Create Meetings',
        'selected_meeting_type':selected_meeting_type,
        'consultations':consultations
    }

    return render(request,"pages-green/meetings/create.html",context)

    #if request.method == 'GET' and request.POST.get('meeting_type'):
    #    selected_meeting_type = request.POST.get('meeting_type')
    #meeting_types_instance = meeting_types.copy()
    #meeting_types_instance.remove(selected_meeting_type)
    #meeting_types_instance.insert(0, selected_meeting_type)
    
   # context = {
   #     'meeting_types_instance': meeting_types_instance,
   #     'meeting_types': meeting_types,
   #     'title': 'Create Meetings',
   #     'selected_meeting_type': selected_meeting_type
   # }
    
   # return render(request, 'pages-green/meetings/create.html', context)


# @login_required(login_url='/signin')
# def view_public_meeting_change(request):
#     context = {}
#
#
#     return render(request, 'pages/meeting-consultations_page.html', context)


@login_required(login_url='/signin')
@approved_required
def instant_meeting_create(request: WSGIRequest) -> HttpResponse:
    return HttpResponseRedirect(create_new_meeting_and_return_link())

    # selected_meeting_type = meeting_types[2]
    # meeting_types_instance = meeting_types.copy()
    # meeting_types_instance.remove(selected_meeting_type)
    # meeting_types_instance.insert(0, selected_meeting_type)
    #
    # context = {
    #     'meeting_types_instance': meeting_types_instance,
    #     'meeting_types': meeting_types,
    #     'title': 'Create Instant Meeting',
    #     'selected_meeting_Type': selected_meeting_type,
    #     'created_meeting': selected_meeting_type,
    #     'meeting_link': meeting_link,
    # }
    #
    # return render(request, 'pages/instant_meetings.html',context)


def instant_meeting_viewer(request: WSGIRequest, id: str) -> HttpResponse:
    """
    Viewer for instant meeting links.
    Wraps a Jitsi meeting instance.
    """

    # Collect user info
    if request.user.is_authenticated:
        user: CustomUser = request.user
        user_name = user.display_name
        user_email = user.email

        # TODO In the future, create a more robust system where meetings have designated moderators (as part of a meetings table or something)
        is_moderator = True
    else:
        user_name = 'Guest'
        user_email = 'guest@example.com'
        is_moderator = False

    # Create a Jitsi JWT
    jwt = create_jaas_jwt(user_name, user_email, is_moderator)

    return render(request, 'pages/instant_meetings.html', {
        'meeting_id': id,
        'jwt': jwt,
        'key_id': JITSI_API_KEY_ID,
    })


# def booking_calendar(request):
#     return render(request,'pages/booking_calendar.html')
#
#     # meeting = ScheduleMeeting.objects.filter(creator=request.user).first()
#     #
#     # selected_meeting_type = meeting_types[2]
#     # meeting_types_instance = meeting_types.copy()
#     # meeting_types_instance.remove(selected_meeting_type)
#     # meeting_types_instance.insert(0, selected_meeting_type)
#     #
#     # context = {
#     #     'meeting_types_instance': meeting_types_instance,
#     #     'meeting_types': meeting_types,
#     #     'title': 'Create Meetings',
#     #     'selected_meeting_type': selected_meeting_type,
#     #     "created_meeting": selected_meeting_type,
#     #     "schedule": meeting,
#     #     'meeting_link': meeting.meeting_link,
#     # }
#     #
#     # return render(request, 'pages-green/meetings/create.html', context)

# ===================================== CAMPAIGN BUILDER PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def compaign_builder(request):
    return render(request, 'pages-green/compaign-builder.html', {'title': 'Compaign Builder'})


# ===================================== EVENTS PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def events(request):
    return render(request, 'pages-green/events.html', {'title': 'Events'})


# ===================================== HELP DOCS PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def help_docs(request):
    return render(request, 'pages-green/help-docs.html', {'title': 'Help Docs'})


# ===================================== CUSTOMER SUPPORT PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def customer_support(request):
    return render(request, 'pages-green/customer-support.html', {'title': 'Customer Support'})


# ===================================== VIDEO WALKTHROUGHS PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def video_walkthroughs(request):
    return render(request, 'pages-green/video-walkthroughs.html', {'title': 'Video Walkthroughs'})


# ===================================== SOCIAL MANAGEMENT PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def social_management(request):
    return render(request, 'pages-green/social-mangement.html', {'title': 'Social Management'})


# Create meeting / events
@login_required(login_url='/signin')
def create_meeting(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            event_link = request.POST.get('event_link')
            duration = request.POST.get('duration')
            description = request.POST.get('description')

            meeting = Meetings.objects.create(
                user=request.user,
                title=title,
                duration=duration,
                description=description,
                event_link=event_link,
            )

            # Retrieve all meetings for the current user
            user_meetings = Meetings.objects.filter(user=request.user)

            # Pass the user's meetings in the context
            return redirect('visible_meetings')
        except ValidationError as e:
            # Handle validation errors
            return HttpResponseServerError(str(e))
    else:
        # If it's not a POST request, simply render the template without creating a meeting
        return render(request, 'pages/meetings.html')


# set meeting visibility

# @login_required(login_url='/signin')
# def toggle_meeting_visibility(request, meeting_id):
#     meeting = get_object_or_404(Meetings, pk=meeting_id)
#
#     meeting.is_hidden = not meeting.is_hidden
#     meeting.save()
#
#     # Redirect to the appropriate URL, update with the actual name or URL
#     return redirect('visible_meetings')
#
#
# # show all meetings that are visible
# @login_required(login_url='/signin')
# def visible_meetings(request):
#     # Retrieve all meetings with is_hidden set to False
#     meetings = Meetings.objects.filter(user=request.user, is_hidden=False).order_by('date')
#     return render(request, 'pages/meetings.html', {'meetings': meetings})
#
# @login_required(login_url='/signin')
# def current_meetings(request):
#     # Retrieve meetings associated with the current user, is_hidden set to False, and date is today
#     meetings = Meetings.objects.filter(user=request.user, is_hidden=False, date=timezone.now().date()).order_by('start_time')
#     return render(request, 'pages/meetings.html', {'meetings': meetings})
#
# @login_required(login_url='/signin')
# def past_meetings(request):
#     # Retrieve past meetings associated with the current user and is_hidden set to False
#     meetings = Meetings.objects.filter(user=request.user, is_hidden=False, date__lt=timezone.now().date()).order_by('-date', '-start_time')
#     return render(request, 'pages/meetings.html', {'meetings': meetings})
#
# @login_required(login_url='/signin')
# def future_meetings(request):
#     # Retrieve future meetings associated with the current user and is_hidden set to False
#     meetings = Meetings.objects.filter(user=request.user, is_hidden=False, date__gt=timezone.now().date()).order_by('date', 'start_time')
#     return render(request, 'pages/meetings.html', {'meetings': meetings})