# Generated by Django 3.1.1 on 2020-10-01 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20201001_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='key',
            field=models.CharField(max_length=40, unique=True, verbose_name='Key'),
        ),
    ]