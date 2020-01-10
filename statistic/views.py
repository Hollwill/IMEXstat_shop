from .models import StatisticData, StatisticAggregateData, StatisticDataDocument, CountryAggregateData, CountryHandbook
from django.db.models import Avg, Max, Sum
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date
import pandas as pd
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
from django.db.models import Q as _Q

tnved_dict = {
    2: 'tnved_two',
    4: 'tnved_four',
    6: 'tnved_six',
    8: 'tnved_eight',
    10: 'tnved',
}


class Autocomplete(APIView):
    def get(self, request):
        search = request.query_params.get('q')
        if search:
            values_list = [i['tnved'] for i in
                           StatisticData.objects.filter(tnved__startswith=search).values('tnved').distinct()][:5]
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
        data_objects_list = [
            StatisticAggregateData.objects.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]]) for i
            in range(len(format_dates_list) - 1)]
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


class TurnoverStructure(APIView):
    def get(self, request):
        def dynamics_list(d):
            res = [0 if d[i] == 0 else int((d[i + 1] - d[i]) / d[i] * 100) for i in range(len(d) - 1)]
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
                s.aggs.metric('stoim', 'sum', field='stoim')
                s.aggs.metric('netto', 'sum', field='netto')
                result = s[:s.count()].execute().aggregations
                label_list.append(i)
                netto_list.append(result['netto']['value'])
                stoim_list.append(result['stoim']['value'])
        else:
            tnved_distinct = [i[tnved_dict[len(tnved) + 2]] for i in
                              StatisticData.objects.filter(**{tnved_dict[len(tnved)]: tnved}).values(
                                  tnved_dict[len(tnved) + 2]).distinct()]
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
            res = [0 if d[i] == 0 else int((d[i + 1] - d[i]) / d[i] * 100) for i in range(len(d) - 1)]
            res.insert(0, 0)
            return res

        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
        countries = [val['country'] for val in
                     CountryAggregateData.objects.filter(period__range=date_range).values('country').distinct()]
        type = request.query_params.get('category')
        table_country_long = []
        weight_table_data = []
        cost_table_data = []
        chart_data_imp = []
        chart_data_exp = []
        for country in countries:
            aggregate_data = CountryAggregateData.objects.filter(period__range=date_range, country=country).aggregate(
                Sum('imp_sum_cost'), Sum('exp_sum_cost'), Sum('imp_sum_weight'), Sum('exp_sum_weight'))
            chart_data_imp.append([country.lower(), aggregate_data['imp_sum_weight__sum'] if aggregate_data[
                'imp_sum_weight__sum'] else 0])
            chart_data_exp.append([country.lower(), aggregate_data['exp_sum_weight__sum'] if aggregate_data[
                'exp_sum_weight__sum'] else 0])
            table_country_long.append(CountryHandbook.objects.get(country=country).description)
            if type == 'IM':
                weight_table_data.append(
                    aggregate_data['imp_sum_cost__sum'] if aggregate_data['imp_sum_cost__sum'] else 0)
                cost_table_data.append(
                    aggregate_data['imp_sum_weight__sum'] if aggregate_data['imp_sum_weight__sum'] else 0)
            else:
                weight_table_data.append(
                    aggregate_data['exp_sum_cost__sum'] if aggregate_data['exp_sum_cost__sum'] else 0)
                cost_table_data.append(
                    aggregate_data['exp_sum_weight__sum'] if aggregate_data['exp_sum_weight__sum'] else 0)
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
        return JsonResponse(context)


# ================= ReportByTnved ================

class TnvedDynamic(APIView):
    def get(self, request):
        get = request.query_params.get('get')

        item_list = [request.query_params.get('item_list[%s]' % i)
                     for i in range(int(request.query_params.get('item_list_length')))]
        if get == 'country':
            item_list = [CountryHandbook.objects.get(description=i).country for i in item_list]
        data_list, split_dates = StatisticData.get_statistic_with_split_by_dates(request, item_list)
        interval = request.query_params.get('interval')
        context = {
            'labels': [i.strftime("%Y") if interval == 'year' else i.strftime("%Y-%m") for i in split_dates],
            'data': data_list,
        }
        if get == 'tnved':
            tnved = request.query_params.get('item_list[0]')
            tnved_sliced = tnved[:len(tnved) - 2]
            filter_dict = {tnved_dict[len(tnved_sliced)]: tnved_sliced}
            tnved_extend = StatisticData.objects.filter(**filter_dict).values(tnved_dict[len(tnved)]).distinct()
            tnved_extend_list = [i[tnved_dict[len(tnved)]] for i in tnved_extend]
            tnved_extend_data = []
            for tnved in tnved_extend_list:
                tnved_data = {
                    'item': tnved,
                    'exp': {},
                    'imp': {},
                }
                filter_dict = {tnved_dict[len(tnved)]: tnved}
                str_date_range = [request.query_params.get('date_from') + '-01',
                                  request.query_params.get('date_to') + '-01']
                tnved_agg_imp = StatisticData.objects.filter(period__range=str_date_range, napr='ИМ', **filter_dict
                                                             ).aggregate(Sum('stoim'), Sum('netto'))
                tnved_agg_exp = StatisticData.objects.filter(period__range=str_date_range, napr='ЭК', **filter_dict
                                                             ).aggregate(Sum('stoim'), Sum('netto'))
                tnved_data['imp']['stoim'] = int(tnved_agg_imp['stoim__sum']) if tnved_agg_imp['stoim__sum'] else 0
                tnved_data['imp']['weight'] = int(tnved_agg_imp['netto__sum']) if tnved_agg_imp['netto__sum'] else 0
                tnved_data['exp']['stoim'] = int(tnved_agg_exp['stoim__sum']) if tnved_agg_exp['stoim__sum'] else 0
                tnved_data['exp']['weight'] = int(tnved_agg_exp['netto__sum']) if tnved_agg_exp['netto__sum'] else 0
                tnved_extend_data.append(tnved_data)
            context['tnved_extend_data'] = tnved_extend_data
        return JsonResponse(context)


class CountryReportByTnved(APIView):
    def get(self, request):

        def get_data(request, item_list):
            get = request.query_params.get('get')
            str_date_range = [request.query_params.get('date_from') + '-01',
                              request.query_params.get('date_to') + '-01']
            if get == 'country':
                item_list = [CountryHandbook.objects.get(description=i).country for i in item_list]
            q_objects = _Q()
            for item in item_list:
                if get == 'tnved':
                    filter_dict = {tnved_dict[len(item)]: item}
                elif get == 'country':
                    filter_dict = {'strana': item}
                elif get == 'region':
                    filter_dict = {'region': item}
                q_objects |= _Q(**filter_dict)
            item_data = StatisticData.objects.filter(q_objects, period__range=str_date_range)
            values_list = [i[0] for i in item_data.values_list('strana' if get == 'tnved' else 'tnved_two').distinct()]
            values_list = values_list[:18]
            data = []
            print(len(values_list))
            for value in values_list:
                print(value)
                value_dict = {'exp': {}, 'imp': {}}
                if get == 'tnved':
                    value_dict['item'] = CountryHandbook.objects.get(country=value).description
                    value_dict['item_short'] = value
                    filter_dict = {'strana': value}
                elif get == 'country' or get == 'region':
                    value_dict['item'] = value
                    filter_dict = {'tnved_two': value}
                imp_country_agg = item_data.filter(napr='ИМ', **filter_dict).aggregate(Sum('netto'), Sum('stoim'))
                exp_country_agg = item_data.filter(napr='ЭК', **filter_dict).aggregate(Sum('netto'), Sum('stoim'))
                value_dict['exp']['cost'] = int(exp_country_agg['stoim__sum']) if exp_country_agg['stoim__sum'] else 0
                value_dict['exp']['weight'] = int(exp_country_agg['netto__sum']) if exp_country_agg[
                    'netto__sum'] else 0
                value_dict['imp']['cost'] = int(imp_country_agg['stoim__sum']) if imp_country_agg['stoim__sum'] else 0
                value_dict['imp']['weight'] = int(imp_country_agg['netto__sum']) if imp_country_agg[
                    'netto__sum'] else 0
                data.append(value_dict)
            return data
        item_list = [request.query_params.get('item_list[%s]' % i)
                      for i in range(int(request.query_params.get('item_list_length')))]
        context = {
            'table': get_data(request, item_list),
        }
        context['pie'] = context['table'] if len(item_list) == 1 else get_data(request, [item_list[0]])
        return JsonResponse(context)


class DetailedCountryReportByTnved(APIView):
    def get(self, request):
        get = request.query_params.get('get')
        selected_item = request.query_params.get('item')
        item_list = [request.query_params.get('item_list[%s]' % i)
                      for i in range(int(request.query_params.get('item_list_length')))]
        q_objects = _Q()
        for item in item_list:
            if get == 'tnved':
                filter_dict = {tnved_dict[len(item)]: item}
            elif get == 'country':
                filter_dict = {'strana': item}
            elif get == 'region':
                filter_dict = {'region': item}
            q_objects |= _Q(**filter_dict)
        if get == 'tnved':
            filter_dict = {'strana': selected_item}
        elif get == 'country' or get == 'region':
            filter_dict = {tnved_dict[len(selected_item)]: selected_item}
        selected_item_data = StatisticData.objects.filter(q_objects, **filter_dict)

        split_dates = StatisticData.pd_split_dates_by_inreval(request)
        format_dates_list = [i.strftime("%Y-%m-%d") for i in split_dates]
        country_data = {
            'exp': {},
            'imp': {},
        }
        aggregate_data_imp = [
            selected_item_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ИМ').aggregate(
                Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
        aggregate_data_exp = [
            selected_item_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ЭК', ).aggregate(
                Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
        country_data['imp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_imp]
        country_data['imp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_imp]
        country_data['exp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_exp]
        country_data['exp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_exp]
        context = {
            'labels': format_dates_list,
            'data': country_data,
        }
        return JsonResponse(context)


class RegionReportByTnved(APIView):
    def get(self, request):

        def get_data(request, item_list):
            get = request.query_params.get('get')
            str_date_range = [request.query_params.get('date_from') + '-01',
                              request.query_params.get('date_to') + '-01']
            if get == 'country':
                item_list = [CountryHandbook.objects.get(description=i).country for i in item_list]
            q_objects = _Q()
            for item in item_list:
                if get == 'tnved':
                    filter_dict = {tnved_dict[len(item)]: item}
                elif get == 'country':
                    filter_dict = {'strana': item}
                elif get == 'region':
                    filter_dict = {'region': item}
                q_objects |= _Q(**filter_dict)
            item_data = StatisticData.objects.filter(q_objects, period__range=str_date_range)
            values_list = [i[0] for i in item_data.values_list('region' if get == 'country' or get == 'tnved' else 'strana').distinct()]
            data = []
            values_list = values_list[:18]
            for value in values_list:
                value_dict = {'exp': {}, 'imp': {}}
                if get == 'region':
                    value_dict['item'] = CountryHandbook.objects.get(country=value).description
                else:
                    value_dict['item'] = value
                if get == 'tnved' or get == 'country':
                    filter_dict = {'region': value}
                elif get == 'region':
                    filter_dict = {'strana': value}
                imp_region_agg = item_data.filter(napr='ИМ', **filter_dict).aggregate(Sum('netto'), Sum('stoim'))
                exp_region_agg = item_data.filter(napr='ЭК', **filter_dict).aggregate(Sum('netto'), Sum('stoim'))
                value_dict['exp']['cost'] = int(exp_region_agg['stoim__sum']) if exp_region_agg['stoim__sum'] else 0
                value_dict['exp']['weight'] = int(exp_region_agg['netto__sum']) if exp_region_agg[
                    'netto__sum'] else 0
                value_dict['imp']['cost'] = int(imp_region_agg['stoim__sum']) if imp_region_agg['stoim__sum'] else 0
                value_dict['imp']['weight'] = int(imp_region_agg['netto__sum']) if imp_region_agg[
                    'netto__sum'] else 0
                data.append(value_dict)
            return data
        item_list = [request.query_params.get('item_list[%s]' % i)
                      for i in range(int(request.query_params.get('item_list_length')))]
        context = {
            'table': get_data(request, item_list),
        }
        context['pie'] = context['table'] if len(item_list) == 1 else get_data(request, [item_list[0]])

        return JsonResponse(context)


class DetailedRegionReportByTnved(APIView):
    def get(self, request):
        get = request.query_params.get('get')
        selected_item = request.query_params.get('item')

        item_list = [request.query_params.get('item_list[%s]' % i)
                      for i in range(int(request.query_params.get('item_list_length')))]
        if get == 'country':
            item_list = [CountryHandbook.objects.get(description=i).country for i in item_list]
        q_objects = _Q()
        for item in item_list:
            if get == 'tnved':
                filter_dict = {tnved_dict[len(item)]: item}
            elif get == 'country':
                filter_dict = {'strana': item}
            elif get == 'region':
                filter_dict = {'region': item}
            q_objects |= _Q(**filter_dict)
        if get == 'tnved' or get == 'country':
            filter_dict = {'region': selected_item}
        elif get == 'region':
            filter_dict = {'strana': CountryHandbook.objects.get(description=selected_item).country }
        selected_item_data = StatisticData.objects.filter(q_objects, **filter_dict)
        print(filter_dict)

        split_dates = StatisticData.pd_split_dates_by_inreval(request)
        format_dates_list = [i.strftime("%Y-%m-%d") for i in split_dates]
        region_data = {
            'exp': {},
            'imp': {},
        }
        aggregate_data_imp = [
            selected_item_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ИМ').aggregate(
                Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
        aggregate_data_exp = [
            selected_item_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ЭК', ).aggregate(
                Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
        region_data['imp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_imp]
        region_data['imp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_imp]
        region_data['exp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_exp]
        region_data['exp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_exp]
        context = {
            'labels': format_dates_list,
            'data': region_data,
        }
        return JsonResponse(context)
    # def get(self, request):
    #     region = request.query_params.get('region')
    #     tnved_list = [request.query_params.get('tnved_list[%s]' % i)
    #                   for i in range(int(request.query_params.get('tnved_list_length')))]
    #     q_objects = _Q()
    #     for tnved in tnved_list:
    #         filter_dict = {tnved_dict[len(tnved)]: tnved}
    #         q_objects |= _Q(**filter_dict)
    #     tnved_data = StatisticData.objects.filter(q_objects, region=region)
    # 
    #     split_dates = StatisticData.pd_split_dates_by_inreval(request)
    #     format_dates_list = [i.strftime("%Y-%m-%d") for i in split_dates]
    #     country_data = {
    #         'exp': {},
    #         'imp': {},
    #     }
    #     aggregate_data_imp = [
    #         tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ИМ').aggregate(
    #             Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
    #     aggregate_data_exp = [
    #         tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ЭК', ).aggregate(
    #             Sum(
    #                 'stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
    #     country_data['imp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_imp]
    #     country_data['imp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_imp]
    #     country_data['exp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_exp]
    #     country_data['exp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_exp]
    #     context = {
    #         'labels': format_dates_list,
    #         'data': country_data,
    #     }
    #     return JsonResponse(context)

# ========================  ReportByCountry ==================================================


# class CountryDynamic(APIView):
#     def get(self, request):
#         country_list = [request.query_params.get('country_list[%s]' % i)
#                       for i in range(int(request.query_params.get('country_list_length')))]
#         country_data_list, split_dates = StatisticData.get_country_statistic_with_split_by_dates(request, country_list)
#         interval = request.query_params.get('interval')
#
#         context = {
#             'labels': [i.strftime("%Y") if interval == 'year' else i.strftime("%Y-%m") for i in split_dates],
#             'data': country_data_list,
#         }
#         return JsonResponse(context)
#
#
# class TnvedReportByCountry(APIView):
#     def get(self, request):
#         def get_data(request, country_list):
#             str_date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
#
#             q_objects = _Q()
#             for country in country_list:
#                 q_objects |= _Q(strana=country)
#             country_data = StatisticData.objects.filter(q_objects, period__range=str_date_range)
#             tnved_list = [i[0] for i in country_data.values_list('tnved_two').distinct()]
#             data = []
#             for tnved in tnved_list:
#                 tnved_dict = {'tnved': tnved, 'exp': {}, 'imp': {}}
#                 imp_tnved_agg = country_data.filter(napr='ИМ', tnved_two=tnved).aggregate(Sum('netto'), Sum('stoim'))
#                 exp_tnved_agg = country_data.filter(napr='ЭК', tnved_two=tnved).aggregate(Sum('netto'), Sum('stoim'))
#                 tnved_dict['exp']['cost'] = int(exp_tnved_agg['stoim__sum']) if exp_tnved_agg['stoim__sum'] else 0
#                 tnved_dict['exp']['weight'] = int(exp_tnved_agg['netto__sum']) if exp_tnved_agg['netto__sum'] else 0
#                 tnved_dict['imp']['cost'] = int(imp_tnved_agg['stoim__sum']) if imp_tnved_agg['stoim__sum'] else 0
#                 tnved_dict['imp']['weight'] = int(imp_tnved_agg['netto__sum']) if imp_tnved_agg['netto__sum'] else 0
#                 data.append(tnved_dict)
#             return data
#         country_list = [request.query_params.get('country_list[%s]' % i)
#                       for i in range(int(request.query_params.get('country_list_length')))]
#         context = {
#             'table': get_data(request, country_list),
#             'pie': get_data(request, [country_list[0]])
#         }
#         return JsonResponse(context)
#
#
# class DetailedTnvedReportByCountry(APIView):
#     def get(self, request):
#         country = request.query_params.get('country')
#         tnved_list = [request.query_params.get('tnved_list[%s]' % i)
#                       for i in range(int(request.query_params.get('tnved_list_length')))]
#         q_objects = _Q()
#         for tnved in tnved_list:
#             filter_dict = {tnved_dict[len(tnved)]: tnved}
#             q_objects |= _Q(**filter_dict)
#         tnved_data = StatisticData.objects.filter(q_objects, strana=country)
#
#         split_dates = StatisticData.pd_split_dates_by_inreval(request)
#         format_dates_list = [i.strftime("%Y-%m-%d") for i in split_dates]
#         country_data = {
#             'exp': {},
#             'imp': {},
#         }
#         aggregate_data_imp = [
#             tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ИМ').aggregate(
#                 Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
#         aggregate_data_exp = [
#             tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ЭК',).aggregate(Sum(
#                 'stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
#         country_data['imp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_imp]
#         country_data['imp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_imp]
#         country_data['exp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_exp]
#         country_data['exp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_exp]
#         context = {
#             'labels': format_dates_list,
#             'data': country_data,
#         }
#         return JsonResponse(context)
#
#
# class RegionReportByCountry(APIView):
#     def get(self, request):
#         def get_data(request, tnved_list):
#             print(tnved_list)
#             str_date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']
#
#             q_objects = _Q()
#             for tnved in tnved_list:
#                 filter_dict = {tnved_dict[len(tnved)]: tnved}
#                 q_objects |= _Q(**filter_dict)
#             tnved_data = StatisticData.objects.filter(q_objects, period__range=str_date_range)
#             region_list = [i[0] for i in tnved_data.values_list('region').distinct()]
#             data = []
#             for region in region_list:
#                 country_dict = {'region': region, 'exp': {}, 'imp': {}}
#                 imp_country_agg = tnved_data.filter(napr='ИМ', region=region).aggregate(Sum('netto'), Sum('stoim'))
#                 exp_country_agg = tnved_data.filter(napr='ЭК', region=region).aggregate(Sum('netto'), Sum('stoim'))
#                 country_dict['exp']['cost'] = int(exp_country_agg['stoim__sum']) if exp_country_agg['stoim__sum'] else 0
#                 country_dict['exp']['weight'] = int(exp_country_agg['netto__sum']) if exp_country_agg['netto__sum'] else 0
#                 country_dict['imp']['cost'] = int(imp_country_agg['stoim__sum']) if imp_country_agg['stoim__sum'] else 0
#                 country_dict['imp']['weight'] = int(imp_country_agg['netto__sum']) if imp_country_agg['netto__sum'] else 0
#                 data.append(country_dict)
#             return data
#         tnved_list = [request.query_params.get('tnved_list[%s]' % i)
#                       for i in range(int(request.query_params.get('tnved_list_length')))]
#         context = {
#             'table': get_data(request, tnved_list),
#             'pie': get_data(request, [tnved_list[0]])
#         }
#         return JsonResponse(context)
#
#
# class DetailedRegionReportByCountry(APIView):
#     def get(self, request):
#         region = request.query_params.get('region')
#         tnved_list = [request.query_params.get('tnved_list[%s]' % i)
#                       for i in range(int(request.query_params.get('tnved_list_length')))]
#         q_objects = _Q()
#         for tnved in tnved_list:
#             filter_dict = {tnved_dict[len(tnved)]: tnved}
#             q_objects |= _Q(**filter_dict)
#         tnved_data = StatisticData.objects.filter(q_objects, region=region)
#
#         split_dates = StatisticData.pd_split_dates_by_inreval(request)
#         format_dates_list = [i.strftime("%Y-%m-%d") for i in split_dates]
#         country_data = {
#             'exp': {},
#             'imp': {},
#         }
#         aggregate_data_imp = [
#             tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ИМ').aggregate(
#                 Sum('stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
#         aggregate_data_exp = [
#             tnved_data.filter(period__range=[format_dates_list[i], format_dates_list[i + 1]], napr='ЭК',).aggregate(Sum(
#                 'stoim'), Sum('netto')) for i in range(len(format_dates_list) - 1)]
#         country_data['imp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_imp]
#         country_data['imp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_imp]
#         country_data['exp']['cost'] = [int(i['stoim__sum']) if i['stoim__sum'] else 0 for i in aggregate_data_exp]
#         country_data['exp']['weight'] = [int(i['netto__sum']) if i['netto__sum'] else 0 for i in aggregate_data_exp]
#         context = {
#             'labels': format_dates_list,
#             'data': country_data,
#         }
#         return JsonResponse(context)
