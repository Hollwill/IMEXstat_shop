# Generated by Django 2.2.5 on 2019-12-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_products_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='priority',
            field=models.IntegerField(default=1, verbose_name='Приоритет'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='tasks',
            order_with_respect_to='priority',
        ),
    ]