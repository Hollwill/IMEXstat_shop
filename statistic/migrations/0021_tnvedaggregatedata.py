# Generated by Django 2.2.5 on 2019-12-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0020_auto_20191223_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnvedAggregateData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tnved', models.CharField(db_index=True, max_length=10)),
                ('imp_sum_cost', models.BigIntegerField(verbose_name='Импорт - суммарная стоимость')),
                ('exp_sum_cost', models.BigIntegerField(verbose_name='Экспорт - суммарная стоимость')),
                ('imp_sum_weight', models.BigIntegerField(verbose_name='Импорт - суммарный вес')),
                ('exp_sum_weight', models.BigIntegerField(verbose_name='Экспорт - суммарный вес')),
            ],
        ),
    ]