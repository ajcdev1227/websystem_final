# from django.contrib import admin
# from django.urls import path, include, re_path
# from .views import change_admin_logo
#
from django.urls import path
from wagtailcms import views

# /api/v1/tenant/
urlpatterns = [
    # path('change-logo', change_admin_logo, name='change_admin_logo'),
    path("<int:customer_id>/events/", views.create_event_page, name="create_event_page")
]
