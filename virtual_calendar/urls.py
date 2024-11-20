from django.urls import path
import home.views
# from .views import CalendarProfileView, EventTypeView, BookingsView, AvailabilityView, AvailabilityTimeSlotView

urlpatterns = [

    # meeting test
    path('', home.views.meetings, name='meetings'),
    path('type/<str:slug>/', home.views.meeting_details, name='meeting_details'),
    path('bookings/', home.views.meeting_bookings, name='meetings_bookings'),
    path('availability/', home.views.meeting_availability, name='meeting_availability'),

    # API
    path('api/event-type', home.views.create_new_event_type, name='create-event-type'),
    #
    # path('calendar-profile/', CalendarProfileView.as_view(), name='calendar_profile'),
    # path('event-types/', EventTypeView.as_view(), name='event_types'),
    # path('event-types/<int:pk>/', EventTypeView.as_view(), name='event_type_details'),
    # path("bookings/", BookingsView.as_view(), name="booking_view"),
    # path('bookings/<str:status>/', BookingsView.as_view(), name='bookings_list_filtered'),
    # path('bookings/<int:pk>/', BookingsView.as_view(), name='booking_details'),
    # path('availability/', AvailabilityView.as_view(), name='availability_view'),
    # path('availability/<int:pk>/', AvailabilityView.as_view(), name='availability_details'),
    # path('availability-slots/', AvailabilityTimeSlotView.as_view(), name='availability_slots'),
    # path('availability-slots/<int:pk>/', AvailabilityTimeSlotView.as_view(), name='availability_slot_details'),
    #
    # # settings
    # path('settings/profile/', CalendarProfileView.as_view(), name='calendar_profile')
]
