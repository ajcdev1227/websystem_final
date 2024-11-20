import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect, JsonResponse
from django.template.defaultfilters import slugify
from django.shortcuts import render

from home.constants import APP_DOMAIN, APP_HOST, CRM_ROOT
from home.decorators import unauthenticated_user
from home.models import CustomUser, Client, Domain, TenantUser, Company
from home.utils import generate_short_uuid, only_alphabets, create_login_token, meeting_link_for_id


def auth_redirect_logic(request: WSGIRequest, user: CustomUser) -> HttpResponseRedirect:
    # Don't send a token if this is a demo user
    if user.role < 0:
        messages.add_message(request, messages.ERROR, 'You are demo user.')
        return HttpResponseRedirect('/signin')

    login_token = create_login_token(user.username)  # username is actually an email

    # Determine where to go.
    # If no next URL was specified, go to the home site.
    next_url = request.GET.get('next', None)
    if next_url is None:
        next_url = f"{request.scheme}://home.{APP_DOMAIN}/dologin"

    direct_url = next_url

    if '?' in direct_url:
        direct_url += '&'
    else:
        direct_url += '?'

    direct_url += 'token=' + login_token
    return HttpResponseRedirect(direct_url)


def sign_in(request: WSGIRequest, *args, **kwargs) -> HttpResponseRedirect:
    if request.user.is_authenticated:
        return auth_redirect_logic(request, request.user)

    if request.method == "GET":
        # Show login page
        context = {}

        # We'll select a template based on the app name, or stick with login.html if default or omitted
        template = 'login.html'

        app_name = request.GET.get('app', 'default')
        if app_name == 'compliance':
            template = 'compliance_login.html'

        return render(request, 'auth/' + template, context)
    if request.method == "POST":
        # Authenticate with credentials
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user is None:
            messages.add_message(request, messages.ERROR, 'Invalid email or password')
            return HttpResponseRedirect(request.build_absolute_uri())
        else:
            login(request, user)

        return auth_redirect_logic(request, user)


def sign_out(request: WSGIRequest) -> HttpResponseRedirect:
    logout(request)

    return HttpResponseRedirect(request.GET.get('next', '/signin'))


def send_post_request(customer_data_for_crm):
    php_url = CRM_ROOT + '/scripts/_account-user-add.php'

    response = requests.post(php_url, data=customer_data_for_crm)


'''
sign up - we send a user and a company ( company , id)
add new users to this tenant -> we send the user and the company id ,

select company,id from company where id = input_id ;
then assign the company to the user
'''
''' 
On our signup - We send post request with user and company (id,company) 
Add new users to the tenant - we send the user and the company id it belongs to
'''

# for send post request
# '''
# "phone": "(221)2223344",
# "timezone": "EST",
# "notes": "test notes",
# "twilio_phone": "9998884455",
# "twilio_sid": "kjsyetrxdf",
# "twilio_token": "pirstrwvn",
# "use_system_twilio": "0"
# '''


# ===================================== SIGN UP PAGE =========================================
@unauthenticated_user
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

        personal_meeting_link = slugify(company) + "-meeting-room"

        # TODO Validate all signup info before doing anything

        # login in to php website
        # when you click on  the button, then send post request with email and (cms flag) password_encoded
        # then get the email and decode the password and call the normal login function or route create php session
        # django by default creates session login token

        # Form will go to CRM via post requests

        # try / catch for email and lead

        company_instance = Company.objects.create(
            company=company
        )

        company_instance.save()

        user = CustomUser(
            email=email,
            username=email,
            display_name=username,
            password=hash_password,
            phonenumber=phonenumber,
            c_members=c_members,
            customer_id=customer_id,
            is_superuser=1,
            personal_meeting_link=personal_meeting_link
        )
        user.company = company_instance
        user.save()

        # This sends a meeting link like http://home.site.com/meeting/pinegrove-financial-meeting-room/
        full_meeting_link = meeting_link_for_id(personal_meeting_link)
        # splits the username to php site
        nameParts = username.split(' ')
        firstname = nameParts[0]
        lastname = nameParts[-1]

        # FOR CRM ACCOUNT CREATION
        customer_data_for_crm = {
            "acx_customer_id": customer_id,
            "customer_name": company,
            "first_name": firstname,
            "last_name": lastname,
            "email": email,
            "nickname": password,
            "acx_meeting_url": full_meeting_link,
        }

        # Send post request to CRM
        send_post_request(customer_data_for_crm)

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
            direct_url = f"{request.scheme}://home.{APP_DOMAIN}"
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
