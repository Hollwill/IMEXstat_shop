from .views import (MarketSummary, ExpImpDynamics, TurnoverStructure, CountryStatistic, Autocomplete,
                    TopBlock, MiddleBlock, DownBlock, DetailedMiddleBlock, DetailedDownBlock)

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
    path('report/top_block/', TopBlock.as_view(), name='tnved_dynamics'),
    path('report/middle_block/', MiddleBlock.as_view(), name='country_report'),
    path('report/middle_block/detailed/', DetailedMiddleBlock.as_view(), name='detailed_counrty_report'),
    path('report/down_block/', DownBlock.as_view(), name='region_report'),
    path('report/down_block/detailed/', DetailedDownBlock.as_view(), name='detailed_region_report'),

    # path('country_dynamics/', CountryDynamic.as_view(), name='tnved_dynamics'),
    # path('tnved_report_by_country/', TnvedReportByCountry.as_view(), name='country_report'),
    # path('detailed_tnved_report_by_country/', DetailedTnvedReportByCountry.as_view(), name='detailed_counrty_report'),
    # path('region_report_by_country/', RegionReportByCountry.as_view(), name='region_report'),
    # path('detailed_region_report_by_country/', DetailedRegionReportByCountry.as_view(), name='detailed_region_report')
]

urlpatterns += router.urls
