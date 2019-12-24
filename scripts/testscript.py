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



def run():
    # s = Search(index='statistic').params(request_timeout=100)
    # s.aggs.bucket('a', 'terms', field='tnved_two', size=200)
    #
    # response = s.execute()
    # print(len(response.aggregations.a.buckets))
    # a = []
    # for item in response.aggregations.a.buckets:
    #     a.append(item.key)
    # print([item for item, count in collections.Counter(a).items() if count > 1])

    s = StatisticDataDocument.search()
    s.aggs.bucket('a', 'terms', field='tnved_two', size=200)
    result = s.execute()
    a = [item.key for item in result.aggregations.a.buckets]



# def run():
#     print([i['tnved_two'] for i in StatisticData.objects.values('tnved_two').distinct()])