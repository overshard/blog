from django import template

from ..utils import og_image as og_image_util


register = template.Library()


@register.simple_tag
def og_image(url):
    return og_image_util(url)
