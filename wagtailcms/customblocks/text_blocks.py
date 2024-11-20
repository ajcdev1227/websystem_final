from wagtail.blocks import (
    CharBlock,
    RichTextBlock,
    StructBlock,
    TextBlock,
    URLBlock,
    IntegerBlock,
)
from django.core.validators import MaxValueValidator, MinValueValidator


class SpacingBlock(StructBlock):
    lines = IntegerBlock(
        null=False,
        blank=False,
        default=1,
        validators=[MaxValueValidator(25), MinValueValidator(1)],
    )

    class Meta:
        icon = "arrows-up-down"
        template = "blocks/textblocks/spacing_block.html"


class ParagraphBlock(StructBlock):
    paragraph = TextBlock()
    attribute_name = CharBlock(blank=True, required=False, label="e.g. Mary Berry")
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = "openquote"
        template = "blocks/textblocks/paragraph_block.html"


class HeadingBlock(StructBlock):
    """
    Custom `StructBlock` that allows the user to select h2 - h4 sizes for headers
    """

    heading_text = CharBlock(classname="title", required=True)
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        icon = "Title"
        template = "blocks/textblocks/heading_block.html"


class ButtonBlock(StructBlock):
    button_text = CharBlock(required=True, max_length=50, label='Button Text')
    button_link = URLBlock(required=True, label='Button Link')
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        label = 'Button block'
        template = "blocks/textblocks/button.html"


class TextWithHeading(StructBlock):
    heading = CharBlock(classname="title", required=True)
    paragraph = TextBlock(required=True, max_length=500, label='Paragraph')
    
    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        label = 'Text With Heading block'
        template = "blocks/textblocks/text_with_heading.html"


class RichTextEditorBlock(RichTextBlock):

    top_margin = CharBlock(required=False, help_text="Top margin in pixels or percentage")
    right_margin = CharBlock(required=False, help_text="Right margin in pixels or percentage")
    bottom_margin = CharBlock(required=False, help_text="Bottom margin in pixels or percentage")
    left_margin = CharBlock(required=False, help_text="Left margin in pixels or percentage")

    class Meta:
        template = "blocks/textblocks/richtextblock.html"
        icon = 'doc-full-inverse'
        label = 'Rich Text'
