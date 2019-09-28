from django.db import models

from products.models import Research
from personal_cabinet.models import Client
from django.db.models import Sum
from decimal import Decimal

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

class Cart(models.Model):
    research = models.ManyToManyField(Research, verbose_name='Исследование', blank=True)
    client = models.OneToOneField(Client, on_delete=models.CASCADE, verbose_name='Клиент')

    @property
    def summary(self):
        research = Research.objects.filter(cart__client=self.client)
        count = research.aggregate(Sum('OM_cost'))
        return count.get('OM_cost__sum')
    
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