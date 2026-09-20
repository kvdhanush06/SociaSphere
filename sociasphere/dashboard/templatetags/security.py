from urllib.parse import urlparse

from django import template

register = template.Library()


@register.filter
def safe_http_url(value):
    if not isinstance(value, str):
        return ''
    value = value.strip()
    if not value:
        return ''
    try:
        parsed = urlparse(value)
    except ValueError:
        return ''
    if parsed.scheme.lower() not in {'http', 'https'} or not parsed.netloc:
        return ''
    if parsed.username or parsed.password:
        return ''
    return value
