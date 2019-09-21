from django.db import models
from personal_cabinet.models import Client

class Research(models.Model):
    TYPE_RESEARCH_CHOICE = [
        ('OTR', 'Отраслевое'),
        ('EXP', 'Экспорт'),
        ('IMP', 'Импорт')
    ]
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    target = models.TextField()
    description = models.TextField()
    data_update = models.TextField()
    image = models.ImageField()
    demo = models.FileField()
    contents = models.TextField()
    using_methods = models.TextField()
    data_sources = models.TextField()
    research_type = models.CharField(max_length=3, choices=TYPE_RESEARCH_CHOICE)
    OM_cost = models.IntegerField()
    OQ_cost = models.IntegerField()
    HY_cost = models.IntegerField()
    OY_cost = models.IntegerField()
    


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ' Исследование'
        verbose_name_plural = 'Исследования'


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
