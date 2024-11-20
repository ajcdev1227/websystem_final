import glob
import json
import os
import random
import re
import subprocess
from datetime import datetime, timedelta

import facebook
import pytz
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponse, \
    HttpResponseBadRequest
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from icalendar import Calendar, Event
from pytz import timezone

from adminapp.models import AvailableTime, DemoMeeting
from core import settings
from core.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from home.constants import COMPLIANCE_STATUS, APP_DOMAIN
from home.decorators import unauthenticated_user, approved_required
from home.forms import DateTimeForm
from home.models import CustomUser, Pages, Slug, Submission, ScheduleMeeting, Article


def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)


# =====================================  USER SIGN IN PAGE =========================================
from home.utils import take_page_screenshot, send_email, generate_random_string


@unauthenticated_user
def sign_in(request):
    if request.method == "GET":
        return render(request, 'demo/auth/login.html')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'No Registered!')
            return HttpResponseRedirect('/signin')


# ===================================== CONFIRM IF EMAIL EXISTS =========================================
def email_validation(request):
    email = request.POST.get('email')
    user = CustomUser.objects.filter(email=email)
    if user.exists():
        return JsonResponse({
            "data": 1,
            "message": "The email is already registered",
            "status": "errors"
        }, status=200)
    else:
        return JsonResponse({
            "data": 0,
            "message": "",
            "status": "success"
        }, status=200)


# ===================================== Tenant USER LOGOUT ================================================
@login_required(login_url='/signin')
def sign_out(request):
    user = request.user
    Article.objects.filter(user=user).delete()
    Pages.objects.filter(user=user).delete()
    ScheduleMeeting.objects.filter(creator=user).delete()
    Slug.objects.filter(author=user).delete()
    Submission.objects.filter(submitter=user).delete()
    logout(request)
    return HttpResponseRedirect('/signin')


# ===================================== DASHBOARD PAGE ================================================
@login_required(login_url='/signin')
@approved_required
def dashboard(request):
    return render(request, 'pages/dashboard.html')


# ===================================== WEBSITE PAGE ================================================
@login_required(login_url='/signin')
def website(request):
    return render(request, 'pages/wesite.html')


# ===================================== CONTACTS PAGE ================================================
@login_required(login_url='/signin')
def contacts(request):
    return render(request, 'pages/contacts.html')


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
    queue_list = Pages.objects.filter(user=request.user).order_by('-id')
    query = request.GET.get('q')
    if query:
        queue_list = Pages.objects \
            .filter(user=request.user) \
            .filter(page_name__contains=query) \
            .order_by('-id')

    paginator = Paginator(queue_list, 15)
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
    return render(request, 'pages/editor-list.html', context)


# ===================================== Create a PAGE ================================================
@login_required(login_url='/signin')
def create_page(request):
    if request.method == "POST":
        page_name = request.POST.get('page_name')
        user = request.user
        Pages.objects.create(user=user, page_name=page_name)
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
        'domain': f'demo.{APP_DOMAIN}',
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

    meeting = ScheduleMeeting.objects.filter(creator=user)
    if meeting.exists():
        return redirect('/')

    cnt_admin = CustomUser.objects.filter(role__gte=1).count()
    rest = user.id % cnt_admin
    group = rest + 1
    ScheduleMeeting.objects.update_or_create(
        creator_id=user.id,
        defaults={
            "group": group,
        })
    return render(request, "auth/success.html")


@login_required(login_url='/signin')
def schedulecall(request):
    return render(request, "auth/schedulecall.html")


@login_required(login_url='/signin')
def chooseschedule(request):
    user = request.user
    cnt_admin = CustomUser.objects.filter(role__gte=1).count()
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
    if request.method == "GET":
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
            timezone_str = form.cleaned_data['timezone']
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
            meeting, created = ScheduleMeeting.objects.update_or_create(
                creator_id=request.user.id,
                defaults={
                    "date": date,
                    "time": time,
                    "timezone": timezone_str,
                    "aware_datetime": aware_datetime,
                    "end_time": meeting_end_datetime.time()
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
            'domain': f'demo.{APP_DOMAIN}',
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

    context = {
        "user": customer
    }

    return render(request, "pages/settingsgear.html", context)


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
            "articles": articles
        }
        return render(request, "pages/articles.html", context)
    else:
        return redirect("/obtain_access_token")


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



def welcome(request):
    demo_domain = f'demo.{APP_DOMAIN}'
    app_domain = demo_domain.replace('demo', 'app')
    signup_url = f"{app_domain}/signup"
    appointment = f"{demo_domain}/appointment"
    context = {
        'signup': signup_url,
        'appointment': appointment
    }
    return render(request, 'demo/pages/welcome.html', context)






# =====================================Professor Calendar=====================================
def appointment(request):
    form = DateTimeForm()
    showcaser_cnt = CustomUser.objects.filter(role=3).count()
    random_number = -random.randint(1, showcaser_cnt)
    context = {
        'form': form,
        'group': random_number,
    }
    return render(request, 'demo/pages/appointment.html', context)


def getavailabletime(request):
    if request.method == 'POST':
        group = request.POST.get('group')
        date = request.POST.get('date')
        time = AvailableTime.objects.filter(Q(date=date) & Q(group=group))
        if time.exists():
            time = time.values()[0]
        else:
            time = None

        response = {
            "message": "",
            "status": "success",
            "data": time,
        }
        return JsonResponse(response, status=200)

def enterdetail(request):
    global meeting
    if request.method == 'GET':
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        timezone = request.GET.get('timezone')
        group = request.GET.get('group')


        request.session['start_time'] = start_time
        request.session['end_time'] = end_time

        format_string = "%Y-%m-%d %H:%M:%S%z"
        start_time = datetime.strptime(start_time, format_string)
        end_time = datetime.strptime(end_time, format_string)
        context = {
            "start_time": start_time.time(),
            "end_time": end_time.time(),
            "date": start_time.date(),
            "timezone": timezone,
            "group": group
        }
        return render(request, 'demo/pages/enterdetail.html', context)

    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        if form.is_valid():
            # Process the form data
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            local_timezone = form.cleaned_data['timezone']
            timezone_str = "EST"
            available_times = form.cleaned_data['available_times']
            group = request.POST.get('group')
            tz = pytz.timezone(timezone_str)
            aware_datetime = tz.localize(datetime.combine(date, time))
            meeting_start_datetime = datetime.combine(date, time)
            meeting_end_datetime = meeting_start_datetime + timedelta(minutes=60)
            current_time = datetime.now()
            if current_time >= meeting_start_datetime:
                messages.error(request, "The meeting time needs to be scheduled for a time that is later \
                                        than the current time")
                return redirect(request.META.get('HTTP_REFERER'))
            # Perform additional actions with the data

            converted_start_time = tz.localize(meeting_start_datetime).astimezone(pytz.timezone(local_timezone))
            converted_end_time = tz.localize(meeting_end_datetime).astimezone(pytz.timezone(local_timezone))



            AvailableTime.objects.filter(Q(group=group) & Q(date=meeting_start_datetime.date())).update(
                times=available_times)

            return redirect(f'/enterdetail?start_time={converted_start_time}'
                            f'&end_time={converted_end_time}&timezone={local_timezone}&group={group}')
        else:
            messages.error(request, "You have to choose the scheduled datetime.")
            return redirect(request.META.get('HTTP_REFERER'))

def confirmed(request):
    if request.method == "GET":
        name = request.GET.get('name')
        email = request.GET.get('email')
        description = request.GET.get('description')
        meeting_link = generate_random_string(20)
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        date = request.GET.get('date')
        timezone = request.GET.get('timezone')
        group = request.GET.get('group')

        email_subject = "Your WebSystem Live Onboarding"
        message = render_to_string('email/schedule_meeting.html', {
            'meeting': {
                "time": start_time,
                "end_time": end_time,
                "date": date,
                "meeting_link": meeting_link
            },
            'domain': f'demo.{APP_DOMAIN}',
            'schema': request.scheme
        })
        try:
            if 'start_time' in request.session and 'end_time' in request.session:
                send_email(
                    email,
                    email_subject,
                    message,
                    is_html=True,
                )

                format_string = "%Y-%m-%d %H:%M:%S%z"
                start_obj = datetime.strptime(request.session['start_time'], format_string)
                end_obj = datetime.strptime(request.session['end_time'], format_string)
                del request.session['start_time']
                del request.session['end_time']
                showcasher = CustomUser.objects.filter(Q(group=group) & Q(role=3)).first()
                DemoMeeting.objects.create(
                    showcasher=showcasher,
                    date=start_obj.date(),
                    time=start_obj.time(),
                    end_time=end_obj.time(),
                    timezone=timezone,
                    email=email,
                    content=description,
                    name=name,
                    meeting_link=meeting_link,
                )
                messages.success(request, f'Please check your email for meeting time.')

            context = {
                "name": name,
                "email": email,
                "description": description,
                "meeting_link": meeting_link,
                "start_time": start_time,
                "end_time": end_time,
                "date": date,
                "timezone": timezone
            }
            return render(request, "demo/pages/confirmed.html", context)
        except Exception as e:
            messages.success(request, str(e))
            return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect('/')

# =====================================End Professor Calendar=====================================