from django.urls import path
from .views import ProfileFormView

app_name = 'lk'

urlpatterns = [
	path('settings/', ProfileFormView.as_view(), name='settings'),


]


