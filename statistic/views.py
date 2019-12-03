from .models import StatisticData
from django.db.models import Avg, Max
from django.http import JsonResponse
from rest_framework.views import APIView
from datetime import date
from dateutil.relativedelta import relativedelta
import copy


class MarketSummary(APIView):
    def get(self, request):
        date_range = [request.query_params.get('date_from') + '-01', request.query_params.get('date_to') + '-01']

        imp_data = StatisticData.objects.filter(napr='ИМ', period__range=date_range)
        exp_data = StatisticData.objects.filter(napr='ЭК', period__range=date_range)


        imp_cost = int(imp_data.aggregate(Avg('stoim'))['stoim__avg'])
        imp_weight = int(imp_data.aggregate(Avg('netto'))['netto__avg'])
        imp_country = imp_data.values('strana').distinct().count()
        imp_max_stoim = imp_data.filter(tnved__regex=r'\d+').aggregate(Max('stoim'))['stoim__max']
        imp_tnved = imp_data.get(stoim=imp_max_stoim).tnved

        exp_cost = int(exp_data.aggregate(Avg('stoim'))['stoim__avg'])
        exp_weight = int(exp_data.aggregate(Avg('netto'))['netto__avg'])
        exp_country = exp_data.values('strana').distinct().count()
        exp_max_stoim = exp_data.filter(tnved__regex=r'\d+').aggregate(Max('stoim'))['stoim__max']
        exp_tnved = exp_data.get(stoim=exp_max_stoim).tnved

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
        def datasets_fragment(data_list1, data_list2):
            return [
                {
                    'label': 'Импорт',
                    'backgroundColor': '#FFF839',
                    'data': data_list1
                },
                {
                    'label': 'Экспорт',
                    'backgroundColor': '#1221FF',
                    'data': data_list2
                }
            ]

        def aggregate_years(item, items_param, year):
            # Todo: переделать функцию
            return int(item.filter(period__range=[date_range[0].strftime('%Y-01-%d'), '%s-%s' % (str(year) + '-01',  date_range[1].strftime('%d'))]).aggregate(Avg(items_param))[items_param + '__avg'])
        interval = request.query_params.get('interval')
        # берем строку даты в url параметрах
        date_range = [request.query_params.get('date_from'), request.query_params.get('date_to')]
        # делаем строку объектом даты
        date_range = [date(int(a[:4]), int(a[5:7]), 0o01) for a in date_range]
        imp_data = StatisticData.objects.filter(napr='ИМ')
        exp_data = StatisticData.objects.filter(napr='ЭК')
        # согласно заданному интервалу, выдаем соответствующие данные
        if interval == 'year':
            label_list = [date_range[1].year - i for i in reversed(range(date_range[1].year - date_range[0].year + 1))]
            imp_cost_list = [aggregate_years(imp_data, 'stoim', i) for i in label_list]
            exp_cost_list = [aggregate_years(exp_data, 'stoim', i) for i in label_list]
            imp_weight_list = [aggregate_years(imp_data, 'netto', i) for i in label_list]
            exp_weight_list = [aggregate_years(exp_data, 'netto', i) for i in label_list]
        elif interval == 'quartal' or interval == 'month':
            label_list = []
            current_time = copy.deepcopy(date_range[1])
            # делаем список согласно выбранному интервалу из заданного промежутка
            while date_range[0] <= current_time:
                label_list.insert(0, current_time.strftime("%Y-%m"))
                current_time = current_time - relativedelta(months=3 if interval == 'quartal' else 1)
            # Если начальная дата не входит в список, то добавляем ее
            label_list.insert(0, date_range[0].strftime('%Y-%m')) if not label_list[0] == date_range[0].strftime('%Y-%m') else None
            imp_data_list = []
            exp_data_list = []
            # берем из базы данных объекты согласно заданному интервалу
            for i in range(len(label_list) - 1):
                imp_data_list.append(imp_data.filter(period__range=[label_list[i] + '-01', label_list[i + 1] + '-01']))
                exp_data_list.append(exp_data.filter(period__range=[label_list[i] + '-01', label_list[i + 1] + '-01']))
            label_list.pop(0)
            # считаем нужные данные исходя из выбранных записей.
            imp_cost_list = [int(a.aggregate(Avg('stoim'))['stoim__avg']) for a in imp_data_list]
            exp_cost_list = [int(a.aggregate(Avg('stoim'))['stoim__avg']) for a in exp_data_list]
            imp_weight_list = [int(a.aggregate(Avg('netto'))['netto__avg']) for a in imp_data_list]
            exp_weight_list = [int(a.aggregate(Avg('netto'))['netto__avg']) for a in exp_data_list]

        context = {
            'chart': {
                'cost': {
                    'chartdata': {
                        'labels': label_list,
                        'datasets': datasets_fragment(imp_cost_list, exp_cost_list)
                    }
                },
                'netto': {
                    'chartdata': {
                        'labels': label_list,
                        'datasets': datasets_fragment(imp_weight_list, exp_weight_list)
                    }

                }
            }
        }
        return JsonResponse(context)
# TODO: сделать на фронте обработку нетто и стоимости без лишнего запроса