# Generated by Django 3.2.4 on 2021-08-04 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0028_enquiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
