from .models import StatisticData, StatisticAggregateData, StatisticDataDocument
from django.db.models import Avg, Max
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date
import pandas as pd
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from math import ceil
import datetime


class MarketSummary(APIView):
    def get(self, request):
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']

        imp_data = StatisticAggregateData.objects.filter(period__range=date_range)
        exp_data = StatisticAggregateData.objects.filter(period__range=date_range)

        imp_cost = int(imp_data.aggregate(Avg('imp_sum_cost'))['imp_sum_cost__avg'])
        imp_weight = int(imp_data.aggregate(Avg('imp_sum_weight'))['imp_sum_weight__avg'])
        imp_country = imp_data.values('imp_sum_unique_countries').distinct().count()
        imp_max_stoim = imp_data.aggregate(Max('imp_sum_cost'))['imp_sum_cost__max']
        imp_tnved = imp_data.get(imp_sum_cost=imp_max_stoim).imp_tnved_by_max_cost

        exp_cost = int(exp_data.aggregate(Avg('exp_sum_cost'))['exp_sum_cost__avg'])
        exp_weight = int(exp_data.aggregate(Avg('exp_sum_weight'))['exp_sum_weight__avg'])
        exp_country = exp_data.values('exp_sum_unique_countries').distinct().count()
        exp_max_stoim = exp_data.aggregate(Max('exp_sum_cost'))['exp_sum_cost__max']
        exp_tnved = exp_data.get(exp_sum_cost=exp_max_stoim).exp_tnved_by_max_cost

        context = {
            'imp': {
                'cost': imp_cost,
                'weight': imp_weight,
                'country': imp_country,
                'tnved': imp_tnved
            },
            'exp': {
                'cost': exp_cost,
                'weight': exp_weight,
                'country': exp_country,
                'tnved': exp_tnved
            }

        }
        # serializer = MarketSummarySerializer(instance=context)
        return JsonResponse(context)


class ExpImpDynamics(APIView):
    def get(self, request):
        def dynamics_list(dataset):
            a = []
            b = 0
            for i in dataset:
                a.append(int((100 * b / i) - 100))
                b = i
                a[0] = 0
            return a

        pd_interval = {
            'year': '12MS',
            'month': 'MS',
            'quartal': '3MS'
        }
        interval = request.query_params.get('interval')
        raw_date_range = [request.query_params.get('date_from'), request.query_params.get('date_to')]
        date_range = [date(int(a[:4]), int(a[5:7]), 0o01) for a in raw_date_range]
        dates_list = [i for i in pd.date_range(start=date_range[0], end=date_range[1], freq=pd_interval[interval])]
        format_dates_list = [i.strftime("%Y-%m-%d") for i in dates_list]
        data_objects_list = [StatisticAggregateData.objects.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]]) for i in range(len(format_dates_list) - 1)]
        imp_cost_list = [int(a.aggregate(Avg('imp_sum_cost'))['imp_sum_cost__avg']) for a in data_objects_list]
        exp_cost_list = [int(a.aggregate(Avg('exp_sum_cost'))['exp_sum_cost__avg']) for a in data_objects_list]
        imp_weight_list = [int(a.aggregate(Avg('imp_sum_weight'))['imp_sum_weight__avg']) for a in data_objects_list]
        exp_weight_list = [int(a.aggregate(Avg('exp_sum_weight'))['exp_sum_weight__avg']) for a in data_objects_list]
        label_list = [i.strftime("%Y") if interval == 'year' else i.strftime("%Y-%m") for i in dates_list]
        label_list.pop()
        # def aggregate_years(item, items_param, year):
        #       # Todo: переделать функцию
        #     return int(item.filter(period__range=[date_range[0].strftime('%Y-01-%d'), '%s-%s' % (str(year) + '-01',  date_range[1].strftime('%d'))]).aggregate(Avg(items_param))[items_param + '__avg'])
        # interval = request.query_params.get('interval')
        # # берем строку даты в url параметрах
        # date_range = [request.query_params.get('date_from'), request.query_params.get('date_to')]
        # # делаем строку объектом даты
        # date_range = [date(int(a[:4]), int(a[5:7]), 0o01) for a in date_range]
        # imp_data = StatisticData.objects.filter(napr='ИМ')
        # exp_data = StatisticData.objects.filter(napr='ЭК')
        # # согласно заданному интервалу, выдаем соответствующие данные
        # if interval == 'year':
        #     label_list = [date_range[1].year - i for i in reversed(range(date_range[1].year - date_range[0].year + 1))]
        #     imp_cost_list = [aggregate_years(imp_data, 'stoim', i) for i in label_list]
        #     exp_cost_list = [aggregate_years(exp_data, 'stoim', i) for i in label_list]
        #     imp_weight_list = [aggregate_years(imp_data, 'netto', i) for i in label_list]
        #     exp_weight_list = [aggregate_years(exp_data, 'netto', i) for i in label_list]
        # elif interval == 'quartal' or interval == 'month':
        #     label_list = []
        #     current_time = copy.deepcopy(date_range[1])
        #     # делаем список согласно выбранному интервалу из заданного промежутка
        #     while date_range[0] <= current_time:
        #         label_list.insert(0, current_time.strftime("%Y-%m"))
        #         current_time = current_time - relativedelta(months=3 if interval == 'quartal' else 1)
        #     # Если начальная дата не входит в список, то добавляем ее
        #     label_list.insert(0, date_range[0].strftime('%Y-%m')) if not label_list[0] == date_range[0].strftime('%Y-%m') else None
        #     imp_data_list = []
        #     exp_data_list = []
        #     # берем из базы данных объекты согласно заданному интервалу
        #     for i in range(len(label_list) - 1):
        #         imp_data_list.append(imp_data.filter(period__range=[label_list[i] + '-01', label_list[i + 1] + '-01']))
        #         exp_data_list.append(exp_data.filter(period__range=[label_list[i] + '-01', label_list[i + 1] + '-01']))
        #     label_list.pop(0)
        #     # считаем нужные данные исходя из выбранных записей.
        #     imp_cost_list = [int(a.aggregate(Avg('stoim'))['stoim__avg']) for a in imp_data_list]
        #     exp_cost_list = [int(a.aggregate(Avg('stoim'))['stoim__avg']) for a in exp_data_list]
        #     imp_weight_list = [int(a.aggregate(Avg('netto'))['netto__avg']) for a in imp_data_list]
        #     exp_weight_list = [int(a.aggregate(Avg('netto'))['netto__avg']) for a in exp_data_list]

        # def datasets_fragment(data_list1, data_list2):
        #     return [
        #         {
        #             'label': 'Импорт',
        #             'backgroundColor': '#FFF839',
        #             'data': data_list1
        #         },
        #         {
        #             'label': 'Экспорт',
        #             'backgroundColor': '#1221FF',
        #             'data': data_list2
        #         }
        #     ]
        context = {
            'labels': label_list,
            'imp_cost_list': [imp_cost_list, dynamics_list(imp_cost_list)],
            'exp_cost_list': [exp_cost_list, dynamics_list(exp_cost_list)],
            'imp_weight_list': [imp_weight_list, dynamics_list(imp_weight_list)],
            'exp_weight_list': [exp_weight_list, dynamics_list(exp_weight_list)],
        }
        # context = {
        #     'chart': {
        #         'cost': {
        #             'chartdata': {
        #                 'labels': label_list,
        #                 'datasets': datasets_fragment(imp_cost_list, exp_cost_list)
        #             }
        #         },
        #         'netto': {
        #             'chartdata': {
        #                 'labels': label_list,
        #                 'datasets': datasets_fragment(imp_weight_list, exp_weight_list)
        #             }
        #
        #         }
        #     }
        # }
        return JsonResponse(context)


tnved_dict = {
    2: 'tnved_two',
    4: 'tnved_four',
    6: 'tnved_six',
    8: 'tnved_eight',
    10: 'tnved',
}


class TurnoverStructure(APIView):
    def get(self, request):
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
        type = request.query_params.get('type')
        type_dict = {'IM': 'ИМ', 'EK': 'ЭК'}
        s = Search(index='statistic')
        tnved = request.query_params.get('tnved')
        print(datetime.datetime.now())
        if not tnved:
            tnved_list = StatisticData.objects.values('tnved_two').distinct()
            for i in tnved_list:
                s.filter(Q('range', date={'gte': date_range[0], 'lt': date_range[1]}))
                s.query = Q('bool', must=[Q('match', napr=type_dict[type]), Q('match', tnved_two=i['tnved_two'])])
                s.aggs.metric('stoim', 'sum', field='stoim')
                s.aggs.metric('netto', 'sum', field='netto')
                try:
                    print(s[:s.count()].execute().aggregations)
                except:
                    print('timed out')
                # stoim = 0
                # netto = 0
                # a = 1
                # for i in range(1, ceil(s.count() // 10000)):
                #     print(a)
                #     print(i * 10000)
                #     agg_result = s[a:i * 10000].execute().aggregations
                #     a += 10000
                #     netto += agg_result['netto']['value']
                #     stoim += agg_result['stoim']['value']
