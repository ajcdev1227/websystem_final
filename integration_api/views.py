import json
import re

from django.contrib.auth import login
from django.core.handlers.wsgi import WSGIRequest
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from rest_framework import serializers
from rest_framework.views import APIView

from home.models import CustomUser
from integration_api.decorators import body_validation_serializer, requires_api_auth
from integration_api.utils import api_success_response, api_serializer_validation_error_response, api_error_response, \
    set_connection_schema_by_customer_id
from wagtail.models import Page
from wagtailcms.models import EventsIndexPage, EventPage


class CreateEventSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=64, allow_blank=False)
    slug = serializers.CharField(max_length=64, allow_blank=False)
    event_type = serializers.CharField(max_length=255, allow_blank=False, default='seminar')
    location = serializers.CharField(max_length=1024, allow_blank=False)
    start_time = serializers.DateTimeField()  # Unix epoch
    end_time = serializers.DateTimeField()  # Unix epoch
    intro_description = serializers.CharField(max_length=500)
    event_url = serializers.URLField()
    event_id = serializers.IntegerField()


class Events(APIView):
    """
    The unspecified event endpoint.
    Provides an interface for creating new events.
    """

    @method_decorator(requires_api_auth)
    @method_decorator(body_validation_serializer(serializer_class=CreateEventSerializer))
    def post(self, request: WSGIRequest, customer_id: str) -> JsonResponse:
        if set_connection_schema_by_customer_id(connection, customer_id) is None:
            return api_error_response(400, 'Invalid customer ID')

        # Authenticate the request as the customer
        customer_user = CustomUser.objects.filter(customer_id=customer_id).first()
        login(request, customer_user)

        body = request.validated_body

        slug = body['slug']

        try:
            # events_index = EventsIndexPage.objects.all().first()
            # Index will have to created prior to using API
            # events_index = EventsIndexPage.objects.all().first()

            events_index = Page.objects.type(EventsIndexPage).first()
        except EventsIndexPage.DoesNotExist:
            print("The Events page was NOT found!")
            return JsonResponse(status=400, message="The Events page was NOT found!")

        same_page = EventPage.objects.filter(title=body['title'])

        if re.search("^[a-zA-Z0-9-]+$", slug) is None:
            return JsonResponse({'message': 'Slug must only contain letters, numbers and dashes'}, status=400)

        if EventPage.objects.filter(author=request.user, slug=slug).exists():
            return JsonResponse({'message': 'Event with this slug already exists. Try another.'}, status=409)

        if same_page.exists():
            return api_error_response(400, 'This Event page already exists!')

        event_type = body['event_type']
        location = "<strong>Location:</strong> " + str(body['location'])
        intro_description = body['intro_description']
        event_url = body['event_url']
        event_id = body['event_id']

        # This data has to be sent correctly from CRM. It has to be caught from POST request "Add Events"
        try:
            event_page = EventPage(
                title=body['title'],
                event_type=event_type,
                intro_description=intro_description,
                information_description=location,
                event_url=event_url,
                event_id=event_id,
                author_id=request.user.pk,
                start_date=body['start_time'],
                end_date=body['end_time']
            )

            events_index.add_child(instance=event_page).unpublish()
            new_event_id = event_page.pk

        except Exception as e:
            print("Error: Could NOT create Event page", e)
            return api_error_response(400, 'Could not create event page')

        return api_success_response(data={'id': new_event_id})
