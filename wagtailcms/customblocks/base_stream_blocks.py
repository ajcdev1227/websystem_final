from wagtail.blocks import StreamBlock, RawHTMLBlock
# from wagtail.embeds.blocks import EmbedBlock
# from wagtail.images.blocks import ImageChooserBlock

from .image_blocks import *
from .text_blocks import *
from .boxes_blocks import *
from .richtext_features import ALL_RICHTEXT_FEATURES
from wagtailstreamforms.blocks import WagtailFormBlock


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """
    # Form Block
    form = WagtailFormBlock()

    # Text Blocks
    raw_html = RawHTMLBlock()
    spacing_block = SpacingBlock()
    ParagraphBlock_ = ParagraphBlock()
    HeadingBlock_ = HeadingBlock()
    ButtonBlock_ = ButtonBlock()
    TextWithHeading_ = TextWithHeading()
    RichTextEditorBlock_ = RichTextEditorBlock(features=ALL_RICHTEXT_FEATURES)

    # Image Blocks
    video_block = VideoBlock()
    carousel_block = CarouselBlock()
    left_image_section_block = LeftImageSectionBlock()
    right_image_section_block = RightImageSectionBlock()
    circle_left_image_section_block = CircleLeftImageSectionBlock()
    circle_right_image_section_block = CircleRightImageSectionBlock()

    # Boxes Blocks
    information_grid_block = InformationGridBlock()
    facts = FactsBlock()
    about_us = AboutUsBlock()
    services = ServicesBlock()
    projects = ProjectsBlock()
    team_members = TeamMembersBlock()
    testimonials = TestimonialsBlock()
    about_us_cards = AboutUsCardBlock()
    features_blocks = FeaturesBlock()
    TwoBoxesBlock_ = TwoBoxesBlock()
    ThreeBoxesBlock_ = ThreeBoxesBlock()
    FourBoxesBlock_ = FourBoxesBlock()

    TwoBoxesBlockwithImage_ = TwoBoxesBlockwithImage()
    ThreeBoxesBlockwithImage_ = ThreeBoxesBlockwithImage()
    FourBoxesBlockwithImage_ = FourBoxesBlockwithImage()

    TwoBoxesBlockwithIcon_ = TwoBoxesBlockwithIcon()
    ThreeBoxesBlockwithIcon_ = ThreeBoxesBlockwithIcon()
