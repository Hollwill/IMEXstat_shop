# Generated by Django 2.2.5 on 2019-09-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_cabinet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
