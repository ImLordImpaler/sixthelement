# Generated by Django 3.2.4 on 2021-09-01 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0042_auto_20210827_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
