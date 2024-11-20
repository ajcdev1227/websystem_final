from django.db import models
from django.utils import timezone
from wagtail.admin.panels import MultiFieldPanel, FieldPanel
from wagtail.fields import StreamField, RichTextField
from wagtail.models import Page
from wagtailseo.models import SeoMixin, SeoType, TwitterCard
from wagtailstreamforms.blocks import WagtailFormBlock

from ..customblocks.content_common_blocks import EventPageBlocks
from ..customblocks.richtext_features import ALL_RICHTEXT_FEATURES
from .theme_settings import get_current_theme

EVENT_TYPES = [
    ("webinar", "Webinar"),
    ("seminar", "Seminar"),
]


class EventsIndexPage(Page):
    parent_page_types = ["wagtailcms.HomePage"]
    subpage_types = ["wagtailcms.EventPage"]
    template = "themes/theme_placeholder/events_index.html"
    max_count = 1

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="events_index_cover_image",
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(EventsIndexPage, self).get_context(request, *args, **kwargs)

        current_time = timezone.now()

        past_events = EventPage.objects.filter(end_date__lte=current_time).live().order_by("-first_published_at")

        upcoming_events = EventPage.objects.filter(end_date__gte=current_time).live().order_by("-first_published_at")

        context.update(
            {
                "past_events": past_events,
                "upcoming_events": upcoming_events,
            }
        )

        return context

    def get_template(self, request, *args, **kwargs):
        selected_theme = get_current_theme(request)
        page_template = self.template
        page_template = str(page_template).replace("theme_placeholder", selected_theme)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.ajax_template or page_template
        else:
            return page_template

    class Meta:
        db_table = "events_index_page"
        verbose_name = "Events Index"


class EventPage(SeoMixin, Page):
    parent_page_types = ["wagtailcms.EventsIndexPage"]
    template = "themes/theme_placeholder/event_page.html"

    event_type = models.CharField(max_length=255, choices=EVENT_TYPES, null=False, blank=False)

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="event_featured_image",
    )

    show_featured_image = models.BooleanField(default=True)

    start_date = models.DateTimeField(null=True)

    end_date = models.DateTimeField(null=True)

    intro_description = RichTextField(features=ALL_RICHTEXT_FEATURES, null=True, blank=True)

    information_description = RichTextField(features=ALL_RICHTEXT_FEATURES, null=True, blank=True)

    event_url = models.URLField(null=True, blank=True)

    # added event_id
    event_id = models.IntegerField(null=True, blank=False)

    register_form = StreamField(
        [("form", WagtailFormBlock())],
        use_json_field=True,
        null=True,
        blank=True,
        max_num=1,
    )

    content = StreamField(EventPageBlocks(), use_json_field=True, null=True, blank=True)

    show_register_button = models.BooleanField(default=True)

    do_not_index = models.BooleanField(default=False)

    author = models.ForeignKey(
        "home.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_page_author",
    )

    content_panels = Page.content_panels + [
        FieldPanel("event_id"),
        FieldPanel("event_type"),
        MultiFieldPanel(
            [
                FieldPanel("featured_image"),
                FieldPanel("show_featured_image"),
            ], heading="Featured Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("start_date"),
                FieldPanel("end_date"),
            ], heading="Event Dates"
        ),
        FieldPanel("show_register_button"),
        FieldPanel("intro_description"),
        FieldPanel("information_description"),
        FieldPanel("event_url"),
        FieldPanel("register_form"),
        FieldPanel("content"),
    ]

    promote_panels = SeoMixin.seo_meta_panels + [
        FieldPanel("do_not_index"),
    ]

    seo_content_type = SeoType.ARTICLE
    seo_twitter_card = TwitterCard.LARGE

    seo_description_sources = [
        "search_description",
        "intro_description",
    ]

    seo_image_sources = [
        "og_image",
        "featured_image",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            author = kwargs["owner"]
        except (AttributeError, KeyError):
            pass
        else:
            self.author = author

    def get_context(self, request, *args, **kwargs):
        context = super(EventPage, self).get_context(request, *args, **kwargs)

        current_time = timezone.now()

        latest_posts = EventPage.objects.exclude(id=self.pk).order_by(
            "-first_published_at"
        )[:3]
        context["latest_posts"] = latest_posts

        context["upcoming_event"] = self.end_date > current_time if self.end_date else False

        return context

    def get_template(self, request, *args, **kwargs):
        selected_theme = get_current_theme(request)
        page_template = self.template
        page_template = str(page_template).replace("theme_placeholder", selected_theme)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.ajax_template or page_template
        else:
            return page_template

    class Meta:
        db_table = "event_pages"
        verbose_name = "Event Page"
        verbose_name_plural = "Event Pages"
