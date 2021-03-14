# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=10)
    info = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = "domain"


class Gender(models.Model):
    value = models.CharField(max_length=20)

    class Meta:
        db_table = "gender"


class Status(models.Model):
    value = models.CharField(max_length=30)

    class Meta:
        db_table = "status"


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.ForeignKey(
        Gender, models.DO_NOTHING, db_column="gender", blank=True, null=True
    )
    photo = models.CharField(max_length=400, blank=True, null=True)
    bio = models.CharField(max_length=600, blank=True, null=True)
    last_seen = models.DateField()

    class Meta:
        db_table = "user"


class UserDomains(models.Model):
    domain = models.ForeignKey(
        Domain, models.DO_NOTHING, db_column="domain", blank=True, null=True
    )
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="user", blank=True, null=True
    )

    class Meta:
        db_table = "user_domains"


class UserFriend(models.Model):
    user1 = models.ForeignKey(
        User, models.DO_NOTHING, db_column="user1", related_name="user1"
    )
    user2 = models.ForeignKey(
        User, models.DO_NOTHING, db_column="user2", related_name="user2"
    )
    status = models.PositiveIntegerField()

    class Meta:
        db_table = "user_friend"
