# Generated by Django 3.1.1 on 2020-09-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='end',
            field=models.DateField(verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='poll',
            name='start',
            field=models.DateField(verbose_name='Дата старта'),
        ),
    ]