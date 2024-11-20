from django import template
from wagtail import blocks


register = template.Library()

@register.filter
def get_streamfield_value(streamfield, block_type):
    for block in streamfield:
        if block.block_type == block_type:
            return block.value
        
    return None