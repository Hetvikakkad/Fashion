# Generated by Django 3.1.7 on 2021-03-21 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0004_auto_20210321_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color_id',
            field=models.CharField(default='', max_length=30),
        ),
    ]
