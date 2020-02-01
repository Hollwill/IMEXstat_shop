from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Model
from django.template import Library
from django.utils.translation import to_locale, get_language
from  project import settings
register = Library()


@register.inclusion_tag('seo/seo.html', takes_context=True)
def get_seo_data(context, seo, obj: Model = None):
    """
    Renders meta data for given obj, that can be
    some instance which inherits SeoTagsMixin mixin
    """

    request = context.request
    return {
        'request': request,
        'canonical': request.build_absolute_uri(),
        'og_locale': to_locale(get_language()),
        'site_name': settings.Base.SEO_SITE_NAME if settings.Base.SEO_SITE_NAME else get_current_site(context.request),
    }