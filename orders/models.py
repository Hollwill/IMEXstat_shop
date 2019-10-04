from django.db import models

from products.models import Research
from personal_cabinet.models import Client
from django.db.models import Sum
from decimal import Decimal

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Клиент')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    paid = models.BooleanField(verbose_name='Оплачен', default=False)

    def __str__(self):
        return self.client.user.username

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
        if self.duration == 'OM':
            self.price = self.research.OM_cost
        elif self.duration == 'OQ':
            self.price = self.research.OQ_cost
        elif self.duration == 'HY':
            self.price = self.research.HY_cost
        elif self.duration == 'OY':
            self.price = self.research.OY_cost

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
        count = research.aggregate(Sum('OM_cost'))
        return count.get('OM_cost__sum')

    def __str__(self):
        return 'корзина'
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
    
    
'''    
class SessionCart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart
    

    def add(self, research):
        research_id = research.id
        if research_id not in self.cart:
            self.cart[research_id] = {'OM_cost': str(research.OM_cost)}
        self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, research):
        research_id = str(research.id)
        if research_id in self.cart:
            del self.cart[research_id]
            self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        research = Research.objects.filter(id__in=product_ids)
        for research in research:
            self.cart[str(research.id)]['research'] = research

        for item in self.cart.values():
            item['OM_cost'] = Decimal(item['OM_cost'])
            yield item

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['OM_cost']) for item in
                   self.cart.values())
'''