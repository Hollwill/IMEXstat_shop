# Generated by Django 2.2.5 on 2020-02-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegionHandbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('okato', models.CharField(blank=True, max_length=5, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]