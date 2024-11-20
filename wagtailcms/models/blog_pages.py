from django.db import models
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel
from wagtailseo.models import SeoMixin, SeoType, TwitterCard

from ..customblocks.content_common_blocks import BlogCommonBlocks
from .theme_settings import get_current_theme


class BlogIndexPage(Page):
    parent_page_types = ["wagtailcms.HomePage"]
    subpage_types = ["wagtailcms.BlogPost"]
    template = "themes/theme_placeholder/blog_index.html"
    max_count = 1

    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_index_cover_image",
    )

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)

        blog_posts = BlogPost.objects.live().order_by("-first_published_at")

        context.update({"blog_posts": blog_posts})

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
        db_table = "blog_index_page"
        verbose_name = "Blog Index"


class BlogPost(SeoMixin, Page):
    parent_page_types = ["wagtailcms.BlogIndexPage"]
    template = "themes/theme_placeholder/blog_post.html"

    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_post_featured_image",
    )

    show_featured_image = models.BooleanField(default=True)

    intro_description = models.CharField(max_length=500, null=True, blank=True)

    content = StreamField(BlogCommonBlocks(), use_json_field=True)

    do_not_index = models.BooleanField(default=False)

    author = models.ForeignKey(
        "home.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_post_author",
    )

    content_panels = Page.content_panels + [
        FieldPanel("featured_image"),
        FieldPanel("show_featured_image"),
        FieldPanel("intro_description"),
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
        context = super(BlogPost, self).get_context(request, *args, **kwargs)

        latest_blog_posts = BlogPost.objects.exclude(id=self.pk).order_by(
            "-first_published_at"
        )[:3]
        context["latest_blog_posts"] = latest_blog_posts

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
        db_table = "blog_post"
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
