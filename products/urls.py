from django.urls import path
from .views import (
    ResearchListView,

    ResearchBuyView,
    ResearchCategoryListView,
    autocomplete,
    IndividualResearchFeedbackView

)

app_name = 'research'

urlpatterns = [
    path('list/autocomplete', autocomplete, name='autocomplete'),
    path('list/', ResearchListView.as_view(), name='list'),
    path('individual/', IndividualResearchFeedbackView.as_view(), name='individual'),
    # path('catalog/<str:type>/', ResearchListView.as_view(), name='type'),
    path('category/<slug:slug>/', ResearchCategoryListView.as_view(), name='category'),
    path('buy/<slug:slug>/', ResearchBuyView.as_view(), name='buy'),
]
