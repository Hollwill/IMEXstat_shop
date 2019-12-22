from statistic.models import StatisticData, TnvedHandbook, StatisticDataDocument
from django.db.models import Avg, Max, Sum
from datetime import datetime
from elasticsearch_dsl import Search, A, Index
from elasticsearch_dsl import Q


split_tnved_dict = {
    2: 'tnved_two',
    4: 'tnved_four',
    6: 'tnved_six',
    8: 'tnved_eight',
    10: 'tnved',
}

# def run():
#     for object in TnvedHandbook.objects.all().values_list('tnved'):
#         filter_dict = {split_tnved_dict[len(object[0])]: object[0]}
#         imp_data = Search(index='statistic')
#         imp_data.query = Q('bool', must=[Q('match', napr='ИМ'), Q('match', **filter_dict)])
#         imp_data = imp_data[:imp_data.count()]
#         imp_data.aggs.metric('stoim_sum', 'sum', field='stoim')
#         exp_data = Search(index='statistic')
#         exp_data.query = Q('bool', must=[Q('match', napr='ЭК'), Q('match', **filter_dict)])
#         exp_data = exp_data[:exp_data.count()]
#         exp_data.aggs.metric('m', 'sum', field='stoim')
#         print(exp_data.execute().aggregations)


def run():
    a = Index('statistic')
    a.put_settings(body={"index.max_result_window": "10000000"})