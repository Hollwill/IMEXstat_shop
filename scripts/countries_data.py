from statistic.models import StatisticData, CountryAggregateData
from django.db.models import Sum
from datetime import datetime


uniq_period_val = [i['period'] for i in StatisticData.objects.all().values('period').distinct()]
b = len(uniq_period_val)

for period in uniq_period_val:
    print('----------------------%s' % b)
    b -= 1
    c = datetime.now()
    uniq_country_val = [i['strana'] for i in StatisticData.objects.filter(period=period).values('strana').distinct()]
    a = len(uniq_country_val)
    for val in uniq_country_val:
        a -= 1
        aggregate_data_imp = StatisticData.objects.filter(strana=val, napr='ЭК').aggregate(Sum('netto'), Sum('stoim'))
        aggregate_data_exp = StatisticData.objects.filter(strana=val, napr='ИМ').aggregate(Sum('netto'), Sum('stoim'))
        imp_sum_cost = int(aggregate_data_imp['stoim__sum']) if aggregate_data_imp['stoim__sum'] else None
        imp_sum_weight = int(aggregate_data_imp['netto__sum']) if aggregate_data_imp['netto__sum'] else None
        exp_sum_cost = int(aggregate_data_exp['stoim__sum']) if aggregate_data_exp['stoim__sum'] else None
        exp_sum_weight = int(aggregate_data_exp['netto__sum']) if aggregate_data_exp['netto__sum'] else None
        CountryAggregateData.objects.create(
            period=period,
            country=val,
            imp_sum_cost=imp_sum_cost,
            imp_sum_weight=imp_sum_weight,
            exp_sum_cost=exp_sum_cost,
            exp_sum_weight=exp_sum_weight
        )
        print(a)
    print(datetime.now() - c)