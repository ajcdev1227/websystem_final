# from django.db import models
# from django import forms
#
# from wagtail.models import Page
# from wagtail.admin.panels import FieldPanel
# from wagtail.fields import StreamField
#
# from wagtail.admin.panels import (
#     FieldPanel,
#     FieldRowPanel,
#     MultiFieldPanel
# )
# from wagtail.fields import RichTextField
#
# from ..customblocks.BaseStreamBlocks import BaseStreamBlock
# from .blocks import *


# Create your models here.
# class HomePage(Page):
#     bg_image = models.ForeignKey(
#         'wagtailimages.Image',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='+',
#     )
#
#     sub_title = models.CharField(max_length=255, blank=True)
#
#     description = models.TextField(blank=True)
#
#     intro = RichTextField(blank=True)
#     intro_position = models.CharField(
#         max_length=6,
#         choices=TWO_POSITION_CHOICES,
#         default='right',
#         help_text='Select the position for the intro field.',
#         blank=True,
#     )
#
#     sub_intro = models.CharField(max_length=255, blank=True)
#
#     talk_button_position = models.CharField(
#         max_length=6,
#         choices=THREE_POSITION_CHOICES,
#         default='center',
#         help_text='Select the position for the Talk button.',
#         blank=True,
#     )
#
#     # services group start
#     services_heading = models.CharField(max_length=255, blank=True)
#     services_heading_sub = models.CharField(max_length=255, blank=True)
#     services_description = models.TextField(blank=True)
#     services_grid_card = StreamField(
#         ServiceGridBlock(),  verbose_name='Grid Card', blank=True, use_json_field=True
#     )
#
#     grid_card_column_count = models.CharField(
#         max_length=6,
#         choices=COLUMN_CHOICES,
#         default="3",
#         help_text="Select the number of columns for the grid (2-4).",
#         blank=True,
#     )
#     services_expend_button = StreamField(
#         ExpendButtonBlock(), verbose_name='Expend Button', blank=True, use_json_field=True
#     )
#
#     section = StreamField(
#         BaseStreamBlock(), verbose_name='Sections', blank=True, use_json_field=True
#     )
#
#     form = StreamField(
#         FormBlock(), verbose_name='form', blank=True, use_json_field=True
#     )
#
#     thank_you_text = RichTextField(blank=True)
#
#     content_panels = Page.content_panels + [
#         FieldPanel('bg_image'),
#         FieldPanel(
#             'sub_title',
#             classname='custom-field-panel custom-sub-title-panel',
#             widget=forms.Textarea(attrs={'rows': 1}),
#         ),
#         FieldPanel(
#             'description',
#             classname='custom-field-panel custom-description-panel',
#             widget=forms.Textarea(attrs={'rows': 3}),
#         ),
#         FieldRowPanel(
#             [
#                 FieldPanel(
#                     'intro',
#                     classname='custom-field-panel custom-intro-panel',
#                     widget=forms.Textarea(attrs={'rows': 3}),
#                 ),
#                 FieldPanel(
#                     'intro_position',
#                     classname='custom-field-panel custom-intro-position',
#                 ),
#             ]
#         ),
#         FieldPanel(
#             'sub_intro',
#             classname='custom-field-panel custom-sub-intro-panel',
#             widget=forms.Textarea(attrs={'rows': 2}),
#         ),
#         FieldPanel(
#             'talk_button_position', classname='custom-field-panel custom-intro-position'
#         ),
#         MultiFieldPanel([
#             FieldPanel('services_heading'),
#             FieldPanel('services_heading_sub'),
#             FieldPanel('services_description', widget=forms.Textarea(attrs={'rows': 3})),
#             FieldRowPanel([
#                 FieldPanel('services_grid_card'),
#                 FieldPanel('grid_card_column_count')
#             ]),
#             FieldPanel('services_expend_button'),
#         ], heading='Services'),
#         FieldPanel('section'),
#         FieldPanel('form'),
#         FieldPanel(
#             'thank_you_text',
#             classname='custom-field-panel custom-thank-you-panel',
#             widget=forms.Textarea(attrs={'rows': 6}),
#         ),
#     ]

