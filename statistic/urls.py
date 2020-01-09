from .views import MarketSummary, ExpImpDynamics, TurnoverStructure, CountryStatistic, Autocomplete,\
    TnvedDynamic, DetailedCountryReport, CountryReport, RegionReport, DetailedRegionReport
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
    path('country_statistic/', CountryStatistic.as_view(), name='country_statistic'),
    path('autocomplete/', Autocomplete.as_view(), name='autocomplete'),
    path('tnved_dynamics/', TnvedDynamic.as_view(), name='tnved_dynamics'),
    path('country_report/', CountryReport.as_view(), name='country_report'),
    path('detailed_country_report/', DetailedCountryReport.as_view(), name='detailed_counrty_report'),
    path('region_report/', RegionReport.as_view(), name='region_report'),
    path('detailed_region_report/', DetailedRegionReport.as_view(), name='detailed_region_report'),
]

urlpatterns += router.urls
