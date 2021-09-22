from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from markdown import markdown

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def render_html(text, autoescape=True):
    """Render markdown formatted text to valid html"""
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = markdown(esc(text))
    return mark_safe(result)
