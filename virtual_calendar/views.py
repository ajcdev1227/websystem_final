# from django.contrib.auth.decorators import login_required
# from django.core.serializers import serialize
# from django.http import JsonResponse
# from django.utils import timezone
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.views.generic import View
# from django.core.handlers.wsgi import WSGIRequest
#
# from .models import CalendarProfile, EventType, Booking, Availability, AvailabilityTimeSlot
# from .forms import CalendarProfileForm, EventTypeForm, BookingForm, AvailabilityForm, AvailabilityTimeSlotForm
#
#
# @login_required()
# @method_decorator(csrf_exempt, name="dispatch")
# class CalendarProfileView(View):
#     def post(self, request: WSGIRequest, *args, **kwargs):
#         # Check if the user already has a profile
#         if CalendarProfile.objects.filter(user_id=request.user.id).exists():
#             return JsonResponse({"error": "Calendar Profile already exists"}, status=400)
#
#         form = CalendarProfileForm(request.POST)
#         if form.is_valid():
#             calendar_profile = form.save(commit=False)
#             calendar_profile.created_ts = timezone.now()
#             calendar_profile.save()
#             return JsonResponse({"success": True, "id": calendar_profile.id})
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#
#     def put(self, request, *args, **kwargs):
#         try:
#             calendar_profile = CalendarProfile.objects.get(user=request.user)
#             form = CalendarProfileForm(request.POST, instance=calendar_profile)
#             if form.is_valid():
#                 calendar_profile = form.save()
#                 return JsonResponse({"success": True, "id": calendar_profile.id})
#             else:
#                 return JsonResponse({"error": form.errors}, status=400)
#         except CalendarProfile.DoesNotExist:
#             return JsonResponse({"error": "Could NOT find Calendar Profile!"}, status=404)
#
#     def get(self, request, *args, **kwargs):
#         try:
#             calendar_profile = CalendarProfile.objects.get(user=request.user)
#             data = {
#                 "title": calendar_profile.title,
#                 "url": calendar_profile.url,
#                 "email": calendar_profile.email,
#                 "about": calendar_profile.about,
#                 "timezone": calendar_profile.timezone_id,
#             }
#             return JsonResponse(data)
#         except CalendarProfile.DoesNotExist:
#             return JsonResponse({"error": "Could NOT find Calendar Profile!"}, status=404)
#
#
# @login_required()
# @method_decorator(csrf_exempt, name="dispatch")
# class EventTypeView(View):
#     def post(self, request, *args, **kwargs):
#         form = EventTypeForm(request.POST)
#         try:
#             cal_profile = CalendarProfile.objects.get(user=request.user)
#         except (CalendarProfile.DoesNotExist, CalendarProfile.MultipleObjectsReturned):
#             error = "Error getting the profile of user!"
#             print(error)
#             return JsonResponse({"error": error}, status=400)
#
#         if form.is_valid():
#             event_type = form.save(commit=False)
#             event_type.profile = cal_profile
#             event_type.created_ts = timezone.now()
#             event_type.save()
#             return JsonResponse({"success": True, "id": event_type.id})
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#
#     def put(self, request, pk, *args, **kwargs):
#         try:
#             event_type_obj = EventType.objects.get(pk=pk)
#             form = EventTypeForm(request.POST, instance=event_type_obj)
#             if form.is_valid():
#                 event_type = form.save()
#                 return JsonResponse({"success": True, "id": event_type.id})
#             else:
#                 return JsonResponse({"error": form.errors}, status=400)
#         except EventType.DoesNotExist:
#             return JsonResponse({"error": "Could NOT find Event Type!"}, status=404)
#
#     def get(self, request, pk=None, *args, **kwargs):
#         if pk:
#             try:
#                 event_type = EventType.objects.get(pk=pk)
#                 data = {
#                     "title": event_type.title,
#                     "url": event_type.url,
#                     "duration": event_type.duration,
#                     "meeting_type": event_type.meeting_type,
#                     "description": event_type.description,
#                 }
#                 return JsonResponse(data)
#             except CalendarProfile.DoesNotExist:
#                 return JsonResponse({"error": "Could NOT find Event Type!"}, status=404)
#
#         else:
#             try:
#                 cal_profile = CalendarProfile.objects.get(user=request.user)
#                 event_types = EventType.objects.filter(profile=cal_profile)
#                 data = serialize("json", event_types)
#                 return JsonResponse(data, safe=False)
#             except (CalendarProfile.DoesNotExist, Exception):
#                 error = "Could NOT get the Event Type!"
#                 print(error)
#                 return JsonResponse({"error", error}, status=400)
#
#
# @login_required()
# @method_decorator(csrf_exempt, name="dispatch")
# class BookingsView(View):
#     def post(self, request, *args, **kwargs):
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.created_ts = timezone.now()
#             booking.save()
#             return JsonResponse({"success": True, "id": booking.id})
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#
#     def get(self, request, pk=None, status=None, *args, **kwargs):
#         if pk:
#             try:
#                 booking = Booking.objects.get(pk=pk)
#                 data = serialize("json", [booking])
#                 return JsonResponse(data, safe=False)
#
#             except (Booking.DoesNotExist, Exception):
#                 error = "Could NOT get the Booking!"
#                 print(error)
#                 return JsonResponse({"error": error}, status=404)
#
#         else:
#             try:
#                 calendar_profile = CalendarProfile.objects.get(user=request.user)
#                 event_type_ids = EventType.objects.filter(
#                     profile=calendar_profile
#                 ).values_list("pk")
#                 bookings = Booking.objects.filter(
#                     event_type__id__in=event_type_ids, status=status
#                 )
#                 data = serialize("json", bookings)
#                 return JsonResponse(data, safe=False)
#             except (CalendarProfile.DoesNotExist, Exception):
#                 error = "Could NOT get the list of Bookings from Profile/Event"
#                 print(error)
#                 return JsonResponse({"error": error}, status=404)
#
#
# @login_required()
# @method_decorator(csrf_exempt, name="dispatch")
# class AvailabilityView(View):
#     def post(self, request, *args, **kwargs):
#         form = AvailabilityForm(request.POST)
#         if form.is_valid():
#             profile_id = request.POST.get('profile_id')
#             profile = CalendarProfile.objects.get(pk=profile_id)
#             availability = form.save(commit=False)
#             availability.profile = profile
#             availability.save()
#             return JsonResponse({"success": True, "id": availability.id})
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#
#     def get(self, request, pk=None, *args, **kwargs):
#         if pk:
#             try:
#                 availability = Availability.objects.get(pk=pk)
#                 data = serialize("json", [availability])
#                 return JsonResponse(data, safe=False)
#             except Availability.DoesNotExist:
#                 error = "Availability not found!"
#                 print(error)
#                 return JsonResponse({"error": error}, status=404)
#         else:
#             try:
#                 cal_profile = CalendarProfile.objects.get(user=request.user)
#                 availability = Availability.objects.filter(profile=cal_profile)
#                 data = serialize("json", availability)
#                 return JsonResponse(data, safe=False)
#             except (CalendarProfile.DoesNotExist, Exception):
#                 error = "Could NOT get the Availabilities list!"
#                 print(error)
#                 return JsonResponse({"error": error}, status=400)
#
#
# @login_required()
# @method_decorator(csrf_exempt, name="dispatch")
# class AvailabilityTimeSlotView(View):
#     def post(self, request, *args, **kwargs):
#         form = AvailabilityTimeSlotForm(request.POST)
#         if form.is_valid():
#             availability_id = request.POST.get('availability_id')
#             availability = Availability.objects.get(pk=availability_id)
#             time_slot = form.save(commit=False)
#             time_slot.availability = availability
#             time_slot.save()
#             return JsonResponse({"success": True, "id": time_slot.id})
#         else:
#             return JsonResponse({"error": form.errors}, status=400)
#
#     def get(self, request, pk=None, *args, **kwargs):
#         if pk:
#             try:
#                 time_slot = AvailabilityTimeSlot.objects.get(pk=pk)
#                 data = serialize("json", [time_slot])
#                 return JsonResponse(data, safe=False)
#             except AvailabilityTimeSlot.DoesNotExist:
#                 error = "Could NOT get Availability Time Slot!"
#                 print(error)
#                 return JsonResponse({"error": error}, status=404)
