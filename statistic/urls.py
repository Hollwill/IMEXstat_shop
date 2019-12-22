from .views import MarketSummary, ExpImpDynamics, TurnoverStructure
from rest_framework import routers
from django.urls import path
from django.views.generic import TemplateView


app_name = 'statistic'
router = routers.DefaultRouter()

urlpatterns = [
    path('', TemplateView.as_view(template_name='statistic.html'), name='statistic'),
    path('market_summary/', MarketSummary.as_view(), name='market_summary'),
    path('exp_imp_dynamics/', ExpImpDynamics.as_view(), name='exp_imp_dynamics'),
    path('turnover_structure/', TurnoverStructure.as_view(), name='turnover_structure'),
]

urlpatterns += router.urls