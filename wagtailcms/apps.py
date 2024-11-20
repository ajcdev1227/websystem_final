from django.apps import AppConfig
from wagtail.signals import page_published, workflow_approved


class WagtailcmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagtailcms'

    def ready(self):
        from wagtailcms.signals import handle_page_published
        page_published.connect(handle_page_published, sender=None)
        import wagtailcms.signals
