from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailstreamforms.blocks import WagtailFormBlock

from .richtext_features import ALL_RICHTEXT_FEATURES


class BlogCommonBlocks(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock(features=ALL_RICHTEXT_FEATURES)
    raw_html = blocks.RawHTMLBlock()
    image = ImageChooserBlock()
    block_quote = blocks.BlockQuoteBlock()
    embed = EmbedBlock()


class EventPageBlocks(blocks.StreamBlock):
    rich_text = blocks.RichTextBlock(features=ALL_RICHTEXT_FEATURES)
    raw_html = blocks.RawHTMLBlock()
    image = ImageChooserBlock()
    block_quote = blocks.BlockQuoteBlock()
    embed = EmbedBlock()
    form = WagtailFormBlock()
