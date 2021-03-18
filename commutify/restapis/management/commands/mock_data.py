import json
import re
import urllib.parse
import urllib.request
from random import choice, randrange

from commutify.restapis.models import (
    Domain,
    FriendshipStatus,
    Gender,
    User,
    UserChats,
    UserDomains,
    UserFriend,
)
from commutify.restapis.util import get_hashed_password
from django.core.management.base import BaseCommand

from .domain_names import domain_names
from .user_result import UserResultfromdict


class Command(BaseCommand):
    help = "Populates the entire DB with dummy data"

    def get_random_gender(self):
        if randrange(5) < 1:
            return None
        return Gender.objects.get(id=randrange(1, 5))

    def get_random_fiendship_status(self):
        return FriendshipStatus.objects.get(id=randrange(2, 5))

    def populate_users(self, count=100):
        print("Populating {} users".format(count))
        url = "https://randomuser.me/api/?results={}".format(count)
        f = urllib.request.urlopen(url)
        user_data = UserResultfromdict(json.loads(f.read().decode("utf-8")))
        for result in user_data.results:
            User.objects.create(
                name=result.name.first,
                email=result.email,
                phone=re.sub("[^0-9]", "", result.phone)[:10],
                password=get_hashed_password(result.email),
                dob="{}-{}-{}".format(
                    result.dob.date.year, result.dob.date.month, result.dob.date.day
                ),
                gender=self.get_random_gender(),
                photo=result.picture.large,
                bio="I am {} {} and my email is {}".format(
                    result.name.first, result.name.last, result.email
                ),
            )
        print("Populated {} users".format(count))

    def populate_domains(self):
        names = domain_names
        print("Populating {} domains".format(len(names)))
        infos = list(map(lambda x: "Some information about {}".format(x), names))

        for i in range(len(names)):
            Domain.objects.create(
                name=names[i].capitalize(),
                info=infos[i],
                created_by=User.objects.order_by("?")[0],
            )
        print("Populated {} domains".format(len(names)))

    def populate_user_domains(self, count=100):
        print("Populating {} user-domains".format(count))
        success_count = 0
        while success_count < count:
            try:
                UserDomains.objects.create(
                    domain=Domain.objects.order_by("?")[0],
                    user=User.objects.order_by("?")[0],
                )
                success_count += 1
            except:
                pass
        print("Populated {} user-domains".format(count))

    def populate_user_friends(self, count=200):
        print("Populating {} user-friends".format(count))
        success_count = 0
        while success_count < count:
            try:
                user1: User = User.objects.order_by("?")[0]
                user2 = User.objects.order_by("?")[0]
                if user1.id == user2.id:
                    raise ""
                if user1.id > user2.id:
                    user1, user2 = user2, user1
                UserFriend.objects.create(
                    user1=user1,
                    user2=user2,
                    status=FriendshipStatus.objects.get(id=choice([3, 4])),
                    initiator=choice([user1, user2]),
                )
                success_count += 1
            except Exception as e:
                pass
        print("Populated {} user-friends".format(count))

    def handle(self, *args, **options):
        self.populate_users()
        self.populate_domains()
        self.populate_user_domains()
        self.populate_user_friends()
