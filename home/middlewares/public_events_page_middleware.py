from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from wagtail.contrib.redirects.middleware import RedirectMiddleware

from home.constants import APP_DOMAIN

import re

from home.models import EventType
from home.views import render_public_events_page, render_public_events_event_type_page
from virtual_calendar.models.calendar_profiles import CalendarProfile


public_page_regex = "^\/([a-zA-Z0-9-]+)\/?$"
public_page_event_regex = "^\/([a-zA-Z0-9-]+)\/([a-zA-Z0-9-]+)\/?$"


class PublicEventsPageMiddleware:
    """
    This middleware handles displaying public event pages for calendar profiles
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest) -> HttpResponse:
        host = request.get_host()
        path = request.path

        profile_slug = None
        event_slug = None

        page_match = re.search(public_page_regex, path)
        if page_match is not None:
            profile_slug = page_match.group(1)
        else:
            page_match = re.search(public_page_event_regex, path)
            if page_match is not None:
                profile_slug = page_match.group(1)
                event_slug = page_match.group(2)

        # Fetch profile to check if it exists
        profile: CalendarProfile = CalendarProfile.objects.filter(user__domain_url=host, url=profile_slug).first()

        # No matching profile was found
        if profile is None:
            return self.get_response(request)

        if event_slug is None:
            return render_public_events_page(request, profile)
        else:
            # Fetch event type
            event_type = EventType.objects.filter(user_id=profile.user_id, slug=event_slug).first()

            if event_type is None:
                return self.get_response(request)
            else:
                return render_public_events_event_type_page(request, profile, event_type)
