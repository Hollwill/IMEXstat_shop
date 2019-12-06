from django.db import models
from ckeditor.fields import RichTextField


class Tasks(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	description = RichTextField(verbose_name='Описание')
	url = models.URLField(max_length=200, verbose_name='Url адрес')
	image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
	priority = models.IntegerField(default=1, verbose_name='Приоритет')

	def __str__(self):
		return self.title
		
	class Meta:
		verbose_name = 'Задачу'
		verbose_name_plural = 'Задачи'
		order_with_respect_to = 'priority'


class Products(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название')
	description = models.TextField(max_length=87, null=True, verbose_name='Описание')
	image = models.ImageField(blank=True, null=True, verbose_name='Изображение')
	cost = models.CharField(max_length=200, blank=True, null=True, verbose_name='Цена')
	url = models.CharField(max_length=200, verbose_name='Url адрес')

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Products, self).save()
		if self.cost == '0':
			self.cost = 'Бесплатно'

	class Meta:
		verbose_name = 'Продукт'
		verbose_name_plural = 'Продукты'


class Feedback(models.Model):
	name = models.CharField(max_length=200, verbose_name='Имя')
	contact_details = models.CharField(max_length=200, verbose_name='Контактные данные')
	date = models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Обратная связь'
		verbose_name_plural = "Обратная связь"


class ClientsImages(models.Model):
	name = models.CharField(max_length=200, verbose_name='Клиент')
	image = models.ImageField(verbose_name='Изображение')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Клиент'
		verbose_name_plural = "Наши клиенты"


class MenuManagement(models.Model):
	title = models.CharField(max_length=200, verbose_name='Пункт')
	url = models.CharField(max_length=200, verbose_name='Url адрес')
	priority = models.IntegerField(verbose_name='очередность')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Пункт меню'
		verbose_name_plural = 'Пункты меню'
