from django.db import models
from django.db.models import fields
from commutify.restapis.models import (
    User,
    Domain,
    Gender,
    FriendshipStatus,
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
        model = FriendshipStatus


class UserSerializer(serializers.ModelSerializer):
    # gender = serializers.CharField(source="gender.value")

    class Meta:
        fields = [
            "id",
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
