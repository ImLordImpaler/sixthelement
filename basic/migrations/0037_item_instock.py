# Generated by Django 3.2.4 on 2021-08-24 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0036_item_beforeprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='instock',
            field=models.BooleanField(default=False),
        ),
    ]