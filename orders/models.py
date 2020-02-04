from django.db import models
from products.models import Research
from personal_cabinet.models import Client
from django.db.models import Sum
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

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
            # if self.duration == 'OM':
            #     self.price = self.research.Q_OM_cost
            if self.duration == 'OQ':
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


# class Cart(models.Model):
#     client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Клиент')
#
#     def summary(self):
#         cart_item = CartItem.objects.filter(cart=self)
#         count = cart_item.aggregate(Sum('price'))
#         return count.get('price__sum')
#
#     def __str__(self):
#         return 'корзина'
#
#     class Meta:
#         verbose_name = 'Корзина'
#         verbose_name_plural = 'Корзина'
#
#
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, blank=True, null=True, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
#     research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name='Исследование')
#     update_frequency = models.CharField(blank=True, null=True, max_length=2, choices=UPDATE_FREQUENCY_CHOICES,
#                                         verbose_name='частота обновления')
#     duration = models.CharField(blank=True, null=True, max_length=2, choices=DURATION_CHOICES, verbose_name='подписка')
#     price = models.IntegerField(blank=True, null=True, verbose_name='стоимость')
#
#     def save(self, *args, **kwargs):
#         if not (self.update_frequency and self.duration):
#             self.price = self.research.nominal
#         else:
#             for u_choice in self._meta.get_field('update_frequency').choices:
#                 if self.update_frequency == u_choice[0]:
#                     for d_choice in  self._meta.get_field('duration').choices:
#                         if self.duration == d_choice[0]:
#                             self.price = getattr(self.research, '{0}_{1}_cost'.format(u_choice[0][0], d_choice[0]))
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return self.research.title
#
#     class Meta:
#         verbose_name = 'Исследование'
#         verbose_name_plural = 'Исследования'
#         get_latest_by = 'id'


class Cart(models.Model):
    client = models.OneToOneField(Client, blank=True, null=True, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(verbose_name='creation date', auto_now_add=True)

    class Meta:
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-creation_date',)

    def __str__(self):
        return str(self.creation_date)

    def summary_price(self):
        product = CartItem.objects.filter(cart=self)
        count = product.aggregate(Sum('price'))
        return count.get('price__sum')
    price = property(summary_price)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, blank=True, null=True, verbose_name='cart', on_delete=models.CASCADE)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, verbose_name='Исследование')
    update_frequency = models.CharField(blank=True, null=True, max_length=2, choices=UPDATE_FREQUENCY_CHOICES,
                                        verbose_name='частота обновления')
    duration = models.CharField(blank=True, null=True, max_length=2, choices=DURATION_CHOICES, verbose_name='подписка')
    price = models.IntegerField(blank=True, null=True, verbose_name='стоимость')

    def save(self, *args, **kwargs):
        if not (self.update_frequency and self.duration):
            self.price = self.research.nominal
        else:
            for u_choice in self._meta.get_field('update_frequency').choices:
                if self.update_frequency == u_choice[0]:
                    for d_choice in self._meta.get_field('duration').choices:
                        if self.duration == d_choice[0]:
                            self.price = getattr(self.research, '{0}_{1}_cost'.format(u_choice[0][0], d_choice[0]))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.research.title

    class Meta:
        verbose_name = 'Исследование'
        verbose_name_plural = 'Исследования'
        get_latest_by = 'id'