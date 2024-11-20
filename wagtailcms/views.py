# from django.shortcuts import render, redirect
# from django import forms
# from django.db import models
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wagtail.models import Page
from rest_framework import serializers

from .models import EventsIndexPage, EventPage


# class CreateEventSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=64, allow_blank=False)
#     slug = serializers.CharField(max_length=64, allow_blank=False)
#     description = serializers.CharField(max_length=2048, allow_blank=True)
#     location = serializers.ChoiceField(choices=EventType.LOCATION_CHOICES)
#     duration = serializers.IntegerField(min_value=1)


@csrf_exempt
def create_event_page(request, customer_id):
    # 8)
    # Make @requires_api_auth decorator that validates a token passed in the Authorization header (look up Bearer Tokens), returns HTTP 403 with JSON {"message": "<the message>"} if not token valid or missing
    # See home/views.py:1552 and onward for how to user serializers to validate JSON bodies -- DONE

    # Have the customer ID as a param -- DONE (We have parameter but need to filter based on Tenant)

    #  - URL format: https://api.websystemcontrol.com/api/v1/tenant/<customer ID>/events -- DONE

    # Validate the body payload like in home/views.py -- DONE

    # Pull data from the validated body like in home/views.py and use it to create the event DONE

    # Once the event is created, return the newly created event ID in the JSON response (field name would be "id" or something) DONE

    # You can heavily reference home/views.py for conventions and whatever DONE

    # Pull the schema from the CustomUser associated with the customer ID param. Remember that it corresponds to customer_id, not company_id. DONE


    # The schema should be used to make sure the Wagtail models in the correct schema are being updated. I don't know how this works, it needs to be figured out.
    # You can't assume it's updating the correct schema because we're not on the same domain as the tenant here (we'll be on the api.<root domain> subdomain).

    if request.method == "POST":
        # post_data = request.POST
        body_val = CreateEventSerializer(data=json.loads(request.body))
        if not body_val.is_valid():
            return JsonResponse({'message': ', '.join([f'{x}: {body_val.errors[x][0]}' for x in body_val.errors.keys()])}, status=400)

        body = body_val.validated_data

        slug = body['slug']
        new_event_id = None

        try:
            # events_index = EventsIndexPage.objects.all().first()
            # Index will have to created prior to using API
            events_index = Page.objects.type(EventsIndexPage).first()
        except EventsIndexPage.DoesNotExist:
            print("The Events page was NOT found!")
            return JsonResponse(status=400, message="The Events page was NOT found!")

        same_page = EventPage.objects.filter(title=body['title'])

        if re.search("^[a-zA-Z0-9-]+$", slug) is None:
            return JsonResponse({'message': 'Slug must only contain letters, numbers and dashes'}, status=400)

        if EventPage.objects.filter(user=request.user, slug=slug).exists():
            return JsonResponse({'message': 'Event with this slug already exists. Try another.'}, status=409)

        if same_page.exists():
            return JsonResponse(status=400, message="This Event page already exists!")

        event_type = "webinar" if body['event_type'] else "seminar"
        location = "Location: " + str(body['location'])
        start_time = "Start time: " + str(body['start_time'])
        end_time = "End time: " + str(body['end_time'])
        intro_description = body['intro_description']
        event_url = body['event_url']
        information_description = "\n".join([event_type, location, start_time, end_time])

        # This data has to be sent correctly from CRM. It has to be caught from POST request "Add Events"
        try:
            event_page = EventPage.objects.create(
                title=body['title'],
                event_type=event_type,
                intro_description=intro_description,
                information_description=information_description,
                event_url=event_url,
                author_id=request.user.pk,
            )

            events_index.add_child(instance=event_page)

            event_page.save_revision().publish()
            new_event_id = event_page.pk

        except Exception as e:
            print("Error: Could NOT create Event page", e)
            return JsonResponse(status=400, message="Could NOT create Event page!")

        context = {"id": new_event_id}
        response = JsonResponse(status=200, data=context)
        return response

    else:
        return JsonResponse(status=405)


# class AdminLogo(models.Model):
#     logo = models.ImageField(upload_to='admin_logos')
#
#     def __str__(self):
#         return "Admin Logo"
#
#     class Meta:
#         verbose_name_plural = 'Admin Logos'
#
#
# class AdminLogoForm(forms.ModelForm):
#     class Meta:
#         model = AdminLogo
#         fields = ['logo']
#
# def change_admin_logo(request):
#     try:
#         logo_instance = AdminLogo.objects.first()
#     except AdminLogo.DoesNotExist:
#         logo_instance = None
#
#     if request.method == 'POST':
#         form = AdminLogoForm(request.POST, request.FILES, instance=logo_instance)
#         if form.is_valid():
#             form.save()
#             # Replace this with the URL where you want to redirect after saving the logo
#             return redirect('wagtailadmin_home')
#     else:
#         form = AdminLogoForm(instance=logo_instance)
#
#     context = {
#         'form': form
#     }
#
#     return render(request, 'wagtailadmin/change_admin_logo.html', context)
