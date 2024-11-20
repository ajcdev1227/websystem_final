from django.conf.urls.static import static
from django.urls import path, include, re_path

from core import settings
from . import views
from virtual_calendar import urls as calendar_urls

from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dologin', views.dologin, name='dologin'),
    path('docmslogin', views.docmslogin, name='docmslogin'),
    path('signin', views.sign_in, name='sign_in'),
    path('signup', views.sign_up, name='sign_up'),
    path('success', views.success, name='success'),
    path('nylas_auth', views.nylas_auth, name='nylas_auth'),
    path('login_callback', views.login_callback, name='login_callback'),
    path('schedulecall', views.schedulecall, name='schedulecall'),
    path('chooseschedule', views.chooseschedule, name='chooseschedule'),
    path('meetingwait', views.meetingwait, name='meetingwait'),
    path('meeting/<meeting_link>', views.meeting, name='meeting'),
    path('enterdetail', views.enterdetail, name='enterdetail'),
    path('confirmed', views.confirmed, name='confirmed'),
    path('schedulemeeting', views.schedulemeeting, name='schedulemeeting'),
    path('getavailabletime', views.getavailabletime, name='getavailabletime'),
    path('pending', views.pending, name='pending'),
    path('logout', views.sign_out, name='logout'),
    path('editor-list', views.editor_list, name='editor-list'),
    path('getpagelist', views.getpagelist, name='getpagelist'),
    path('updatepath', views.updatepath, name='updatepath'),
    path('remove_page', views.remove_page, name='remove_page'),
    path('temppage', views.temppage, name='temppage'),

    path('editor/cms/<slug>', views.editor, name='editor'),
    path('builder/<page_id>', views.builder, name='builder'),
    path('page/<slug>', views.page, name='page'),

    path('vvvebjs/<page_id>', views.vvvebjs, name='vvveb'),
    path('vvvebjs_edit/<page_id>', views.vvvebjs_edit, name='vvveb_edit'),

    path('vvvebjss/save-page/<page_id>', views.save_vvveb_page, name='save_vvveb_page'),
    path('create_page', views.create_page, name='create_page'),
    path('update_vvvebjss/save-page/<page_id>', views.update_save_vvveb_page, name='update_save_vvveb_page'),
    path('subitForReview/<page_id>', views.subitForReview, name='subitForReview'),
    path('submission/officer/view/<int:id>/<int:old>/', views.submission_version_officer_viewer,
         name='submission_version_officer_viewer'),
    path('submission/view/', views.submission_version_viewer, name='submission_version_viewer'),
    path('view_reason/<submission_id>', views.view_reason, name='view_reason'),


    # This is older compliance
    #
    # If compliance.fod, home.fod etc did not exist, this compliance would cause a issue
    # mixing an issue with compliance.urls, so it would not know where to go.
    path('compliance', views.compliance, name='compliance'),
    path('compliance/archive', views.archive, name='compliance/archive'),
    path('compliance/settings', views.settingss, name='compliance/settings'),
    path('statusChange/', views.statusChange, name='statusChange'),

    # Link generation API
    path('api/', include('link_api.urls')),  # include jitsi link generation

    # Facebook App
    path('obtain_access_token/', views.obtain_access_token, name='obtain_access_token'),
    path('callback/', views.callback, name='callback'),
    path('post_article/', views.post_article, name='post_article'),
    path('article/<id>', views.article, name='article'),

    path('groups', views.groups, name='groups'),
    path('email', views.email, name='email'),
    path('forms', views.forms, name='forms'),
    path('chat', views.chat, name='chat'),
    path('calendar/', views.calendar_view, name='calendar'),

    path('tv/', views.tv, name='tv'),

    # nylas webhook
    path('nylas_webhook', views.nylas_webhook, name='nylas_webhook'),

    # wagtail
    path('cms_auth', views.cms_auth, name='cms_auth'),
    path('cms/login/', views.a, name='a'),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('api/v1/tenant/', include('wagtailcms.urls')),
    # Optional URL for including your own vanilla Django urls/views
    # re_path(r'site/', include('wagtailcms.urls')), # this is index
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's serving mechanism
    re_path(r'site/', include(wagtail_urls)),


    # green design paths # is not implemented yet.

    # below paths are implemented already
    path('contacts', views.contacts, name='contacts'),
    path('website', views.website, name='website'),
    path('socialsystem', views.socialsystem, name='socialsystem'),
    path('settingsgear/', views.settingsgear, name='settingsgear'),

    # below paths are not implemented yet.
    path('ai-tool', views.ai_tool, name='ai_tool'), #
    path('automations', views.automations, name='automations'), #

    # meetings start
    path("meetings/", include(calendar_urls)),
    # path('meetings/bookings/',include(calendar_urls)),
    # path('meetings', views.meetings, name='meetings'),

    # path('mypage/<str:unique_identifier>/', views.user_booking_page, name='booking_page'),

    # path('meetings/create', views.meetings_create, name='meetings_create'),
    # path('meetings/create/personal', views.instant_meeting_create, name='meetings/personal'),
    # path('meetings/create/consultations', views.instant_meeting_create, name='meetings/consultations'),
    path('meetings/create/instant/', views.instant_meeting_create, name='meetings/instant'),
    # path('meetings/view-public-page/', views.view_public_meeting_change, name='view_public_meeting_page'),
    path('meeting/<str:id>/', views.instant_meeting_viewer, name='instant_meeting_viewer'),
    # path('meetings/schedular', views.instant_meeting_create, name='meetings/schedular'),
    # meetings end

    path('compaign-builder', views.compaign_builder, name='compaign_builder'),#
    path('events', views.events, name='events'), #
    path('help-docs', views.help_docs, name='help_docs'),
    path('customer-support', views.customer_support, name='customer_support'), #
    path('video-walkthroughs', views.video_walkthroughs, name='video_walkthroughs'), #
    path('social-management', views.social_management, name='social_management'), #

    # meeting creation/ toggle visibility
    # path('create-meeting/',views.create_meeting,name='create_meeting'),
    # path('visible-meetings/',views.visible_meetings, name='visible_meetings'),
    # path('toggle-visibility/<int:meeting_id>/', views.toggle_meeting_visibility, name='toggle_meeting_visibility'),
    # path('current_meetings/', views.current_meetings, name='current_meetings'),
    # path('past_meetings/', views.past_meetings, name='past_meetings'),
    # path('future_meetings/', views.future_meetings, name='future_meetings'),
    # path('meetings/create/', views.instant_meeting_create, name='instant_meeting'),
    # path('calendar1/',views.booking_calendar, name='booking_calendar'),
]

handler404 = "home.views.handler404"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
