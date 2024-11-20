from django.conf.urls.static import static
from django.urls import path, include, re_path

from core import settings
from . import views
# from home import views as home_views

# For compliance signout
# Compliance does not have a clue what home is. Doesnt know the home.urls
# Compliance acts like a seperate application
# We just needed the URLs to be only from the compliance, and it recognizes it.
# Previously

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('archive/', views.archive, name='archive'),

    path('preview/<uuid>/', views.preview, name='preview'),
    path('preview/<uuid>/embed/', views.preview_embed, name='preview_embed'),

    # Better to do backlash here in case of other parameters i.e signin?next=http%3A
    path('signin/', views.sign_in, name='sign_in'),
    path('signout/', views.sign_out, name='sign_out'),
    path('signup/', views.sign_up, name='sign_up'),
    path('dologin/', views.dologin, name='dologin'),
    # path('submission/officer/view/<int:id>/<int:old>/', views.submission_version_officer_viewer,
    #      name='submission_version_officer_viewer'),
    # path('submission/view/', views.submission_version_viewer, name='submission_version_viewer'),
    # path('view_reason/<submission_id>', views.view_reason, name='view_reason'),
    # path('compliance', views.compliance, name='compliance'),
    # path('compliance/archive', views.archive, name='compliance/archive'),
    # path('compliance/settings', views.settingss, name='compliance/settings'),
    # path('statusChange/', views.statusChange, name='statusChange'),
]
