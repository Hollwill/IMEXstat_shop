from django.urls import path
from .views import (
    ResearchListView,
    ResearchDetailView,
    ResearchBuyView,
    ResearchCategoryListView
)
urlpatterns = [
    path('list/<str:type>', ResearchListView.as_view(), name='researchs'),
    path('category/<int:pk>', ResearchCategoryListView.as_view(), name='researchs_category' ),
    path('buy/<int:pk>', ResearchBuyView.as_view(), name='research_buy'),
    path('detail/<int:pk>', ResearchDetailView.as_view(), name='research_detail')
]
