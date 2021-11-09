# Generated by Django 3.2.4 on 2021-08-24 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0037_item_instock'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='servings',
            field=models.CharField(blank=True, choices=[('30', '30'), ('40', '40'), ('60', '60'), ('30/60', '30/60')], max_length=100, null=True),
        ),
    ]
