from django.urls import path
from .views import (
    ResearchListView,
    ResearchDetailView,
    ResearchBuyView,
    ResearchCategoryListView
)

app_name = 'research'

urlpatterns = [
	path('list/', ResearchListView.as_view(), name='list'),
    path('catalog/<str:type>', ResearchListView.as_view(), name='type'),
    path('category/<slug:slug>', ResearchCategoryListView.as_view(), name='category' ),
    path('buy/<slug:slug>', ResearchBuyView.as_view(), name='buy'),
    path('detail/<slug:slug>', ResearchDetailView.as_view(), name='detail')
]
