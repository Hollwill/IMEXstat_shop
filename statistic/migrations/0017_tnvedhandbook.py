# Generated by Django 2.2.5 on 2019-12-19 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0016_auto_20191216_0717'),
    ]

    operations = [
        migrations.CreateModel(
            name='TnvedHandbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tnved', models.IntegerField()),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
