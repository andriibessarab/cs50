# Generated by Django 3.0.6 on 2020-05-24 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_auto_20200522_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
