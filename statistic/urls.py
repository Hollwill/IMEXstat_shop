from .views import MarketSummary, ExpImpDynamics, TurnoverStructure, CountryStatistic, Autocomplete,\
    TnvedDynamic, DetailedCountryReportByTnved, CountryReportByTnved, RegionReportByTnved, DetailedRegionReportByTnved
    # CountryDynamic, TnvedReportByCountry, DetailedTnvedReportByCountry, RegionReportByCountry, DetailedRegionReportByCountry
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
    path('country_report/', CountryReportByTnved.as_view(), name='country_report'),
    path('detailed_country_report/', DetailedCountryReportByTnved.as_view(), name='detailed_counrty_report'),
    path('region_report/', RegionReportByTnved.as_view(), name='region_report'),
    path('detailed_region_report/', DetailedRegionReportByTnved.as_view(), name='detailed_region_report'),


    # path('country_dynamics/', CountryDynamic.as_view(), name='tnved_dynamics'),
    # path('tnved_report_by_country/', TnvedReportByCountry.as_view(), name='country_report'),
    # path('detailed_tnved_report_by_country/', DetailedTnvedReportByCountry.as_view(), name='detailed_counrty_report'),
    # path('region_report_by_country/', RegionReportByCountry.as_view(), name='region_report'),
    # path('detailed_region_report_by_country/', DetailedRegionReportByCountry.as_view(), name='detailed_region_report'),
]

urlpatterns += router.urls
