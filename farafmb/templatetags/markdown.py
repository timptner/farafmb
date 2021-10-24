import bleach
import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def render_html(value, autoescape=True):
    """Converts markdown styled text to valid html"""
    # We need to process markdown before sanitizing html
    # Otherwise some elements (e.g. blockquotes) will break
    html = markdown.markdown(value, extensions=['toc', 'sane_lists'])
    if autoescape:
        safe_html = bleach.clean(
            html,
            tags=[
                'a', 'blockquote', 'br', 'code', 'div', 'em', 'hr', 'h1', 'h2', 'h3',
                'h4', 'h5', 'h6', 'img', 'li', 'ol', 'p', 'pre', 'strong', 'ul',
            ],
            attributes={
                'a': ['href', 'title'],
                'div': ['class'],
                'h1': ['id'],
                'h2': ['id'],
                'h3': ['id'],
                'h4': ['id'],
                'h5': ['id'],
                'h6': ['id'],
                'img': ['alt', 'src', 'title'],
            },
        )
    else:
        safe_html = html
    return mark_safe(safe_html)
