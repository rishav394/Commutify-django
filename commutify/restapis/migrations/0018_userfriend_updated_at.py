# Generated by Django 3.1.7 on 2021-03-14 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapis', '0017_auto_20210314_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfriend',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
