# Generated by Django 3.1.7 on 2021-03-14 10:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapis', '0009_auto_20210314_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(8), django.core.validators.RegexValidator(code='invalid_phonee', message='Phone number can only contain numbers', regex='^\\d+$')]),
        ),
    ]