import bleach

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import markdown as render_markdown

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def render_html(value, autoescape=True):
    """Converts markdown styled text to valid html"""
    # We need to process markdown before sanitizing html
    # Otherwise some elements (e.g. blockquotes) will break
    html = render_markdown(value)
    if autoescape:
        safe_html = bleach.clean(
            html,
            tags=[
                'a', 'blockquote', 'br', 'code', 'em', 'hr', 'h1', 'h2', 'h3',
                'h4', 'h5', 'h6', 'img', 'li', 'ol', 'p', 'pre', 'strong', 'ul',
            ],
            attributes={
                'a': ['href', 'title'],
                'img': ['alt', 'src', 'title'],
            },
        )
    else:
        safe_html = html
    return mark_safe(safe_html)
