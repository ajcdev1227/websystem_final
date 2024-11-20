import glob
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, date

import facebook
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, HttpResponseBadRequest, \
    JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from nylas import APIClient
from pytz import timezone

from adminapp.models import TenantOption, AvailableTime, DemoMeeting
from core.settings import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from home.constants import COMPLIANCE_STATUS, APP_NYLAS_REDIRECT_URL_ADMIN, APP_DOMAIN, OFFICER_ROLE
from home.decorators import approved_required, super_admin
from home.forms import DateTimeForm
from home.models import CustomUser, Submission, Pages, Slug, ScheduleMeeting, Article, Client
from home.utils import generate_short_uuid, take_page_screenshot, send_email, base64_encode, generate_calendar_invite, \
    initialize_nylas_client, create_login_token, update_user_enable_self_managed_compliance
from compliance.models import OfficerTenantAssignment
from django.db.models import F

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def admin_login(request):
    if request.method == "GET":
        print("------------------------------")
        return render(request, 'admin/auth/login.html')
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.role >= 1:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.add_message(request, messages.ERROR, 'You do not have admin role!')
                logout(request)
                return HttpResponseRedirect('/login')
        else:
            user_email = CustomUser.objects.filter(email=email)
            if user_email.exists():
                messages.add_message(request, messages.ERROR, 'You entered wrong password.')
            else:
                messages.add_message(request, messages.ERROR, 'No Registered!')
            return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def tenants(request):
    if request.method == "GET":
        users = (CustomUser.objects
                 .filter(tenantuser__isnull=False)
                 .order_by('-id'))

        query = request.GET.get('q')
        if query:
            users = users.filter(email__contains=query)

        paginator = Paginator(users, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'tenants': posts
        }
        return render(request, 'admin/pages/tenants.html', context)


# ===================================== Tenant USER LOGOUT ================================================
@login_required(login_url='/login')
def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def tenant_for_id(request, id):
    user_tenant = CustomUser.objects.filter(customer_id=id).first()

    # If the user is an officer, fetch assigned tenants
    assigned_tenants: list[Client] = []

    if user_tenant.role == OFFICER_ROLE:
        assigned_tenants = list(Client.objects.filter(officertenantassignment__officer_id=user_tenant.id))

    context = {
        'tenant': user_tenant,
        'assigned_tenants': assigned_tenants
    }

    return render(request, 'admin/pages/tenant.html', context)


# TODO Security note: Ensure the user has to be an admin to access this route
@login_required(login_url='/login')
def tenant(request):
    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'enable-managed-compliance':
            username = request.POST.get('username')
            enable = request.POST.get('enable-self-managed-compliance')

            update_user_enable_self_managed_compliance(username, enable == 'on')

        elif action == 'enable-production':
            id = request.POST.get('id')
            approved = request.POST.get('approved')

            if approved is not None:
                if approved == '0':
                    CustomUser.objects.filter(id=id).update(approved=1)
                else:
                    CustomUser.objects.filter(id=id).update(approved=0)

        elif action == 'is-compliance-officer':
            id = int(request.POST.get('id'))
            is_officer = request.POST.get('is-compliance-officer')

            if is_officer == 'on':
                role = OFFICER_ROLE
            else:
                role = 0

            CustomUser.objects.filter(id=id).update(role=role)

        elif action == 'remove-assigned-tenant':
            tenant_id = int(request.POST.get('tenant-id'))
            officer_id = int(request.POST.get('officer-id'))

            OfficerTenantAssignment.objects.filter(tenant_id=tenant_id, officer_id=officer_id).delete()

        elif action == 'add-assigned-tenant':
            officer_id = int(request.POST.get('officer-id'))
            tenant_email = request.POST.get('email', '').strip().lower()

            if tenant_email != '':
                client = Client.objects.filter(tenant_name=tenant_email).first()

                if client is None:
                    messages.add_message(request, messages.ERROR, 'No tenant with that email found')
                else:
                    # Check for existing assignment
                    existing = OfficerTenantAssignment.objects.filter(officer_id=officer_id, tenant_id=client.id).first()

                    if existing is None:
                        OfficerTenantAssignment.objects.create(officer_id=officer_id, tenant_id=client.id).save()

        messages.add_message(request, messages.SUCCESS, 'Options updated')

    referer_url = request.META.get('HTTP_REFERER', '/tenants')
    return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def dashboard(request):
    if 'tenant_id' in request.session:
        del request.session['tenant_id']
    return render(request, 'admin/pages/dashboard.html')


@login_required(login_url='/login')
@super_admin
def admin(request):
    if request.method == "GET":
        return render(request, 'admin/pages/add_admin.html')
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                cnt_admin = CustomUser.objects.filter(role__gte=1).count()
                group = cnt_admin + 1
                customer_id = generate_short_uuid()
                CustomUser.objects.create(first_name=firstname, last_name=lastname, email=email, username=email
                                          , role=1, password=make_password(password),
                                          customer_id=customer_id, group=group)
                messages.add_message(request, messages.SUCCESS, 'Added a new admin successfully.')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            messages.add_message(request, messages.ERROR, 'Please Confirm Password Again.')

        referer_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def admins(request):
    if request.method == "GET":
        users = CustomUser.objects.filter(Q(role=1) | Q(role=2)).order_by('group')
        query = request.GET.get('q')
        if query:
            users = CustomUser.objects.filter(Q(role=1) | Q(role=2)).filter(email__contains=query).order_by('group')

        paginator = Paginator(users, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'tenants': posts
        }
        return render(request, 'admin/pages/admin_list.html', context)


@login_required(login_url='/login')
@super_admin
def demo_user(request):
    if request.method == "GET":
        return render(request, 'admin/pages/add_demo_user.html')
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                customer_id = generate_short_uuid()
                demo_user = CustomUser.objects.create(first_name=firstname, last_name=lastname, email=email,
                                                      username=email, role=-1, password=make_password(password),
                                                      approved=1,
                                                      customer_id=customer_id, group=-1, company='WebSystem')
                ScheduleMeeting.objects.create(creator=demo_user, status='END', enable_user_to_join='YES',
                                               lock_meeting='YES', group=1)

                messages.add_message(request, messages.SUCCESS, 'Added a new admin successfully.')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            messages.add_message(request, messages.ERROR, 'Please Confirm Password Again.')

        referer_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def demo_users(request):
    if request.method == "GET":
        users = CustomUser.objects.filter(Q(role=-1)).order_by('group')
        query = request.GET.get('q')
        if query:
            users = CustomUser.objects.filter(Q(role=-1)).filter(email__contains=query).order_by('group')

        paginator = Paginator(users, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'tenants': posts
        }
        return render(request, 'admin/pages/demo_user_list.html', context)


@login_required(login_url='/login')
@super_admin
def update_demo_user(request, id):
    if request.method == 'GET':
        demo_user = CustomUser.objects.get(customer_id=id)
        context = {
            "demo_user": demo_user,
        }
        return render(request, 'admin/pages/update_demo_user.html', context)
    if request.method == 'POST':
        referer_url = request.META.get('HTTP_REFERER')
        try:
            password = request.POST.get('password')
            CustomUser.objects.filter(id=id).update(password=make_password(password))
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(referer_url)
        messages.add_message(request, messages.SUCCESS, 'Changed the Demo User password Successfully.')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
@super_admin
def showcaser(request):
    if request.method == "GET":
        return render(request, 'admin/pages/add_showcaser.html')
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                customer_id = generate_short_uuid()
                group = -CustomUser.objects.filter(role=3).count() - 1
                demo_user = CustomUser.objects.create(first_name=firstname, last_name=lastname, email=email,
                                                      username=email, role=3, password=make_password(password),
                                                      approved=1,
                                                      customer_id=customer_id, group=group, company='WebSystem')
                ScheduleMeeting.objects.create(creator=demo_user, status='END', enable_user_to_join='YES',
                                               lock_meeting='YES', group=1)

                messages.add_message(request, messages.SUCCESS, 'Added a new admin successfully.')
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            messages.add_message(request, messages.ERROR, 'Please Confirm Password Again.')

        referer_url = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def showcasers(request):
    if request.method == "GET":
        users = CustomUser.objects.filter(Q(role=3)).order_by('group')
        query = request.GET.get('q')
        if query:
            users = CustomUser.objects.filter(Q(role=3)).filter(email__contains=query).order_by('group')

        paginator = Paginator(users, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'tenants': posts
        }
        return render(request, 'admin/pages/showcasers.html', context)


@login_required(login_url='/login')
def showcasedashboard(request):
    if request.method == "GET":
        cnt_admin = CustomUser.objects.filter(role__gte=1).count()
        user = request.user
        print(user.id)
        # meetings = ScheduleMeeting.objects.annotate(remainder=F('id') % cnt_admin).filter(remainder=group-1).all()
        meetings = DemoMeeting.objects.filter(showcasher=user)
        context = {
            "meetings": meetings,
            "domain": f"{request.scheme}://admin.{APP_DOMAIN}"
        }
        return render(request, 'admin/pages/showcaserdashboard.html', context)


@login_required(login_url='/login')
@super_admin
def update_showcasher(request, id):
    if request.method == 'GET':
        showcaser = CustomUser.objects.get(customer_id=id)
        context = {
            "showcasher": showcaser,
        }
        return render(request, 'admin/pages/update_showcasher.html', context)
    if request.method == 'POST':
        referer_url = request.META.get('HTTP_REFERER')
        try:
            password = request.POST.get('password')
            CustomUser.objects.filter(id=id).update(password=make_password(password))
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(referer_url)
        messages.add_message(request, messages.SUCCESS, 'Changed the Showcasher password Successfully.')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def profile(request):
    return render(request, 'admin/pages/profile.html')


@login_required(login_url='/login')
@super_admin
def update_admin(request, id):
    admin = CustomUser.objects.get(customer_id=id)
    cnt_group = CustomUser.objects.filter(role__gte=1).count()
    context = {
        "admin": admin,
        'cnt_group': cnt_group
    }
    return render(request, 'admin/pages/update_admin.html', context)


@login_required(login_url='/login')
@super_admin
def update_post_admin(request):
    if request.method == "POST":
        referer_url = request.META.get('HTTP_REFERER')
        try:
            user_id = request.POST.get('user_id')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            group = request.POST.get('group')
            password = request.POST.get('password')
            CustomUser.objects.filter(id=user_id).update(first_name=firstname
                                                         , last_name=lastname
                                                         , email=email, username=email
                                                         , group=group)
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(referer_url)
        messages.add_message(request, messages.SUCCESS, 'Updated Successfully.')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
@super_admin
def change_admin_password(request):
    if request.method == "POST":
        referer_url = request.META.get('HTTP_REFERER')
        try:
            user_id = request.POST.get('user_id')
            password = request.POST.get('password')
            CustomUser.objects.filter(id=user_id).update(password=make_password(password))
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))
            return HttpResponseRedirect(referer_url)
        messages.add_message(request, messages.SUCCESS, 'Changed the password Successfully.')
        return HttpResponseRedirect(referer_url)


@login_required(login_url='/login')
def changepassword(request):
    if request.method == "POST":
        user = CustomUser.objects.get(email=request.user.email)
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        c_pass = request.POST.get('confirm_password')
        user_exist = authenticate(username=request.user.email, password=old_pass)
        referer_url = request.META.get('HTTP_REFERER')
        if user_exist is not None:
            if c_pass == new_pass:
                user.set_password(new_pass)
                user.save()
            else:
                messages.add_message(request, messages.ERROR, 'Please Confirm New Password Again.')
                return HttpResponseRedirect(referer_url)
        else:
            messages.add_message(request, messages.ERROR, 'You can not change the password.')
            return HttpResponseRedirect(referer_url)
        messages.add_message(request, messages.SUCCESS, 'You have changed your password successfully. Please login \
                                                        again with new password.')
        return HttpResponseRedirect(referer_url)



@login_required(login_url='/login')
def update_meeting_info(request):
    if request.method == "POST":
        meeting_id = request.POST.get('meeting_id')
        lock_meeting = request.POST.get('lock_meeting')
        onboarding_meeting_url = request.POST.get('onboarding_meeting_url')
        enable_user_to_join = request.POST.get('enable_user_to_join')
        meeting = ScheduleMeeting.objects.get(id=meeting_id)
        to_email = meeting.creator.email
        meeting.meeting_link = onboarding_meeting_url
        meeting.enable_user_to_join = enable_user_to_join
        meeting.lock_meeting = lock_meeting
        meeting.save()
        email_subject = "Notice! Information about your WebSystem Meeting."
        message = render_to_string('email/changed_meeting_info_by_admin.html', {
            'meeting': meeting,
            'domain': f'admin.{APP_DOMAIN}',
            'schema': request.scheme
        })

        try:
            send_email(
                to_email,
                email_subject,
                message,
                is_html=True,
            )
            messages.success(request, 'Changed the infos successfully.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/login')
def save_tenant_option(request):
    if request.method == "POST":
        tenant_id = request.POST.get('tenant_id')
        user_url = request.POST.get('user_url')
        dns_settings = request.POST.get('dns_settings')
        billing_info = request.POST.get('billing_info')
        youtube_acc_link = request.POST.get('youtube_acc_link')
        twilio_acc = request.POST.get('twilio_acc')
        color_palette = request.POST.get('color_palette')
        plan = request.POST.get('plan')
        rtmp = request.POST.get('rtmp')

        tenantOption = TenantOption.objects.filter(user_id=tenant_id)
        if tenantOption.exists():
            tenantOption.update(tenant_url=user_url, dns_settings=dns_settings, billing_info=billing_info
                                , youtube_acc_link=youtube_acc_link,
                                twilio_acc=twilio_acc, color_palette=color_palette, plan=plan, rtmp=rtmp)
        else:
            tenantOption.create(user_id=tenant_id, tenant_url=user_url, dns_settings=dns_settings,
                                billing_info=billing_info
                                , youtube_acc_link=youtube_acc_link,
                                twilio_acc=twilio_acc, color_palette=color_palette, plan=plan, rtmp=rtmp)

        response = {
            "message": "",
            "status": "success"
        }
        return JsonResponse(response, status=200)


# ===================================== Jitsi meeting ================================================
@login_required(login_url='/login')
def meetingsystem(request):
    if request.method == "GET":
        users = ScheduleMeeting.objects.filter(creator__role=0).order_by('-id')
        query = request.GET.get('q')
        if query:
            users = (ScheduleMeeting.objects.filter(creator__role=0)
                     .filter(Q(name__contains=query) | Q(creator__email__contains=query)).order_by('-id'))
        paginator = Paginator(users, 15)
        page = request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context = {
            'meetings': posts
        }
        return render(request, 'admin/pages/meetingsystem.html', context)


@login_required(login_url='/login')
def meetingconfig(request):
    if request.method == "GET":
        cnt_admin = CustomUser.objects.filter(role__gte=1).count()
        group = request.user.group
        # meetings = ScheduleMeeting.objects.annotate(remainder=F('id') % cnt_admin).filter(remainder=group-1).all()
        meetings = ScheduleMeeting.objects.filter(group=group)
        context = {
            "meetings": meetings,
            "domain": f"{request.scheme}://admin.{APP_DOMAIN}"
        }
        return render(request, 'admin/pages/meetingconfig.html', context)


@login_required(login_url='/login')
def scheduler(request):
    return render(request, 'admin/pages/scheduler.html')


@login_required(login_url='/login')
def connectcalendar(request):
    return render(request, 'admin/pages/connectcalendar.html')


@login_required(login_url='/login')
def meeting(request):
    meeting_link = request.GET.get('id')

    context = {
        "meeting_link": meeting_link
    }
    return render(request, 'admin/pages/meeting.html', context)


@login_required(login_url='/login')
def save_available_time(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        times = request.POST.get('times')
        user = request.user
        AvailableTime.objects.update_or_create(
            date=date,
            defaults={
                "admin": user,
                "group": user.group,
                "date": date,
                "times": times
            }
        )
        response = {
            "message": "success",
            "status": "success"
        }
        return JsonResponse(response, status=200)


@login_required(login_url='/login')
def getavailabletime(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        time = AvailableTime.objects.filter(Q(date=date) & Q(group=request.user.group))
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


# ========================== Start Connect Nylas ===========================
def connect_nylas(request):
    user = request.user
    nylas_client = initialize_nylas_client()
    return redirect(nylas_client.authentication_url(APP_NYLAS_REDIRECT_URL_ADMIN, user.email, scopes=["calendar"], state=None))

def login_callback(request):
    user = request.user
    nylas_client = initialize_nylas_client()
    code = request.GET.get('code')
    user.nylas_access_token = nylas_client.token_for_code(code)
    nylas_client.access_token = user.nylas_access_token
    calendars = nylas_client.calendars.all()
    real_calendar = None
    for calendar in calendars:
        if calendar.is_primary:
            real_calendar = calendar
    if real_calendar is None:
        real_calendar = calendars[0]
    user.calendar_id = real_calendar.id
    user.save()
    return redirect('/connectcalendar')



# ========================== End Connect Nylas ===========================

# ========== As Admin ===========
# ===================================== DASHBOARD PAGE ================================================
@login_required(login_url='/login')
def tenant_dashboard(request, id):
    request.session['tenant_id'] = id
    tenant = CustomUser.objects.get(id=id)
    request.tenant = tenant
    return render(request, 'as_admin/pages/dashboard.html')


# ===================================== WEBSITE PAGE ================================================
@login_required(login_url='/login')
def website(request):
    return render(request, 'as_admin/pages/wesite.html')


# ===================================== CONTACTS PAGE ================================================
@login_required(login_url='/login')
def contacts(request):
    return render(request, 'as_admin/pages/contacts.html')


# ===================================== GROUPS PAGE ================================================
@login_required(login_url='/login')
def groups(request):
    return render(request, 'as_admin/pages/groups.html')


# ===================================== EMAIL PAGE ================================================
@login_required(login_url='/login')
def email(request):
    return render(request, 'as_admin/pages/email.html')


# ===================================== FORM PAGE ================================================
@login_required(login_url='/login')
def forms(request):
    return render(request, 'as_admin/pages/forms.html')


# ===================================== CHAT PAGE ================================================
@login_required(login_url='/login')
def chat(request):
    return render(request, 'as_admin/pages/chat.html')


# ===================================== MEETINGS PAGE ================================================
@login_required(login_url='/login')
def meetings(request):
    return render(request, 'as_admin/pages/meeting.html')


# ===================================== compliance PAGE ================================================
@login_required(login_url='/login')
def compliance(request):
    if request.method == "GET":
        tenant = CustomUser.objects.get(id=request.session['tenant_id'])
        request.tenant = tenant

        user_id = request.tenant.id
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
        return render(request, 'as_admin/pages/compliance.html', context)


# ===================================== archive PAGE ================================================
@login_required(login_url='/login')
def archive(request):
    if request.method == "GET":
        tenant = CustomUser.objects.get(id=request.session['tenant_id'])
        request.tenant = tenant
        user_id = request.tenant.id

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
        return render(request, 'as_admin/pages/archive.html', context)


# ===================================== settings PAGE ================================================
@login_required(login_url='/login')
def settingss(request):
    return render(request, 'as_admin/pages/settings.html')


# ===================================== editor list PAGE ================================================
@login_required(login_url='/login')
def editor_list(request):
    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant
    queue_list = Pages.objects.filter(user=request.tenant).order_by('-id')
    query = request.GET.get('q')
    if query:
        queue_list = Pages.objects \
            .filter(user=request.tenant) \
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
    return render(request, 'as_admin/pages/editor-list.html', context)


# ===================================== Create a PAGE ================================================
@login_required(login_url='/login')
def create_page(request):
    if request.method == "POST":
        page_name = request.POST.get('page_name')
        tenant = CustomUser.objects.get(id=request.session['tenant_id'])
        request.tenant = tenant
        user = request.tenant
        Pages.objects.create(user=user, page_name=page_name)
        messages.add_message(request, messages.SUCCESS, 'Created successfully')
        return HttpResponseRedirect('/editor-list')


# ===================================== Editor PAGE ================================================
@login_required(login_url='/login')
def editor(request, slug=None):
    page = Pages.objects.filter(id=slug).first()
    context = {
        "page": page,
        "submission_cnt": page.submissions.count()
    }
    return render(request, 'as_admin/pages/editor.html', context)


# ===================================== Builder PAGE ================================================
@login_required(login_url='/login')
def builder(request, page_id):
    context = {
        "page_id": page_id
    }
    return render(request, 'as_admin/pages/builder.html', context)


@login_required(login_url='/login')
def vvvebjs(request, page_id):
    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant
    html_files = glob.glob(
        os.path.join(settings.STATIC_DIR, 'saved-pages/' + str(request.tenant.id) + '/*.html')) + glob.glob(
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
    return render(request, 'as_admin/page-builder.html', context)


@csrf_exempt
@login_required(login_url='/login')
def save_vvveb_page(request, page_id):
    MAX_FILE_LIMIT = 1024 * 1024 * 2  # 2 Megabytes max html file size

    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    def draft_file_endpoint(file_name):
        file_name = '/saved-pages/' + str(request.tenant.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name))) + ".html"
        file_name = file_name.replace('\\', '/')
        return file_name

    def sanitize_file_name(file_name):
        file_name = re.sub(r'^/static/', '/', file_name)
        # file_name = settings.MEDIA_ROOT + '/saved-pages/' + str(request.tenant.id) + '/' + re.sub(r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)) + '_' + datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        file_name = settings.STATIC_DIR + '/saved-pages/' + str(request.tenant.id) + '/' + file_name + '/' + re.sub(
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
            slug = Slug.objects.create(filename=filename, author=request.tenant)

            # Create new unapproved submission entry
            new_submission = Submission()
            new_submission.slug = filename  # <-- TODO We should have a better slug later
            new_submission.old_version = old_html
            new_submission.new_version = html
            new_submission.submitter_id = request.tenant.id
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


@login_required(login_url='/login')
def vvvebjs_edit(request, page_id):
    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    html_files = glob.glob(
        os.path.join(settings.STATIC_DIR, 'saved-pages/' + str(request.tenant.id) + '/*.html')) + glob.glob(
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
    submission = Submission.objects.filter(submitter_id=request.tenant.id).filter(page_id=page_id).order_by(
        '-id').first()
    context = {
        'pages': pages,
        'submission': submission
    }
    return render(request, 'as_admin/page-builder-edit.html', context)


@csrf_exempt
@login_required(login_url='/login')
def update_save_vvveb_page(request, page_id):
    MAX_FILE_LIMIT = 1024 * 1024 * 2  # 2 Megabytes max html file size

    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    def draft_file_endpoint(file_name):
        file_name = '/saved-pages/' + str(request.tenant.id) + '/' + file_name + '/' + re.sub(
            r'\?.*$', '', re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name))) + ".html"
        file_name = file_name.replace('\\', '/')
        return file_name

    def sanitize_file_name(file_name):
        file_name = re.sub(r'^/static/', '/', file_name)
        # file_name = settings.MEDIA_ROOT + '/saved-pages/' + str(request.tenant.id) + '/' + re.sub(r'\?.*$', '',
        # re.sub(r'\.{2,}', '', re.sub(r'[^\/\\a-zA-Z0-9\-\._]', '', file_name)) + '_' + datetime.now().strftime(
        # "%Y-%m-%d-%H-%M-%S"))
        file_name = settings.STATIC_DIR + '/saved-pages/' + str(request.tenant.id) + '/' + file_name + '/' + re.sub(
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
            slug = Slug.objects.create(filename=filename, author=request.tenant)

            submission = Submission.objects.filter(submitter_id=request.tenant.id) \
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
                new_submission.submitter_id = request.tenant.id
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


@login_required(login_url='/login')
def subitForReview(request, page_id):  # Publish

    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    user = request.tenant
    username = f"{user.first_name} {user.last_name}"
    submission = Submission.objects.filter(submitter_id=request.tenant.id).filter(page_id=page_id)
    submission.update(status=COMPLIANCE_STATUS["pending"])
    submission = submission.first()

    email_subject = f'{user.email} has made changes to page ({submission.slug})'
    message = render_to_string('email/publish.html', {
        'name': username,
        'domain': f'admin.{APP_DOMAIN}',
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
    return render(request, "as_admin/pages/viewer.html", context)


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


@login_required(login_url='/login')
def view_reason(request, submission_id):
    submission = Submission.objects.filter(id=submission_id).first()
    page = Pages.objects.filter(id=submission.page_id).first()
    context = {
        "submission": submission,
        "page_name": page.page_name
    }
    return render(request, "as_admin/pages/reason_viewer.html", context)


@login_required(login_url='/login')
def success(request):
    return render(request, "as_admin/auth/success.html")


@login_required(login_url='/login')
def schedulecall(request):
    return render(request, "as_admin/auth/schedulecall.html")


@login_required(login_url='/signing')
def chooseschedule(request):
    form = DateTimeForm()
    context = {
        "form": form,
    }
    return render(request, 'as_admin/auth/chooseschedule.html', context)


@login_required(login_url='/signing')
def enterdetail(request):
    global meeting
    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        if form.is_valid():
            # Process the form data
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            timezone_str = form.cleaned_data['timezone']
            tz = timezone(timezone_str)
            aware_datetime = tz.localize(datetime.combine(date, time))

            current_datetime = datetime.combine(date, time)
            new_datetime = current_datetime + timedelta(minutes=60)

            # Perform additional actions with the data
            meeting, created = ScheduleMeeting.objects.update_or_create(
                creator_id=request.tenant.id,
                defaults={
                    "date": date,
                    "time": time,
                    "timezone": timezone_str,
                    "aware_datetime": aware_datetime,
                    "end_time": new_datetime.time()
                }
            )

        user = request.tenant
        context = {
            "user": user,
            "schedule": meeting
        }
        return render(request, 'as_admin/auth/enterdetail.html', context)


@login_required(login_url='/signing')
def confirmed(request):
    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    user = request.tenant
    context = {
        "token": base64_encode(generate_calendar_invite(user.email)),
    }
    return render(request, "as_admin/auth/confirmed.html", context)


@login_required(login_url='/signing')
def settingsgear(request):
    tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    request.tenant = tenant

    user = request.tenant
    customer = CustomUser.objects.filter(email=user.email).first()
    context = {
        "user": customer
    }

    return render(request, "as_admin/pages/settingsgear.html", context)


@login_required(login_url='/signing')
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
        return render(request, "as_admin/pages/articles.html", context)
    else:
        return redirect("/obtain_access_token")


# =========================Create a view for obtaining the Access Token======================
@login_required(login_url='/signing')
def obtain_access_token(request):
    redirect_uri = request.build_absolute_uri(reverse('callback'))
    oauth_args = {
        'client_id': FACEBOOK_APP_ID,
        'redirect_uri': redirect_uri,
    }
    login_url = facebook.GraphAPI().get_auth_url(FACEBOOK_APP_ID, redirect_uri)
    return redirect(login_url)


# ===================Create a callback view to handle the authorization code==================
@login_required(login_url='/signing')
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
@login_required(login_url='/signing')
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
                user=request.tenant,
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
        return render(request, 'as_admin/pages/socialsystem.html')


# ===================View an article==================
def article(request, id):
    art = Article.objects.filter(id=id).first()
    context = {
        "article": art
    }
    return render(request, 'as_admin/pages/article.html', context)


def pending(request):
    return render(request, 'as_admin/auth/pending.html')


def create_event(request):
    nylas = APIClient(
        os.getenv('NYLAS_CLIENT_ID'),
        os.getenv('NYLAS_CLIENT_SECRET'),
        os.getenv('NYLAS_ACCESS_TOKEN')
    )

    # Get today’s date
    today = date.today()
    # Today’s date at 12:00:00 am
    START_TIME = int(datetime(today.year, today.month, today.day, 23, 20, 0).timestamp())
    # Today’s date at 11:59:59 pm
    END_TIME = int(datetime(today.year, today.month, today.day, 23, 30, 0).timestamp())
    # Create event draft
    event = nylas.events.create()
    # Define event elements
    event.title = "I am testing now"
    event.location = "Blag's Den!"
    event.when = {"start_time": START_TIME, "end_time": END_TIME}
    event.participants = [{"name": "Blag", 'email': 'lovekite612@outlook.com'}]
    event.calendar_id = "lovekite612@outlook.com"
    # We would like to notify participants
    event.save(notify_participants=True)
    if event.id:
        print("Event created successfully")
    else:
        print("There was an error creating the event")
    pass

    return redirect('/')


def read_calendars(request):
    nylas = APIClient(
        os.getenv('NYLAS_CLIENT_ID'),
        os.getenv('NYLAS_CLIENT_SECRET'),
        os.getenv('NYLAS_ACCESS_TOKEN')
    )
    # Access and print all calendars information
    calendars = nylas.calendars.all()
    for calendar in calendars:
        print("Id: {} | Name: {} | Description: {}".format(
            calendar.id, calendar.name, calendar.description))

    return redirect('/')


# ====================================== Wagtail CMS ===========================================

@login_required(login_url='/signin')
def cms_auth(request):
    token = create_login_token(request.user.email)
    #tenant = CustomUser.objects.get(id=request.session['tenant_id'])
    #token = create_login_token(tenant.email)
    
    return HttpResponseRedirect(f"{request.scheme}://{tenant.tenantuser.tenant.domain_url}/docmslogin?token={token}")
    
@login_required(login_url='/signin')
def a(request):
    return redirect('/')


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
