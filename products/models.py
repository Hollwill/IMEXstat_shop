from django.db import models

from pytils.translit import slugify

from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeForeignKey as TreeKey


class Research(models.Model):
    TYPE_RESEARCH_CHOICE = [
        ('industry', 'Отраслевое'),
        ('export', 'Экспорт'),
        ('import', 'Импорт')
    ]
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    category = TreeKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    target = RichTextField(blank=True, null=True, verbose_name='Цель исследования')
    description = RichTextField(blank=True, null=True, verbose_name='Описание исследования')
    data_update = RichTextField(blank=True, null=True, verbose_name='Обновление данных')
    extra = models.TextField(blank=True, null=True, default=' ', verbose_name='Дополнительно')
    extra_red = models.TextField(blank=True, null=True, default=' ', verbose_name='Дополнительно*')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    demo = models.FileField(blank=True, null=True, verbose_name='Демо файл')
    contents = RichTextField(blank=True, null=True, verbose_name='Структура исследования')
    using_methods = RichTextField(blank=True, null=True, verbose_name='Используемые методы')
    data_sources = RichTextField(blank=True, null=True, verbose_name='Источники данных')
    research_type = models.CharField(max_length=10, choices=TYPE_RESEARCH_CHOICE, verbose_name='Тип исследования')
    nominal = models.IntegerField(verbose_name='Номинальная цена', default=1)
    M_OM_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежемесячное обновление - На один месяц')
    M_OQ_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежемесячное обновление - На один квартал')
    M_HY_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежемесячное обновление - На пол года')
    M_OY_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежемесячное обновление - На один год')
    # Q_OM_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежеквартальное обновление - На один месяц')
    Q_OQ_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежеквартальное обновление - На один квартал')
    Q_HY_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежеквартальное обновление - На пол года')
    Q_OY_cost = models.IntegerField(blank=True, null=True, verbose_name='Ежеквартальное обновление - На один год')
    stock = models.BooleanField(default=False, verbose_name='Акция')
    discount = models.IntegerField(default=0, choices=[(i, i) for i in range(0, 101)], verbose_name='Скидка')

    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super(Research, self).save()
        if not self.slug.endswith('-' + str(self.id)):
            self.slug += '-' + str(self.id)
            super(Research, self).save()

    def only_nominal(self):
        if self.M_OM_cost or self.M_OQ_cost or self.M_HY_cost or self.M_OY_cost or \
                self.Q_OQ_cost or self.M_HY_cost or self.Q_OY_cost:
            return False
        else:
            return True

    def get_discount_cost(self, value):
        return int(value - (value * self.discount / 100))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ' Исследование'
        verbose_name_plural = 'Исследования'


class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='Родитель')

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['title']


class IndividualResearchFeedback(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    contact_details = models.CharField(max_length=200, verbose_name='Контактные данные')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Исследование на заказ'
        verbose_name_plural = "Исследования на заказ"



