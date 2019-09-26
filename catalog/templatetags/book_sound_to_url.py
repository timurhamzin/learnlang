from django import template
from django.conf import settings

register = template.Library()


# @register.filter
# def book_sound_to_url(book_sound):
#     from os import path
#     print('!!!!!!!!', book_sound.url)
#     if book_sound:
#         if path.isfile(book_sound.url):
#             url = book_sound.url
#         else:
#             url = book_sound.url[len(settings.MEDIA_ROOT):]
#         return url.replace(' ', '%20')
