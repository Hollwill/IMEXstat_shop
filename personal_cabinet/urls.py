from django.urls import path
from .views import ProfileSettingsView, ProfileFormView, RequizitesFormView

urlpatterns = [
	path('settings/<slug:slug>/', ProfileSettingsView.as_view(), name='lk_settings'),
	path('profile_form', ProfileFormView.as_view(), name='profile_form' ),
	path('requizites_form', RequizitesFormView.as_view(), name='requizites_form' )

]


