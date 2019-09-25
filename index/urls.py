from django.urls import path
from .views import IndexList

app_name = 'index'


urlpatterns = [
	path('', IndexList.as_view(template_name="index/index.html"), name='index' )
]