from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from personal_cabinet.views import RegisterFormView
from django.contrib import flatpages 


urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('index.urls', namespace='index')),
    path('lk/', include('personal_cabinet.urls', namespace='lk')),
    path('research/', include('products.urls', namespace='research')),
    path('article/', include('articles.urls', namespace='article')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', RegisterFormView.as_view(), name='register'),
    path('order/', include('orders.urls', namespace='orders')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('handbook/', include('handbook.urls', namespace='handbook') )

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()