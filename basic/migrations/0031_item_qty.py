# Generated by Django 3.2.4 on 2021-08-20 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0030_enquiry_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='qty',
            field=models.CharField(blank=True, choices=[('250 gm', '250 gm'), ('255 gm', '255 gm'), ('1 gm', '1 gm'), ('3 gm', '3 gm')], max_length=1000, null=True),
        ),
    ]
