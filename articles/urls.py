from django.urls import path
from .views import (
    ArticlesListView,
    ArticleCategoryListView,
    ArticleDetailView
)

app_name = 'research'

urlpatterns = [
	path('list/', ArticlesListView.as_view(), name='list'),
    path('category/<slug:slug>', ArticleCategoryListView.as_view(), name='category' ),
    path('detail/<slug:slug>', ArticleDetailView.as_view(), name='detail'),
]
