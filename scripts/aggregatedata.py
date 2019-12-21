from statistic.models import StatisticAggregateData, StatisticData
from django.db.models import Sum, Max

def run():
    unique_dates = StatisticData.objects.all().values('period').distinct()
    a = 1
    for date in unique_dates:
        date = date['period']
        imp_data = StatisticData.objects.filter(napr='ИМ', period=date)
        exp_data = StatisticData.objects.filter(napr='ЭК', period=date)

        imp_cost = int(imp_data.aggregate(Sum('stoim'))['stoim__sum'])
        imp_weight = int(imp_data.aggregate(Sum('netto'))['netto__sum'])
        imp_country = imp_data.values('strana').distinct().count()
        imp_max_stoim = imp_data.filter(tnved__regex=r'\d+').aggregate(Max('stoim'))['stoim__max']
        imp_tnved = imp_data.get(stoim=imp_max_stoim).tnved

        exp_cost = int(exp_data.aggregate(Sum('stoim'))['stoim__sum'])
        exp_weight = int(exp_data.aggregate(Sum('netto'))['netto__sum'])
        exp_country = exp_data.values('strana').distinct().count()
        exp_max_stoim = exp_data.filter(tnved__regex=r'\d+').aggregate(Max('stoim'))['stoim__max']
        exp_tnved = exp_data.get(stoim=exp_max_stoim).tnved
        model = StatisticAggregateData(
            period=date,
            imp_sum_cost=imp_cost,
            exp_sum_cost=exp_cost,
            imp_sum_weight=imp_weight,
            exp_sum_weight=exp_weight,
            imp_sum_unique_countries=imp_country,
            exp_sum_unique_countries=exp_country,
            imp_tnved_by_max_cost=imp_tnved,
            exp_tnved_by_max_cost=exp_tnved
        )
        model.save()
        print('model %d created' % a)
        a += 1
