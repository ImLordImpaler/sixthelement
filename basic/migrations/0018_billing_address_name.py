# Generated by Django 3.2.4 on 2021-07-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0017_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing_address',
            name='name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]