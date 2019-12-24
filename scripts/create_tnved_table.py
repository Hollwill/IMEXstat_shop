from statistic.models import StatisticData, TnvedHandbook, StatisticDataDocument
from elasticsearch_dsl import Q

def run():
    s = StatisticDataDocument.search()
    s.aggs.bucket('a', 'terms', field='tnved_two', size=200)
    result = s.execute()
    tnved_two_distinct = [item.key for item in result.aggregations.a.buckets]
    s = StatisticDataDocument.search().params(request_timeout=100)
    print('test')
    for i in tnved_two_distinct:
        s.query = Q('bool', must=[Q('match', napr='ЭК'), Q('match', tnved_two=i)])
        s.aggs.metric('stoim', 'sum', field='stoim')
        s.aggs.metric('netto', 'sum', field='netto')
        print('all ok')
        result = s[:s.count()].execute().aggregations
        print('all ok')
        print(result)