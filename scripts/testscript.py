from statistic.models import StatisticData
from django.db.models import Avg, Max

tnved_values = StatisticData.objects.all().values('split_tnved__2').distinct()

for value in tnved_values:
    StatisticData.objects.filter(tnved=value)