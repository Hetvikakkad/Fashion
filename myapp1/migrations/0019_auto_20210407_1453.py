# Generated by Django 3.1.7 on 2021-04-07 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0018_auto_20210407_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_table',
            name='cancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='owner_order_table',
            name='cancel',
            field=models.BooleanField(default=False),
        ),
    ]
