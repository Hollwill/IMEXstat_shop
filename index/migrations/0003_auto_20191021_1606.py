# Generated by Django 2.2.5 on 2019-10-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='cost',
            field=models.IntegerField(max_length=100, verbose_name='Цена'),
        ),
    ]