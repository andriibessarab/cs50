# Generated by Django 3.0.6 on 2020-05-24 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_order_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(default=0),
        ),
    ]
