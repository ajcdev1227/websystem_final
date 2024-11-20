from django.urls import path
from .views import JitsiLinkCreateAPIView

urlpatterns = [
    path('generate_link/', JitsiLinkCreateAPIView.as_view(), name='generate_link'),
]