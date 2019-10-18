from django.urls import path
from  .views import HandbookList

app_name='handbook'

urlpatterns = [
	path('', HandbookList.as_view(), name='handbook' )	
]