from django.shortcuts import redirect

from home.models import ScheduleMeeting
from home.utils import is_req_user_officer


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view_func(request, *args, **kwargs)

    return wrapper_func


def approved_required(view_func):
    def wrapper(request, *args, **kwargs):
        # Your logic to check if the user is approved or not
        if request.user.approved == 0:
            meeting = ScheduleMeeting.objects.filter(creator=request.user)
            if not meeting.exists():
                return redirect('/success')

            meeting = meeting.first()

            if meeting.status == 'SCHEDULED' or meeting.status == 'MEETING NOW':
                return redirect('/meetingwait')  # Replace 'not_approved_page' with your actual URL name
            elif meeting.status == 'END':
                return redirect('/pending')  # Replace 'not_approved_page' with your actual URL name
            elif meeting.status == "":
                return redirect('/success')

        return view_func(request, *args, **kwargs)

    return wrapper

def super_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.role != 2:
            # Get the previous URL from the HTTP_REFERER header
            previous_url = request.META.get('HTTP_REFERER')

            if previous_url:
                # Redirect the user back to the previous page
                return redirect(previous_url)
            else:
                # If there's no previous URL, you can redirect to a default page
                return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper_func


def compliance_officer(view_func):
    """
    This route may only be accessed by compliance officers.
    If the user isn't a compliance officer, he or she will be redirected to the last page, or homepage if no last page is available.
    """

    def wrapper_func(request, *args, **kwargs):
        if not is_req_user_officer(request):
            # Get the previous URL from the HTTP_REFERER header
            previous_url = request.META.get('HTTP_REFERER')

            if previous_url:
                # Redirect the user back to the previous page
                return redirect(previous_url)
            else:
                # If there's no previous URL, you can redirect to a default page
                return redirect('/')
        return view_func(request, *args, **kwargs)

    return wrapper_func
