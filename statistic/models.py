from django.db import models
from django.contrib.postgres.fields import JSONField

class StatisticData(models.Model):
    napr = models.CharField(max_length=2, db_index=True, blank=True, null=True)
    period = models.DateField(db_index=True, blank=True, null=True)
    strana = models.CharField(db_index=True, max_length=3, blank=True, null=True)
    tnved = models.CharField(db_index=True, max_length=10, blank=True, null=True)
    split_tnved = JSONField(db_index=True, blank=True, null=True)
    edizm = models.CharField(max_length=20, blank=True, null=True)
    stoim = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    netto = models.DecimalField(db_index=True, max_digits=22, decimal_places=0, blank=True, null=True)
    kol = models.DecimalField(max_digits=22, decimal_places=0, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    region_s = models.CharField(max_length=255, blank=True, null=True)


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

    ''' update statistic_statisticdata
set split_tnved  = json_build_object('two', substring(tnved from 1 for 2),            
'four', substring(tnved from 1 for 4),
'six', substring(tnved from 1 for 6),
'eight', substring(tnved from 1 for 8),
'ten', substring(tnved from 1 for 10))
;'''

