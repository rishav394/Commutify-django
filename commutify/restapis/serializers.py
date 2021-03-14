from django.db import models
from django.db.models import fields
from commutify.restapis.models import (
    User,
    Domain,
    Gender,
    Status,
    UserDomains,
    UserFriend,
)
from rest_framework import serializers


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Domain


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Gender


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "name",
            "email",
            "phone",
            "dob",
            "gender",
            "photo",
            "bio",
            "joined_at",
        ]
        model = User


class UserDomainsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = UserDomains


class UserFriendSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = UserFriend
