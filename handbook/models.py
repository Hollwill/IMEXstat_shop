from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Handbook(MPTTModel):
    name = models.CharField(max_length=200, verbose_name='Название')
    group = models.IntegerField(blank=True, null=True, verbose_name='Код')
    is_link = models.BooleanField(default=False, verbose_name='Это ссылка.')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            on_delete=models.CASCADE, verbose_name='Родитель')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'в справочник'
        verbose_name_plural = 'Справочник'

    class MPTTMeta:
        order_insertion_by = ['name']
