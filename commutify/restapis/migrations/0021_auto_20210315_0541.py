# Generated by Django 3.1.7 on 2021-03-15 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapis', '0020_auto_20210314_1946'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Status',
            new_name='FriendshipStatus',
        ),
    ]
