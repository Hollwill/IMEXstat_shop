# Generated by Django 2.2.5 on 2020-01-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0029_auto_20200104_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statisticdata',
            name='edizm',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='statisticdata',
            name='kol',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='statisticdata',
            name='netto',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='statisticdata',
            name='stoim',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=22, null=True),
        ),
    ]