# Generated by Django 3.2.4 on 2021-09-01 18:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0045_item_beforeprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='beforePrice',
        ),
        migrations.AddField(
            model_name='item',
            name='percent',
            field=models.PositiveIntegerField(default=30, validators=[django.core.validators.MaxValueValidator(99)]),
        ),
    ]
