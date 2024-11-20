from wagtail import blocks
from ..customblocks.boxes_blocks import *
from ..customblocks.text_blocks import *
from ..customblocks.image_blocks import *

THREE_POSITION_CHOICES = [
    ("left", "Left"),
    ("center", "Center"),
    ("right", "Right"),
]

TWO_POSITION_CHOICES = [
    ("left", "Left"),
    ("right", "Right"),
]


COLUMN_CHOICES = [
    ("2", "2 columns"),
    ("3", "3 columns"),
    ("4", "4 columns"),
]


class ExpendButtonBlock(StreamBlock):
    button_text = CharBlock(required=True, max_length=50, label='Button Text')


class ImageCardBlock(blocks.StructBlock):
    description = blocks.RichTextBlock()
    image = ImageChooserBlock()
    image_position = blocks.ChoiceBlock(
        max_length=6,
        help_text='Select the position of Image.',
    )


class GridCardBlock(blocks.StructBlock):
    icon = IconChooserBlock(
        help_text="Choose an Service Icon."
    )
    title = blocks.CharBlock()
    description = blocks.TextBlock()
    image = ImageChooserBlock()


class ServiceGridBlock(StreamBlock):
    cards = blocks.ListBlock(GridCardBlock())

    # class Meta:
    #     icon = "placeholder"
    #     template = "/blocks/custom_grid_block.html"
    

class FormElementBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=False, help_text="Enter your full name")
    email = blocks.EmailBlock(required=False, help_text="Enter your email address")
    phone_no = blocks.CharBlock(required=False, help_text="Enter your phone number")
    password = blocks.TextBlock(required=False, help_text="Enter your password")
    address = blocks.TextBlock(required=False, help_text="Enter your address")
    post_code = blocks.TextBlock(required=False, help_text="Enter your postal code")


class FormBlock(StreamBlock):
    image = ImageChooserBlock(
        help_text="Choose an image for the form.",
    )
    heading = blocks.CharBlock(help_text="Enter the heading for the content block")
    text = blocks.TextBlock(help_text="Enter the text for the content block")
    elements = FormElementBlock(
        choices=TWO_POSITION_CHOICES,
        default="right",
        blank=True,
        help_text="Select the position for the intro field.",
    )
    
    