from django.db import models
from project.personal_cabinet.models import Client

class Research(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    clients = models.ManyToManyField(Client, on_delete=models.PROTECT)

class Category(models.Model):
    title = models.CharField(max_length=50)
