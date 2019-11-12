from django.urls import path
from .views import (
    IndexList,
    IndexFormView,
    ContactsList,
    InnView,
    autocomplete,
    AnalysisView,
    Analysis2View,
    ElectionView,
    SearchView,
    RobotsView
)

app_name = 'index'

urlpatterns = [
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('', IndexList.as_view(template_name="index/index.html"), name='index'),
    path('form/', IndexFormView.as_view(), name='form'),
    path('contacts/', ContactsList.as_view(), name='contacts'),
    path('inn/', InnView.as_view(), name='inn'),
    path('analysis/', AnalysisView.as_view(), name='analysis'),
    path('analysis2/', Analysis2View.as_view(), name='analysis2'),
    path('election/', ElectionView.as_view(), name='election'),
    path('search/', SearchView.as_view(), name='search'),
    path('robots.txt/', RobotsView.as_view(), name='robots')
]
