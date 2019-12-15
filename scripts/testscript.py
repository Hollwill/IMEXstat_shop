from statistic.models import StatisticData

tnved_values = StatisticData.objects.all().values('tnved').distinct()

