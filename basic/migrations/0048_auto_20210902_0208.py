# Generated by Django 3.2.4 on 2021-09-01 20:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic', '0047_auto_20210902_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='text',
            field=models.CharField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]