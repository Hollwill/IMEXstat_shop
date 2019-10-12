from django.urls import path
from .views import IndexList, IndexFormView, ContactsList, InnView, autocomplete

app_name = 'index'


urlpatterns = [
	path('autocomplete/', autocomplete, name='autocomplete'),
	path('', IndexList.as_view(template_name="index/index.html"), name='index' ),
	path('form/', IndexFormView.as_view(), name='form'),
	path('contacts/', ContactsList.as_view(), name='contacts'),
	path('inn/', InnView.as_view(), name='inn')
]