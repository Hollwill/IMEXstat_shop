from django.db import models
from ckeditor.fields import RichTextField
from solo.models import SingletonModel


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


class Contacts(SingletonModel):
	fax = models.CharField(max_length=255, blank=True, null=True, verbose_name="Факс")
	fax_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Факс ссылка")
	email = models.CharField(max_length=255, blank=True, null=True, verbose_name='E-mail')
	INN = models.CharField(max_length=255, blank=True, null=True, verbose_name='ИНН')
	OGRN = models.CharField(max_length=255, blank=True, null=True, verbose_name='ОГРН')
	KPP = models.CharField(max_length=255, blank=True, null=True, verbose_name='КПП')

	class Meta:
		verbose_name = "Контакты"


class ContactsPhone(models.Model):
	contacts = models.ForeignKey(Contacts, related_name='phones', on_delete=models.CASCADE)
	number = models.CharField(max_length=255, verbose_name='Номер телефона')
	number_link = models.CharField(max_length=255, default='', verbose_name='ссылка')

	def __str__(self):
		return self.number

	class Meta:
		verbose_name = "Телефонный номер"
		verbose_name_plural = "Телефонные номера"

class ContactsOffice(models.Model):
	contacts = models.ForeignKey(Contacts, related_name='offices', blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Название")
	address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Адрес")
	map_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ссылка карты")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Офис"
		verbose_name_plural = "Офисы"


class ContactsOfficeImage(models.Model):
	office = models.ForeignKey(ContactsOffice, related_name='images', on_delete=models.CASCADE)
	img = models.ImageField(verbose_name="Изображение")

	class Meta:
		verbose_name = "Изображение"
		verbose_name_plural = "Изображения"


class ContactsTeam(models.Model):
	contacts = models.ForeignKey(Contacts, related_name='team_members', blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
	img = models.ImageField(verbose_name="Изображение")
	job = models.CharField(max_length=255, blank=True, null=True, verbose_name="Должность")
	description = models.TextField(verbose_name="Описание")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Член команды"
		verbose_name_plural = "Члены команды"
