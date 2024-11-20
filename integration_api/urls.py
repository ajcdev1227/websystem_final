from django.urls import path

from .views import Events

urlpatterns = [
    path('api/v1/tenant/<str:customer_id>/events', Events.as_view(), name='api_events'),
]
