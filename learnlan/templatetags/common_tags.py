from django import template
from django.utils.safestring import mark_safe
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def include_scripts(context):
    if 'scripts' in context:
        return '\n'.join(context['scripts'])
    else:
        return ''


@register.simple_tag
def define(the_string):
    return the_string


@register.filter
def return_safe(str_):
    return mark_safe(str_)
