# Generated by Django 3.1.7 on 2021-04-07 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0017_order_table_deliver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='P_id',
            field=models.TextField(default=''),
        ),
    ]
