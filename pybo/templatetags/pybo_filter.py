import markdown
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from django.utils.dateformat import DateFormat

register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))


@register.filter()
def datediff(value):
    return DateFormat(datetime.now() - timedelta(days=365)).format('Y-m-d')