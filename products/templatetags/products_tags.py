from django import template
from urlobject import URLObject

register = template.Library()

@register.simple_tag(takes_context=True)
def url_set_param(context, **kwargs):
    url = URLObject(context.request.get_full_path())
    path = url.path
    query = url.query
    for k, v in kwargs.items():
        query = query.set_param(k, v)
    return '{}?{}'.format(path, query)