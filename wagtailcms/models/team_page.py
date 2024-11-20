from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from ..customblocks.base_stream_blocks import BaseStreamBlock
from .theme_settings import get_current_theme


class TeamPage(Page):
    template = 'themes/theme_placeholder/team_page.html'

    body = StreamField(BaseStreamBlock(), verbose_name="Page Body", blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]

    def get_template(self, request, *args, **kwargs):
        selected_theme = get_current_theme(request)
        page_template = self.template
        page_template = str(page_template).replace("theme_placeholder", selected_theme)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return self.ajax_template or page_template
        else:
            return page_template


'''
TeamPag
Objects : Tp1 --> Body 

TeamPage --> Bodyteam_page.html

HomePage 
About
Service
Contact
Team
Locations
Event Type Page (From the CRM) dont worry about details of this page yet, just make the model for it.
'''