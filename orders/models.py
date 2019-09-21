from django.db import models
from personal_cabinet.models import Client
from products.models import Research


class Order(models.Model):
    UPDATE_FREQUENCY_CHOICES = [
        ('MU', 'Ежемесячное обновление'),
        ('QU', 'Ежеквартальное обновление')
    ]
    DURATION_CHOICES = [
        ('OM', 'На один месяц'),
        ('OQ', 'На один квартал'),
        ('HY', 'На пол года'),
        ('OY', 'На один год')
    ]
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    research = models.ForeignKey(Research, on_delete=models.PROTECT, verbose_name='Исследование')
    update_frequency = models.CharField(max_length=2, choices=UPDATE_FREQUENCY_CHOICES, verbose_name='частота обновления')
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES, verbose_name='подписка')
    date = models.DateTimeField(auto_now_add=True)
    cost = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.duration == 'OM':
            self.cost = self.research.OM_cost
        elif self.duration == 'OQ':
            self.cost = self.research.OQ_cost
        elif self.duration == 'HY':
            self.cost = self.research.HY_cost
        elif self.duration == 'OY':
            self.cost = self.research.OY_cost

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.research.title + ' ' + self.client.firstname

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


