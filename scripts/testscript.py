from statistic.models import StatisticData, TnvedHandbook, StatisticDataDocument
from django.db.models import Avg, Max, Sum
from datetime import datetime
from elasticsearch_dsl import Search, A, Index
import collections
from elasticsearch_dsl import Q


split_tnved_dict = {
    2: 'tnved_two',
    4: 'tnved_four',
    6: 'tnved_six',
    8: 'tnved_eight',
    10: 'tnved',
}

# def run():
#     country_dict = StatisticData.objects.all().values('strana').distinct()
#     country_list = [i['strana'] for i in country_dict]
#     for country in country_list:
#         imp_data = StatisticData.objects.filter(napr='ИМ', strana=country)
#         exp_data = StatisticData.objects.filter(napr='ЭК', strana=country)
#         imp_agg_data = imp_data.aggregate(Sum('netto'), Sum('stoim'))
#         exp_agg_data = exp_data.aggregate(Sum('netto'), Sum('stoim'))
#         print(imp_agg_data)
#         print(exp_agg_data)

def run():
    country_dict = StatisticData.objects.all().values('strana').distinct()
    country_list = [i['strana'] for i in country_dict]
    s = Search(index='statistic').params(request_timeout=100)
    for country in country_list:
        s.query = Q('match', strana=country)
        s.aggs.bucket('stoim', 'sum', field='stoim')
        s.aggs.bucket('netto', 'sum', field='netto')
        result = s[:s.count()].execute().aggregations
<<<<<<< HEAD
        print(result)
=======
        print(result)
>>>>>>> 21eb6125a5978c9ae28bac91153bd364503a4655
