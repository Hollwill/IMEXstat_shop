from django.urls import path
from .views import (
    ResearchListView,
    ResearchDetailView,
    ResearchBuyView,
    ResearchCategoryListView
)
urlpatterns = [
	path('list/', ResearchListView.as_view(), name='research_list'),
    path('catalog/<str:type>', ResearchListView.as_view(), name='research_type'),
    path('category/<slug:slug>', ResearchCategoryListView.as_view(), name='research_category' ),
    path('buy/<slug:slug>', ResearchBuyView.as_view(), name='research_buy'),
    path('detail/<slug:slug>', ResearchDetailView.as_view(), name='research_detail')
]
