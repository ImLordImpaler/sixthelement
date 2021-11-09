# Generated by Django 3.2.4 on 2021-09-01 21:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0049_reviews_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='rating',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]
