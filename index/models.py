from django.db import models

class Tasks(models.Model):
	title = models.CharField(max_length=200, verbose_name='Заголовок')
	description = models.TextField(verbose_name='Описание')
	url = models.URLField(max_length=200, verbose_name='Url адрес')
	image = models.ImageField(blank=True, null=True, verbose_name='Изображение')

	def __str__(self):
		return self.title
		
	class Meta:
		verbose_name = 'Задачу'
		verbose_name_plural = 'Задачи'



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