from django.db import models
from django.contrib.auth.models import User



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='Nickname')
    firstname = models.CharField(max_length=50, blank=True, verbose_name='Имя')
    lastname = models.CharField(max_length=50, blank=True, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=50, blank=True, verbose_name='Мобильный телефон')
    firm_name = models.CharField(max_length=100, blank=True, verbose_name='Название фирмы')
    legal_adress = models.CharField(max_length=100, blank=True, verbose_name='Юридический адрес')
    INN = models.IntegerField(blank=True, null=True, verbose_name='ИНН')
    KPP = models.IntegerField(blank=True, null=True, verbose_name='КПП')
    requisites_file = models.FileField(blank=True, verbose_name='Файл с реквизитами')

    def __str__(self):
        return self.firstname + ' ' + self.lastname + self.user.username

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
