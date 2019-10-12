from django.db import models
from personal_cabinet.models import Client
from pytils.translit import slugify

from ckeditor.fields import RichTextField


class Research(models.Model):
    TYPE_RESEARCH_CHOICE = [
        ('industry', 'Отраслевое'),
        ('export', 'Экспорт'),
        ('import', 'Импорт')
    ]
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    target = models.TextField(blank=True, null=True, verbose_name='Цель исследования')
    description = models.TextField(blank=True, null=True, verbose_name='Описание исследования')
    data_update = models.TextField(blank=True, null=True, verbose_name='Обновление данных')
    image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
    demo = models.FileField(blank=True, null=True, verbose_name='Демо файл')
    contents = RichTextField(blank=True, null=True, verbose_name='Оглавление')
    using_methods = RichTextField(blank=True, null=True, verbose_name='Используемые методы')
    data_sources = RichTextField(blank=True, null=True, verbose_name='Источники данных')
    research_type = models.CharField(max_length=10, choices=TYPE_RESEARCH_CHOICE, verbose_name='Тип исследования')
    OM_cost = models.IntegerField(verbose_name='цена за месяц')
    OQ_cost = models.IntegerField(blank=True, null=True, verbose_name='цена за квартал')
    HY_cost = models.IntegerField(blank=True, null=True, verbose_name='цена за полгода')
    OY_cost = models.IntegerField(blank=True, null=True, verbose_name='цена за год')
    slug = models.SlugField(unique=True, blank=True)

    def save(self):
        super(Research, self).save()
        if not self.slug.endswith('-' + str(self.id)):
            self.slug += '-' + str(self.id)
            super(Research, self).save()
    


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ' Исследование'
        verbose_name_plural = 'Исследования'


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
