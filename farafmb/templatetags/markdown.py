from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from markdown import markdown as render_markdown

register = template.Library()


@register.filter
def render_html(value):
    """Converts markdown styled text to valid html"""
    esc = conditional_escape(value)
    result = render_markdown(esc)
    return mark_safe(result)
