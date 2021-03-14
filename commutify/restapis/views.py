from commutify.restapis.decorators import valid_session
from commutify.restapis.models import Domain, User, UserDomains, UserFriend, Status
from commutify.restapis.serializers import (
    DomainSerializer,
    UserDomainsSerializer,
    UserSerializer,
)
from django.db.models import Q
from django.core.exceptions import ValidationError
from commutify.restapis.util import get_hashed_password
from rest_framework import request, status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# USER


@api_view(["POST"])
def login(request: request.Request):
    if request.method == "POST":
        email = request.data.get("email", None)
        phone = request.data.get("phone", None)
        password = request.data.get("password", None)
        if (email is None and phone is None) or password is None:
            return Response(status=status.status.HTTP_400_BAD_REQUEST)
        t = dict()
        if email is not None:
            t["email__iexact"] = email
        elif phone is not None:
            t["phone"] = phone
        user: (User or None) = User.objects.filter(**t).first()
        if user is not None and user.check_password(password):
            # Correct details
            request.session["id"] = user.id
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def sign_up(request):
    if request.method == "PUT":
        try:
            newUser: User = User(**request.data)
            if not newUser.password:
                raise ValidationError("Password is required")
            newUser.password = get_hashed_password(newUser.password)
            newUser.save()
            request.session["id"] = newUser.id
            return Response(
                UserSerializer(newUser).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def logout(request):
    if "id" in request.session:
        del request.session["id"]
    return Response(status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@valid_session
def users(request: request.Request):
    # Get users for any filter. (From id, self user or by name, filters etc)
    if request.method == "GET":
        users = User.objects.filter(**request.data).values()
        return Response(users)
    if request.method == "POST":
        # Update self
        user: User or None = request.user
        for key in ["bio", "photo", "phone", "email", "gender"]:
            if request.data.get(key, None) is not None:
                setattr(user, key, request.data.get(key))
        user.save()
        return Response(UserSerializer(user).data)


# DOMAINS


@api_view(["GET", "PUT"])
@valid_session
def domains(request):
    if request.method == "GET":
        # Get domains
        domains = Domain.objects.filter().values()
        subscribed_domains = UserDomains.objects.filter(
            user=request.session["id"]
        ).values_list("domain_id")
        for domain in domains:
            domain["subscribed"] = domain["id"] in subscribed_domains[0]
        return Response(domains)
    elif request.method == "PUT":
        # Create domains
        try:
            newDomain: Domain = Domain.objects.create(
                **request.data, created_by=request.user
            )
            return Response(
                DomainSerializer(newDomain).data, status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@valid_session
def domain_users(request):
    # Get users in domains
    if request.method == "GET":
        users = UserDomains.objects.filter(**request.data).values(
            "user__id", "user__name", "domain__id", "user__photo"
        )
        # Need to verify
        friends = UserFriend.objects.filter(
            Q(Q(user1=request.session["id"]) | Q(user2=request.session["id"]))
            & Q(status=Status.objects.get(value="Connected"))
        ).values_list("user1", "user2")
        for user in users:
            user["connected"] = user["user__id"] in friends
        return Response(users)
    elif request.method == "PUT":
        # Link user to domain
        try:
            user = request.user
            domain = Domain.objects.filter(id=request.data.get("domain")).first()
            newUserDomain: UserDomains = UserDomains.objects.create(
                user=user, domain=domain
            )
            return Response(
                UserDomainsSerializer(newUserDomain).data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        # Unlink user to domain
        try:
            user = request.user
            domain = Domain.objects.filter(id=request.data.get("domain")).first()
            deleted_data = UserDomains.objects.filter(user=user, domain=domain).delete()
            if deleted_data[0] == 0:
                raise ValidationError("User isn't linked to this domain")
            return Response(
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


# FRIENDS


@api_view(["GET", "POST", "PUT", "DELETE"])
@valid_session
def friends(request):
    if request.method == "GET":
        # List friends with filter of this user
        all_friends = (
            UserFriend.objects.filter(
                Q(user1=request.session["id"]) | Q(user2=request.session["id"])
            )
            .filter(**request.data)
            .values("user1__id", "user2__id", "status__value", "initiator__id")
        )
        return Response(all_friends)
    if request.method == "POST":
        # Accept request
        user1 = request.data.get("friend_id")
        user2 = request.user.id
        if user1 > user2:
            user1, user2 = user2, user1

        update_count = UserFriend.objects.filter(
            user1=user1,
            user2=user2,
            status__value="Pending",
            initiator=request.data["friend_id"],
        ).update(status=Status.objects.get(value="Connected"))

        if update_count == 1:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("No such request found", status=status.HTTP_400_BAD_REQUEST)
    if request.method == "PUT":
        # Send friend request
        try:
            user1 = request.data.get("friend_id")
            user2 = request.user.id
            if user1 > user2:
                user1, user2 = user2, user1

            if user1 == request.user.id:
                user1 = request.user
            else:
                user1 = User.objects.get(id=user1)

            if user2 == request.user.id:
                user2 = request.user
            else:
                user2 = User.objects.get(id=user2)

            UserFriend.objects.create(
                user1=user1,
                user2=user2,
                status=Status.objects.get(value="Pending"),
                initiator=request.user,
            )

            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        # Cancel friend request or unfriend user
        user1 = request.data.get("friend_id")
        user2 = request.user.id
        if user1 > user2:
            user1, user2 = user2, user1

        delete = UserFriend.objects.filter(user1=user1, user2=user2).delete()
        if not delete[0] == 0:
            return Response(status=status.HTTP_202_ACCEPTED)
        else:
            return Response("No such request found", status=status.HTTP_400_BAD_REQUEST)