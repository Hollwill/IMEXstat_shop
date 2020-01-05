from django.db import models
from django.contrib.postgres.fields import JSONField
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from datetime import date
import pandas as pd
from django.db.models import Avg, Max, Sum

tnved_dict = {
    2: 'tnved_two',
    4: 'tnved_four',
    6: 'tnved_six',
    8: 'tnved_eight',
    10: 'tnved',
}


class StatisticData(models.Model):
    napr = models.CharField(max_length=2, db_index=True, blank=True, null=True)
    period = models.DateField(db_index=True, blank=True, null=True)
    strana = models.CharField(db_index=True, max_length=3, blank=True, null=True)
    tnved = models.CharField(db_index=True, max_length=10, blank=True, null=True)
    tnved_two = models.CharField(db_index=True, max_length=2, blank=True, null=True)
    tnved_four = models.CharField(db_index=True, max_length=4, blank=True, null=True)
    tnved_six = models.CharField(db_index=True, max_length=6, blank=True, null=True)
    tnved_eight = models.CharField(db_index=True, max_length=8, blank=True, null=True)
    edizm = models.CharField(max_length=20, blank=True, null=True)
    stoim = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    netto = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    kol = models.DecimalField(max_digits=22, decimal_places=0, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    region_s = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def pd_split_dates_by_inreval(cls, request):
        pd_interval = {'year': '12MS', 'month': 'MS', 'quartal': '3MS'}
        interval = request.query_params.get('interval')
        str_date_range = [request.query_params.get('date_from'), request.query_params.get('date_to')]
        date_range = [date(int(a[:4]), int(a[5:7]), 0o01) for a in str_date_range]
        return [i for i in pd.date_range(start=date_range[0], end=date_range[1], freq=pd_interval[interval])]

    @classmethod
    def get_codes_tnved_statistic_with_split_by_dates(cls, request, tnved_list):
        split_dates = cls.pd_split_dates_by_inreval(request)
        imp_data = StatisticData.objects.filter(napr='ИМ')
        exp_data = StatisticData.objects.filter(napr='ЭК')
        tnved_data_list = []
        for tnved in tnved_list:
            tnved_data = {
                'tnved': tnved,
                'exp': {
                    'stoim': [],
                    'weight': []
                },
                'imp': {
                    'stoim': [],
                    'weight': []
                },
            }
            filter_dict = {tnved_dict[len(tnved)]: tnved}
            tnved_imp_data = imp_data.filter(**filter_dict)
            tnved_exp_data = exp_data.filter(**filter_dict)
            for i in range(len(split_dates) - 1):
                tnved_agg_imp = tnved_imp_data.filter(
                    period__range=[split_dates[i], split_dates[i + 1]]).aggregate(
                    Sum('stoim'), Sum('netto'))
                tnved_agg_exp = tnved_exp_data.filter(
                    period__range=[split_dates[i], split_dates[i + 1]]).aggregate(
                    Sum('stoim'), Sum('netto'))
                tnved_data['imp']['stoim'].append(int(tnved_agg_imp['stoim__sum']) if tnved_agg_imp['stoim__sum'] else 0)
                tnved_data['imp']['weight'].append(int(tnved_agg_imp['netto__sum']) if tnved_agg_imp['netto__sum'] else 0)
                tnved_data['exp']['stoim'].append(int(tnved_agg_exp['stoim__sum']) if tnved_agg_exp['stoim__sum'] else 0)
                tnved_data['exp']['weight'].append(int(tnved_agg_exp['netto__sum']) if tnved_agg_exp['netto__sum'] else 0)
            tnved_data_list.append(tnved_data)
        del split_dates[0]
        return tnved_data_list, split_dates


@registry.register_document
class StatisticDataDocument(Document):
    class Index:
        name = 'statistic'

    class Django:
        model = StatisticData
        fields = [
            'tnved',
            'tnved_two',
            'tnved_four',
            'tnved_six',
            'tnved_eight',
            'stoim',
            'netto',
            'napr',
            'period',
            'strana',
        ]


class StatisticAggregateData(models.Model):
    period = models.DateField(db_index=True)
    # таблица "сводка рынка"
    imp_sum_cost = models.BigIntegerField(verbose_name='Импорт - суммарная стоимость')
    exp_sum_cost = models.BigIntegerField(verbose_name='Экспорт - суммарная стоимость')
    imp_sum_weight = models.BigIntegerField(verbose_name='Импорт - суммарный вес')
    exp_sum_weight = models.BigIntegerField(verbose_name='Экспорт - суммарный вес')
    imp_sum_unique_countries = models.BigIntegerField(verbose_name='Импорт - Количество вовлеченных стран')
    exp_sum_unique_countries = models.BigIntegerField(verbose_name='Экспорт - Количество вовлеченных стран')
    imp_tnved_by_max_cost = models.BigIntegerField(verbose_name='Импорт - Код тнвэд имеющий максимальную стоимость')
    exp_tnved_by_max_cost = models.BigIntegerField(verbose_name='Экспорт - Код тнвэд имеющий максимальную стоимость')
    # график динамика экспорта и импорта России


class TnvedHandbook(models.Model):
    tnved = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)


class CountryHandbook(models.Model):
    country = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, blank=True, null=True)


class CountryAggregateData(models.Model):
    country = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    country_long = models.CharField(max_length=255, blank=True, null=True)
    period = models.DateField(db_index=True, blank=True, null=True)
    imp_sum_cost = models.BigIntegerField(blank=True, null=True, verbose_name='Импорт - суммарная стоимость')
    exp_sum_cost = models.BigIntegerField(blank=True, null=True, verbose_name='Экспорт - суммарная стоимость')
    imp_sum_weight = models.BigIntegerField(blank=True, null=True, verbose_name='Импорт - суммарный вес')
    exp_sum_weight = models.BigIntegerField(blank=True, null=True, verbose_name='Экспорт - суммарный вес')

    ''' update statistic_statisticdata
set split_tnved  = json_build_object('two', substring(tnved from 1 for 2),            
'four', substring(tnved from 1 for 4),
'six', substring(tnved from 1 for 6),
'eight', substring(tnved from 1 for 8),
'ten', substring(tnved from 1 for 10))
;'''

