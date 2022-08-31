from django import template
from django.utils.safestring import mark_safe
import markdown
import re

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='phone_link')
def phone_link_format(text):
    return f'tel:+{re.sub("[^0-9]", "", text)}'
