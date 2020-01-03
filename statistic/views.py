from .models import StatisticData, StatisticAggregateData, StatisticDataDocument, CountryAggregateData, CountryHandbook
from django.db.models import Avg, Max, Sum
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date
import pandas as pd
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q


class Autocomplete(APIView):
    def get(self, request):
        search = request.query_params.get('q')
        if search:
            values_list = [i['tnved'] for i in StatisticData.objects.filter(tnved__startswith=search).values('tnved').distinct()][:5]
            return JsonResponse(values_list, safe=False)


class MarketSummary(APIView):
    def get(self, request):
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']

        imp_data = StatisticAggregateData.objects.filter(period__range=date_range)
        exp_data = StatisticAggregateData.objects.filter(period__range=date_range)

        imp_cost = int(imp_data.aggregate(Sum('imp_sum_cost'))['imp_sum_cost__sum'])
        imp_weight = int(imp_data.aggregate(Sum('imp_sum_weight'))['imp_sum_weight__sum'])
        imp_country = imp_data.values('imp_sum_unique_countries').distinct().count()
        imp_max_stoim = imp_data.aggregate(Max('imp_sum_cost'))['imp_sum_cost__max']
        imp_tnved = imp_data.get(imp_sum_cost=imp_max_stoim).imp_tnved_by_max_cost

        exp_cost = int(exp_data.aggregate(Sum('exp_sum_cost'))['exp_sum_cost__sum'])
        exp_weight = int(exp_data.aggregate(Sum('exp_sum_weight'))['exp_sum_weight__sum'])
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
        def dynamics_list(d):
            res = [int((d[i + 1] - d[i]) / d[i] * 100) for i in range(len(d) - 1)]
            res.insert(0, 0)
            return res

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
        context = {
            'labels': label_list,
            'imp_cost_list': [imp_cost_list, dynamics_list(imp_cost_list)],
            'exp_cost_list': [exp_cost_list, dynamics_list(exp_cost_list)],
            'imp_weight_list': [imp_weight_list, dynamics_list(imp_weight_list)],
            'exp_weight_list': [exp_weight_list, dynamics_list(exp_weight_list)],
        }
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
        def dynamics_list(d):
            res = [0 if d[i] == 0 else int((d[i+1] - d[i])/d[i] * 100) for i in range(len(d)-1)]
            res.insert(0, 0)
            return res
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
        date_range = [date(int(a[:4]), int(a[5:7]), 0o01) for a in date_range]
        type = request.query_params.get('category')
        s = Search(index='statistic').params(request_timeout=100)
        tnved = request.query_params.get('tnved')
        start_tnved_list = int(request.query_params.get('start'))
        length_tnved_list = int(request.query_params.get('length'))
        label_list = []
        netto_list = []
        stoim_list = []
        if not tnved:
            two_tnved_list_request = StatisticDataDocument.search()
            two_tnved_list_request.aggs.bucket('a', 'terms', field='tnved_two', size=200)
            result = two_tnved_list_request.execute()
            tnved_two_distinct = [item.key for item in result.aggregations.a.buckets]
            tnved_two_distinct.reverse()
            for i in tnved_two_distinct[start_tnved_list:start_tnved_list + length_tnved_list]:
                s.query = Q('bool', must=[Q('match', napr=type),
                                          Q('match', tnved_two=i),
                                          Q('range', period={'gte': date_range[0], 'lt': date_range[1]})])
                s.aggs.bucket('stoim', 'sum', field='stoim')
                s.aggs.bucket('netto', 'sum', field='netto')
                result = s[:s.count()].execute().aggregations
                label_list.append(i)
                netto_list.append(result['netto']['value'])
                stoim_list.append(result['stoim']['value'])
        else:
            tnved_distinct = [i[tnved_dict[len(tnved) + 2]] for i in StatisticData.objects.filter(**{tnved_dict[len(tnved)]: tnved}).values(tnved_dict[len(tnved) + 2]).distinct()]
            for i in tnved_distinct[start_tnved_list:start_tnved_list + length_tnved_list]:
                tnved_query_field = {tnved_dict[len(tnved) + 2]: i}
                s.query = Q('bool', must=[Q('match', napr=type),
                                          Q('match', **tnved_query_field),
                                          Q('range', period={'gte': date_range[0], 'lt': date_range[1]})])
                s.aggs.metric('stoim', 'sum', field='stoim')
                s.aggs.metric('netto', 'sum', field='netto')
                result = s[:s.count()].execute().aggregations
                label_list.append(i)
                netto_list.append(result['netto']['value'])
                stoim_list.append(result['stoim']['value'])
        context = {
            'labels': label_list,
            'netto': [netto_list, dynamics_list(netto_list)],
            'cost': [stoim_list, dynamics_list(stoim_list)]
        }
        return JsonResponse(context)


class CountryStatistic(APIView):
    def get(self, request):
        def dynamics_list(d):
            res = [0 if d[i] == 0 else int((d[i+1] - d[i])/d[i] * 100) for i in range(len(d)-1)]
            res.insert(0, 0)
            return res
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
        countries = [val['country'] for val in CountryAggregateData.objects.filter(period__range=date_range).values('country').distinct()]
        type = request.query_params.get('category')
        table_country_long = []
        weight_table_data = []
        cost_table_data = []
        chart_data_imp = []
        chart_data_exp = []
        for country in countries:
            aggregate_data = CountryAggregateData.objects.filter(period__range=date_range, country=country).aggregate(
                Sum('imp_sum_cost'), Sum('exp_sum_cost'), Sum('imp_sum_weight'), Sum('exp_sum_weight'))
            chart_data_imp.append([country.lower(), aggregate_data['imp_sum_weight__sum'] if aggregate_data['imp_sum_weight__sum'] else 0])
            chart_data_exp.append([country.lower(), aggregate_data['exp_sum_weight__sum'] if aggregate_data['exp_sum_weight__sum'] else 0])
            table_country_long.append(CountryHandbook.objects.get(country=country).description)
            if type == 'IM':
                weight_table_data.append(aggregate_data['imp_sum_cost__sum'] if aggregate_data['imp_sum_cost__sum'] else 0)
                cost_table_data.append(aggregate_data['imp_sum_weight__sum'] if aggregate_data['imp_sum_weight__sum'] else 0)
            else:
                weight_table_data.append(aggregate_data['exp_sum_cost__sum'] if aggregate_data['exp_sum_cost__sum'] else 0)
                cost_table_data.append(aggregate_data['exp_sum_weight__sum'] if aggregate_data['exp_sum_weight__sum'] else 0)
        context = {
            'table': {
                'labels': table_country_long,
                'netto': [weight_table_data, dynamics_list(weight_table_data)],
                'cost': [cost_table_data, dynamics_list(cost_table_data)]
            },
            'chart': {
                'imp': chart_data_imp,
                'exp': chart_data_exp
            }
        }
        print(context)
        return JsonResponse(context)


# ================= ReportByTnved ================

class TnvedDynamic(APIView):
    def get(self, request):
        def dynamics_list(d):
            res = [0 if d[i] == 0 else int((d[i+1] - d[i])/d[i] * 100) for i in range(len(d)-1)]
            res.insert(0, 0)
            return res
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
        type = request.query_params.get('category')
        params = request.query_params.get('params')
        tnved_list = []
        for i in range(int(request.query_params.get('tnved_list_length'))):
            tnved_list.append(request.query_params.get('tnved_list[%s]' % i))

        chartdata = []
        raw_tabledata_stoim_imp = []
        raw_tabledata_weight_imp = []
        raw_tabledata_stoim_exp = []
        raw_tabledata_weight_exp = []
        for tnved in tnved_list:
            tnved_chart_data = {}
            tnved_chart_data['name'] = tnved
            tnved_data_imp = StatisticData.objects.filter(tnved=tnved, napr='ИМ')
            tnved_data_exp = StatisticData.objects.filter(tnved=tnved, napr='ЭК')
            tnved_data_stoim_exp = []
            tnved_data_weight_exp = []
            tnved_data_stoim_imp = []
            tnved_data_weight_imp = []
            for i in range(len(format_dates_list) - 1):
                tnved_items_imp = tnved_data_imp.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]]).aggregate(
                    Sum('stoim'), Sum('netto'))
                tnved_items_exp = tnved_data_exp.filter(
                    period__range=[format_dates_list[i], format_dates_list[i + 1]]).aggregate(
                    Sum('stoim'), Sum('netto'))
                tnved_data_stoim_exp.append(tnved_items_exp['stoim__sum'])
                tnved_data_weight_exp.append(tnved_items_exp['netto__sum'])

                tnved_data_stoim_imp.append(tnved_items_imp['stoim__sum'])
                tnved_data_weight_imp.append(tnved_items_imp['netto__sum'])

            tnved_data_stoim_exp = [int(i) if i else 0 for i in tnved_data_stoim_exp]
            tnved_data_weight_exp = [int(i) if i else 0 for i in tnved_data_weight_exp]

            tnved_data_stoim_imp = [int(i) if i else 0 for i in tnved_data_stoim_imp]
            tnved_data_weight_imp = [int(i) if i else 0 for i in tnved_data_weight_imp]

            raw_tabledata_stoim_imp.append(tnved_data_stoim_imp)
            raw_tabledata_weight_imp.append(tnved_data_weight_imp)

            raw_tabledata_stoim_exp.append(tnved_data_stoim_exp)
            raw_tabledata_weight_exp.append(tnved_data_weight_exp)

            if type == 'ИМ':
                tnved_chart_data['data'] = tnved_data_stoim_imp if params == 'stoim' else tnved_data_weight_imp

            elif type == 'ЭК':
                tnved_chart_data['data'] = tnved_data_stoim_exp if params == 'stoim' else tnved_data_weight_exp


            chartdata.append(tnved_chart_data)
        tabledata_stoim_imp = [sum(i) for i in zip(*raw_tabledata_stoim_imp)]
        tabledata_weight_imp = [sum(i) for i in zip(*raw_tabledata_weight_imp)]
        tabledata_stoim_exp = [sum(i) for i in zip(*raw_tabledata_stoim_exp)]
        tabledata_weight_exp = [sum(i) for i in zip(*raw_tabledata_weight_exp)]

        label_list = [i.strftime("%Y") if interval == 'year' else i.strftime("%Y-%m") for i in dates_list]
        label_list.pop()
        context = {
            'labels': label_list,
            'chartdata': chartdata,
            'table': {
                'stoim': [tabledata_stoim_imp, dynamics_list(tabledata_stoim_imp)] if type == 'ИМ' else [tabledata_stoim_exp, dynamics_list(tabledata_stoim_exp)],
                'weight': [tabledata_weight_imp, dynamics_list(tabledata_weight_imp)] if type == 'ИМ' else [tabledata_weight_exp, dynamics_list(tabledata_weight_exp)]
            },
            'imp_sum_table': {
                'stoim': sum(tabledata_stoim_imp),
                'weight': sum(tabledata_weight_imp)
            },
            'exp_sum_table': {
                'stoim': sum(tabledata_stoim_exp),
                'weight': sum(tabledata_weight_exp)
            }
        }
        return JsonResponse(context)