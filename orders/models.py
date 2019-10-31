from django.db import models

from products.models import Research
from personal_cabinet.models import Client
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField


class Order(models.Model):
    client = models.ForeignKey(Client, blank=True, null=True, on_delete=models.PROTECT, verbose_name='Клиент')
    firstname = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    lastname = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='Мобильный телефон')
    firm_name = models.CharField(max_length=100, blank=True, verbose_name='Название фирмы')
    INN = models.IntegerField(blank=True, null=True, verbose_name='ИНН')
    KPP = models.IntegerField(blank=True, null=True, verbose_name='КПП')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    paid = models.BooleanField(verbose_name='Оплачен', default=False)

    def save(self, *args, **kwargs):
        if self.client:
            self.firstname = self.client.firstname
            self.lastname = self.client.lastname
            self.email = self.client.email
            self.phone = self.client.phone
            self.firm_name = self.client.firm_name
            self.INN = self.client.INN
            self.KPP = self.client.KPP
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.client:
            return self.client.user.username
        else:
            return self.firstname

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        get_latest_by = 'id'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    get_total_cost.short_description = u'Полная стоимость'


class OrderItem(models.Model):
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
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    research = models.ForeignKey(Research, related_name='order_items', on_delete=models.CASCADE, verbose_name='Исследования')
    update_frequency = models.CharField(max_length=2, choices=UPDATE_FREQUENCY_CHOICES, verbose_name='частота обновления')
    duration = models.CharField(max_length=2, choices=DURATION_CHOICES, verbose_name='подписка')
    price = models.IntegerField(blank=True, null=True, verbose_name='стоимость')

    def save(self, *args, **kwargs):
        if self.update_frequency == 'MU':
            if self.duration == 'OM':
                self.price = self.research.M_OM_cost
            elif self.duration == 'OQ':
                self.price = self.research.M_OQ_cost
            elif self.duration == 'HY':
                self.price = self.research.M_HY_cost
            elif self.duration == 'OY':
                self.price = self.research.M_OY_cost
        elif self.update_frequency == 'QU':
            if self.duration == 'OM':
                self.price = self.research.Q_OM_cost
            elif self.duration == 'OQ':
                self.price = self.research.Q_OQ_cost
            elif self.duration == 'HY':
                self.price = self.research.Q_HY_cost
            elif self.duration == 'OY':
                self.price = self.research.Q_OY_cost
        if self.research.stock:
            self.price = int(self.price - (self.price * self.research.discount / 100))
        super(OrderItem, self).save(*args, **kwargs)

    def get_cost(self):
        return self.price

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'

    def __str__(self):
        return ''


class Cart(models.Model):
    research = models.ManyToManyField(Research, verbose_name='Исследование', blank=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    @property
    def summary(self):
        research = Research.objects.filter(cart__client=self.client)
        count = research.aggregate(Sum('nominal'))
        return count.get('nominal__sum')

    def __str__(self):
        return 'корзина'
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
