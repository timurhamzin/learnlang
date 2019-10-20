from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def include_scripts(context):
    if uses_jquery(context):
        if settings.DEBUG:
            return '<script src="jquery-3.4.1.min.js"></script>'
        else:
            return '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js">'
    else:
        return ''


def uses_jquery(context):
    urlnames = 'book_deconjugated'
    if context['request'].resolver_match.url_name in urlnames.split():
        return True
    else:
        return False
