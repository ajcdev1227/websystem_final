from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


@register_setting(icon="site")
class WebsiteSettings(BaseGenericSetting):
    navbar_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    display_email = models.EmailField(null=False, blank=False)
    display_phone = models.CharField(max_length=50, null=False, blank=False)
    display_address = models.CharField(max_length=200, null=True, blank=True)
    working_hours = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="For example: 9.00 am - 9.00 pm",
    )

    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)

    footer_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    footer_copyright = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="For example: © Site, All Right Reserved.",
    )
    footer_developer = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="For example: Developed by:",
    )
    google_analytics_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )
    ms_clarity_key = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel("navbar_logo"),
        MultiFieldPanel(
            [
                FieldPanel("display_email"),
                FieldPanel("display_phone"),
                FieldPanel("display_address"),
                FieldPanel("working_hours"),
            ],
            heading="Contact Info",
        ),
        MultiFieldPanel(
            [
                FieldPanel("facebook"),
                FieldPanel("twitter"),
                FieldPanel("instagram"),
                FieldPanel("linkedin"),
                FieldPanel("youtube"),
                FieldPanel("github"),
            ],
            heading="Social Media",
        ),
        MultiFieldPanel(
            [
                FieldPanel("footer_logo"),
                FieldPanel("footer_copyright"),
                FieldPanel("footer_developer"),
            ],
            heading="Footer Info",
        ),
        MultiFieldPanel(
            [
                FieldPanel("google_analytics_key"),
                FieldPanel("ms_clarity_key"),
            ],
            heading="Tracking Keys",
        ),
    ]

    class Meta:
        verbose_name = "Website Settings"
