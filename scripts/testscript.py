from statistic.models import StatisticData, TnvedHandbook
from django.db.models import Avg, Max, Sum
from datetime import datetime
split_tnved_dict = {
    2: 'two',
    4: 'four',
    6: 'six',
    8: 'eight',
    10: 'ten',
}

def run():
    imp_data = StatisticData.objects.filter(napr='ИМ')
    exp_data = StatisticData.objects.filter(napr='ЭК')
    for object in TnvedHandbook.objects.all().values_list('tnved').reverse():
        a = datetime.now()
        filter_dict = {'split_tnved__' + split_tnved_dict[len(object[0])]: object[0]}
        ag_imp_data = imp_data.filter(**filter_dict).aggregate(Sum('stoim'), Sum('netto'))
        ag_exp_data = exp_data.filter(**filter_dict).aggregate(Sum('stoim'), Sum('netto'))
        print(exp_data.filter(**filter_dict).query)
        print(datetime.now() - a)
        print(ag_imp_data)
        print(ag_exp_data)

