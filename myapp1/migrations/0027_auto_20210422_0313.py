# Generated by Django 3.1.7 on 2021-04-21 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp1', '0026_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='v_gstno',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
