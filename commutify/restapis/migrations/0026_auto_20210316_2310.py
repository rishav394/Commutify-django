# Generated by Django 3.1.7 on 2021-03-16 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapis', '0025_auto_20210315_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
