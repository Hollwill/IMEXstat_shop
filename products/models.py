from django.db import models
from personal_cabinet.models import Client
from pytils.translit import slugify
class Research(models.Model):
    TYPE_RESEARCH_CHOICE = [
        ('industry', 'Отраслевое'),
        ('export', 'Экспорт'),
        ('import', 'Импорт')
    ]
    title = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    target = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    data_update = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    demo = models.FileField(blank=True, null=True)
    contents = models.TextField(blank=True, null=True)
    using_methods = models.TextField(blank=True, null=True)
    data_sources = models.TextField(blank=True, null=True)
    research_type = models.CharField(max_length=10, choices=TYPE_RESEARCH_CHOICE)
    OM_cost = models.IntegerField()
    OQ_cost = models.IntegerField(blank=True, null=True)
    HY_cost = models.IntegerField(blank=True, null=True)
    OY_cost = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def get_absolute_url(self):
        return reverse('settings', args=(self.slug,))

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
    title = models.CharField(max_length=50)
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
