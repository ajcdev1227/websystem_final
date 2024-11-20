from django.conf.urls.static import static
from django.urls import path

from core import settings
from . import views

app_name = 'webauth'
urlpatterns = [
    path('signin', views.sign_in, name='sign_in'),
    path('signout', views.sign_out, name='sign_out'),
    path('signup', views.sign_up, name='sign_up'),
    path('email_validation', views.email_validation, name='email_validation'),
]

handler404 = 'webauth.views.sign_in'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
