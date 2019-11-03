# Generated by Django 2.2.5 on 2019-11-03 02:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20191031_1430'),
        ('orders', '0003_auto_20191030_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='research',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_frequency', models.CharField(blank=True, choices=[('MU', 'Ежемесячное обновление'), ('QU', 'Ежеквартальное обновление')], max_length=2, null=True, verbose_name='частота обновления')),
                ('duration', models.CharField(blank=True, choices=[('OM', 'На один месяц'), ('OQ', 'На один квартал'), ('HY', 'На пол года'), ('OY', 'На один год')], max_length=2, null=True, verbose_name='подписка')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='стоимость')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Cart', verbose_name='Корзина')),
                ('research', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Research', verbose_name='Исследование')),
            ],
            options={
                'verbose_name': 'Исследование',
                'verbose_name_plural': 'Исследования',
            },
        ),
    ]