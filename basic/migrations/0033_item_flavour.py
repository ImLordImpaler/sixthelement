# Generated by Django 3.2.4 on 2021-08-20 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0032_auto_20210820_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='flavour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='basic.flavor'),
        ),
    ]