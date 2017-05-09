from markdown import markdown as md

from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def markdown(value, autoescape=True):
    """Converts markdown text into html"""
    #if autoescape:
    #    esc = conditional_escape
    #else:
    #    esc = lambda x: x
    return mark_safe(md(conditional_escape(value)))

@register.inclusion_tag('card.html')
def render_card(card):
    title = escape(card.title)
    image = card.image.url if card.image else None
    content = mark_safe(md(conditional_escape(card.content)))
    button = card.button

    if content:
        image_height = 100
    else:
        image_height = 180

    return {'title': title,
            'image': image,
            'content': content,
            'button': button,
            'image_height': image_height,}