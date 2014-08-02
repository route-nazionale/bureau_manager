
from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def setting(setting_var):
    return getattr(settings, setting_var)

