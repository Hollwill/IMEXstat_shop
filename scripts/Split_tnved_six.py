import pickle
from statistic.models import StatisticData

with open('statistic_data_2_to_4.txt', 'rb') as f:
    values_list = pickle.load(f)



six_values = []
a = len(values_list[1])
for value in values_list[1]:
    six_values.extend([i['split_tnved__six']for i in StatisticData.objects.filter(split_tnved__four=value).values('split_tnved__six').distinct()])
    a -= 1
    print(a)

with open('statistic_data_6.txt', 'wb') as f:
    pickle.dump(six_values, f)