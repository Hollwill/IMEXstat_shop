from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('index.urls', namespace='index')),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('lk/', include('personal_cabinet.urls', namespace='lk')),
    path('research/', include('products.urls', namespace='research')),
    path('article/', include('articles.urls', namespace='article')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', include('django_registration.backends.activation.urls')),
    path('order/', include('orders.urls', namespace='orders')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('statistic/', include('statistic.urls', namespace='statistic')),
    path('nested_admin/', include('nested_admin.urls')),
]

# Справочник вырезан из кода на время
# path('handbook/', include('handbook.urls', namespace='handbook')),

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()