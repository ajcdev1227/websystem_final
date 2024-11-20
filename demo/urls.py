from django.conf.urls.static import static
from django.urls import path

from core import settings
from . import views

app_name = 'demo'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signin', views.sign_in, name='sign_in'),

    path('success', views.success, name='success'),
    path('schedulecall', views.schedulecall, name='schedulecall'),
    path('chooseschedule', views.chooseschedule, name='chooseschedule'),
    path('meetingwait', views.meetingwait, name='meetingwait'),
    path('meeting/<meeting_link>', views.meeting, name='meeting'),
    path('enterdetail', views.enterdetail, name='enterdetail'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('schedulemeeting', views.schedulemeeting, name='schedulemeeting'),
    path('getavailabletime', views.getavailabletime, name='getavailabletime'),

    path('email_validation', views.email_validation, name='email_validation'),
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
    path('calendar/', views.calendar_view, name='calendar'),



    path('welcome/', views.welcome, name='welcome'),
    path('appointment/', views.appointment, name='appointment'),
    path('getavailabletime', views.getavailabletime, name='getavailabletime'),
    path('enterdetail', views.enterdetail, name='enterdetail'),
    path('confirmed', views.confirmed, name='confirmed'),
]

handler404 = "demo.views.handler404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
