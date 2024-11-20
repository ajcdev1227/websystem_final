from django.db import models
from django.utils.timezone import now
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from ..customblocks.richtext_features import ALL_RICHTEXT_FEATURES
from .theme_settings import get_current_theme


class PrivacyPolicyPage(Page):
    template = 'themes/theme_placeholder/privacy_policy.html'
    max_count = 1

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="privacy_policy_cover_image",
    )

    content = RichTextField(features=ALL_RICHTEXT_FEATURES, null=True, blank=True)

    updated_at = models.DateTimeField(default=now, blank=True)

    panels = [
        FieldPanel("cover_image"),
        FieldPanel("content"),
    ]

    def get_template(self, request, *args, **kwargs):
        selected_theme = get_current_theme(request)
        page_template = self.template
        page_template = str(page_template).replace("theme_placeholder", selected_theme)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.ajax_template or page_template
        else:
            return page_template
