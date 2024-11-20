from django.conf.urls.static import static
from django.urls import path, re_path, include

from wagtail.documents import urls as wagtaildocs_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from core import settings
from . import views

app_name = 'admin'

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('login', views.admin_login, name='admin_login'),
    path('tenants/', views.tenants, name='tenants'),
    path('logout', views.sign_out, name='logout'),
    path('tenants/<id>', views.tenant_for_id, name='tenants'),
    path('tenant', views.tenant, name='tenant'),

    path('admin/', views.admin, name='admin'),
    path('admin/<id>', views.update_admin, name='update-admin'),
    path('update_post_admin', views.update_post_admin, name='update_post_admin'),
    path('admins/', views.admins, name='admins'),
    path('change_admin_password/', views.change_admin_password, name='change_admin_password'),

    # start connect nylas
    path('connect_nylas/', views.connect_nylas, name='connect_nylas'),
    path('login_callback/', views.login_callback, name='login_callback'),
    # end connect nylas

    path('demo_user/', views.demo_user, name='demo_user'),
    path('demo_users/', views.demo_users, name='demo_users'),
    path('update_demo_user/<id>', views.update_demo_user, name='update_demo_user'),

    path('showcaser/', views.showcaser, name='showcaser'),
    path('showcasers/', views.showcasers, name='showcasers'),
    path('showcasedashboard/', views.showcasedashboard, name='showcasedashboard'),
    path('update_showcasher/<id>', views.update_showcasher, name='update_showcasher'),

    path('profile/', views.profile, name='profile'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('save_tenant_option/', views.save_tenant_option, name='save_tenant_option'),
    path('meetingsystem/', views.meetingsystem, name='meetingsystem'),
    path('meetingconfig/', views.meetingconfig, name='meetingconfig'),
    path('scheduler/', views.scheduler, name='scheduler'),
    path('connectcalendar/', views.connectcalendar, name='connectcalendar'),
    path('meeting/', views.meeting, name='meeting'),
    path('update_meeting_info/', views.update_meeting_info, name='update_meeting_info'),
    path('save_available_time/', views.save_available_time, name='save_available_time'),
    path('getavailabletime/', views.getavailabletime, name='getavailabletime'),

    # As Admin
    path('dashboard/<id>', views.tenant_dashboard, name='dashboard'),
    path('success', views.success, name='success'),
    path('schedulecall', views.schedulecall, name='schedulecall'),
    path('chooseschedule', views.chooseschedule, name='chooseschedule'),
    path('enterdetail', views.enterdetail, name='enterdetail'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('pending', views.pending, name='pending'),
    path('logout', views.sign_out, name='logout'),
    path('editor-list', views.editor_list, name='editor-list'),
    path('editor/cms/<slug>', views.editor, name='editor'),
    path('builder/<page_id>', views.builder, name='builder'),
    path('vvvebjs/<page_id>', views.vvvebjs, name='vvveb'),
    path('vvvebjss/save-page/<page_id>', views.save_vvveb_page, name='save_vvveb_page'),
    path('create_page', views.create_page, name='create_page'),
    path('vvvebjs_edit/<page_id>', views.vvvebjs_edit, name='vvveb_edit'),
    path('update_vvvebjss/save-page/<page_id>', views.update_save_vvveb_page, name='update_save_vvveb_page'),
    path('subitForReview/<page_id>', views.subitForReview, name='subitForReview'),
    path('submission/officer/view/<int:id>/<int:old>/', views.submission_version_officer_viewer,
         name='submission_version_officer_viewer'),
    path('submission/view/', views.submission_version_viewer, name='submission_version_viewer'),
    path('view_reason/<submission_id>', views.view_reason, name='view_reason'),
    path('compliance', views.compliance, name='compliance'),
    path('compliance/archive', views.archive, name='compliance/archive'),
    path('compliance/settings', views.settingss, name='compliance/settings'),
    path('statusChange/', views.statusChange, name='statusChange'),
    path('settingsgear/', views.settingsgear, name='settingsgear'),
    path('socialsystem', views.socialsystem, name='socialsystem'),

    # Facebook App
    path('obtain_access_token/', views.obtain_access_token, name='obtain_access_token'),
    path('callback/', views.callback, name='callback'),
    path('post_article/', views.post_article, name='post_article'),
    path('article/<id>', views.article, name='article'),

    path('website', views.website, name='website'),
    path('contacts', views.contacts, name='contacts'),
    path('groups', views.groups, name='groups'),
    path('email', views.email, name='email'),
    path('forms', views.forms, name='forms'),
    path('chat', views.chat, name='chat'),
    path('meetings', views.meetings, name='meetings'),

    # nylas test version
    path('create_event/', views.create_event, name='create_event'),
    path('read_calendars/', views.read_calendars, name='read_calendars'),
    
     # wagtail
    path('cms_auth', views.cms_auth, name='cms_auth'),
    path('cms/login/', views.a, name='a'),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    
    # Optional URL for including your own vanilla Django urls/views
    re_path(r'wagtail/', include('wagtailcms.urls')),
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'wagtail/', include(wagtail_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
