# Generated by Django 3.1.7 on 2021-03-14 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapis', '0002_auto_20210314_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
