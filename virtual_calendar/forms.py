from django import forms
from .models import (
    CalendarProfile,
    EventType,
    Booking,
    Availability,
    AvailabilityTimeSlot,
)


class CalendarProfileForm(forms.ModelForm):
    class Meta:
        model = CalendarProfile
        fields = ["title", "url", "email", "about", "timezone"]


class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = ["title", "url", "duration", "meeting_type", "description"]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "event_type",
            "time_slot_start",
            "time_slot_end",
            "name",
            "email_address",
            "additional_note",
        ]


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = [
            "profile",
            "start_date",
            "end_date",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]


class AvailabilityTimeSlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilityTimeSlot
        fields = ["availability", "day_of_week", "start_time", "end_time"]
