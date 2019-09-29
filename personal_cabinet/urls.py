from django.urls import path
from .views import(
	ProfileFormView,
	FavoriteArticles,
	FavoriteReports,
	) 

app_name = 'lk'

urlpatterns = [
	path('settings/', ProfileFormView.as_view(), name='settings'),
	path('favorite/articles/', FavoriteArticles.as_view(), name='favorite_articles'),
	path('favorite/reports/', FavoriteReports.as_view(), name='favorite_reports'),


]


