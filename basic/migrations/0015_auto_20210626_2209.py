# Generated by Django 3.2.4 on 2021-06-26 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0014_auto_20210623_1035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='category',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
