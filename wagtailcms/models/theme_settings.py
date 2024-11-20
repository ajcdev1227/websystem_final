from django import forms
from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.fields import StreamField
from wagtail.blocks import RawHTMLBlock

from wagtail_color_panel.fields import ColorField


@register_setting(icon="site")
class ThemeSettings(BaseGenericSetting):
    selected_theme = models.CharField(
        max_length=255,
        choices=[
            ('theme1', 'Theme 1'),
            ('theme2', 'Theme 2'),
            ('theme3', 'Theme 3'),
        ],
        default='theme1',
    )

    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    headline_font = models.CharField(
        max_length=255,
        choices=[
            ('Arial', 'Arial'),
            ('Helvetica', 'Helvetica'),
            ('Times New Roman', 'Times New Roman'),
            ('Georgia', 'Georgia'),
            ('Verdana', 'Verdana'),
            ('Roboto', 'Roboto'),
            ('Open Sans', 'Open Sans'),
            ('Lato', 'Lato'),
            ('Roboto Slab', 'Roboto Slab'),
            ('Cabin', 'Cabin'),
        ],
        default='',
    )

    headline_size = models.CharField(
        max_length=255,
        choices=[
            ('14px', 'Small'),
            ('18px', 'Medium'),
            ('22px', 'Large'),
        ],
        default='',
    )

    paragraph_font = models.CharField(
        max_length=255,
        choices=[
            ('Arial', 'Arial'),
            ('Helvetica', 'Helvetica'),
            ('Times New Roman', 'Times New Roman'),
            ('Georgia', 'Georgia'),
            ('Verdana', 'Verdana'),
            ('Roboto', 'Roboto'),
            ('Open Sans', 'Open Sans'),
            ('Lato', 'Lato'),
            ('Roboto Slab', 'Roboto Slab'),
            ('Cabin', 'Cabin'),
        ],
        default='',
    )

    paragraph_size = models.CharField(
        max_length=255,
        choices=[
            ('12px', 'Small'),
            ('14px', 'Medium'),
            ('18px', 'Large'),
        ],
        default='',
    )

    global_style_and_scripts_head = StreamField(
        [("raw_html", RawHTMLBlock(required=True))],
        use_json_field=True,
        null=True,
        blank=True,
        help_text="Don't forget to use <style></style> or <script></script> tags"
    )

    global_style_and_scripts_end = StreamField(
        [("raw_html", RawHTMLBlock(required=True))],
        use_json_field=True,
        null=True,
        blank=True,
        help_text="Don't forget to use <style></style> or <script></script> tags"
    )

    primary_color = ColorField(default="#355EFC")
    cta_color = ColorField(default="#355EFC")
    heading_color = ColorField(default="#011A41")
    paragraph_color = ColorField(default="#555555")
    footer_color = ColorField(default="#011A41")

    def get_form(self):
        class ThemeSettingsForm(forms.ModelForm):
            class Meta:
                model = ThemeSettings
                fields = [
                    "selected_theme",
                    "headline_font",
                    "headline_size",
                    "paragraph_font",
                    "paragraph_size",
                    "global_style_and_scripts_head",
                    "global_style_and_scripts_end",
                    "primary_color",
                    "cta_color",
                    "heading_color",
                    "paragraph_color",
                    "footer_color",
                ]
                widgets = {
                    "selected_theme": forms.Select(
                        attrs={"class": "customized-input-field"}
                    ),
                    "headline_font": forms.Select(
                        attrs={"class": "customized-input-field"}
                    ),
                    "headline_size": forms.Select(
                        attrs={"class": "customized-input-field"}
                    ),
                    "paragraph_font": forms.Select(
                        attrs={"class": "customized-input-field"}
                    ),
                    "paragraph_size": forms.Select(
                        attrs={"class": "customized-input-field"}
                    ),
                    "primary_color": forms.TextInput(
                        attrs={"type": "color", "class": "customized-color-field"}
                    ),
                    "cta_color": forms.TextInput(
                        attrs={"type": "color", "class": "customized-color-field"}
                    ),
                    "heading_color": forms.TextInput(
                        attrs={"type": "color", "class": "customized-color-field"}
                    ),
                    "paragraph_color": forms.TextInput(
                        attrs={"type": "color", "class": "customized-color-field"}
                    ),
                    "footer_color": forms.TextInput(
                        attrs={"type": "color", "class": "customized-color-field"}
                    ),
                }

        return ThemeSettingsForm


def get_current_theme(request):
    theme_settings = ThemeSettings.load(request_or_site=request)
    return theme_settings.selected_theme
