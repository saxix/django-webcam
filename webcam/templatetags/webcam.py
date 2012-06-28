from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static, PrefixNode
from urlparse import urljoin
from django import template
from django.utils.encoding import iri_to_uri

register = template.Library()

@register.inclusion_tag('webcam/camera.html')
def camera(save_url, initial=None, callback="_callback"):
    if not save_url:
        raise ImproperlyConfigured('`camera` templatetag expect a url as argument')

    return {'url': save_url,
            'callback':callback,
            'initial':initial,
            }

@register.filter
def default_image(imagefield, default):
    try:
        return imagefield.url
    except ValueError:
        return default
