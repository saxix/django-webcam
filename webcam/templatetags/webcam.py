from django.templatetags.static import static, PrefixNode
from urlparse import urljoin
from django import template
from django.utils.encoding import iri_to_uri

register = template.Library()

@register.inclusion_tag('webcam/camera.html')
def camera():
    return {}
