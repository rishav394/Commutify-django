import json
import re
import urllib.parse
import urllib.request
from random import choice, randrange, sample

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

    def populate_users(self, count=150):
        print("Populating {} users".format(count))
        url = "https://randomuser.me/api/?results={}".format(count)
        f = urllib.request.urlopen(url)
        user_data = UserResultfromdict(json.loads(f.read().decode("utf-8")))
        User.objects.create(
            name="Rishav Rungta",
            email="rishav394@gmail.com",
            phone="9958095891",
            password=get_hashed_password("9958095891"),
            dob="{}-{}-{}".format(1999, 11, 20),
            gender=self.get_random_gender(),
            bio="I am {} {} and my email is {}. I like to code and I am batman. Yes.".format(
                "Rishav", "Rungta", "rishav394@gmail.com"
            ),
        )
        for result in user_data.results:
            try:
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
            except Exception as e:
                print(e)
                print(result.email)
        print("Populated {} users".format(count))

    def populate_domains(self):
        names = domain_names
        print("Populating {} domains".format(len(names)))
        infos = list(map(lambda x: "Some information about {}".format(x), names))

        for i in range(len(names)):
            try:
                Domain.objects.create(
                    name=names[i].capitalize(),
                    info=infos[i],
                    created_by=User.objects.order_by("?")[0],
                )
            except Exception as e:
                print(names[i])
        print("Populated {} domains".format(len(names)))

    def populate_user_domains(self):
        print("Populating user-domains")
        domain_count = UserDomains.objects.count()
        users = UserDomains.objects.all()
        counter = 0
        for i in range(1, domain_count):
            users_to_do = sample(users, (len(users) - i) // 5)
            domain: Domain = Domain.objects.get(id=i)
            for x in users_to_do:
                try:
                    UserDomains.objects.create(
                        domain=domain,
                        user=x,
                    )
                    counter += 1
                except Exception as e:
                    print(e)
        print("Populated {} user-domains".format(counter))

    def populate_user_friends(self):
        print("Populating {} user-friends".format("some"))
        user_count = User.objects.count()
        counter = 0
        for i in range(1, user_count):
            to_friend = sample(range(i + 1, user_count), (user_count - i) // 2)
            user1: User = User.objects.get(id=i)
            for x in to_friend:
                user2 = User.objects.get(id=x)

                try:
                    UserFriend.objects.create(
                        user1=user1,
                        user2=user2,
                        status=FriendshipStatus.objects.get(id=choice([3, 4])),
                        initiator=choice([user1, user2]),
                    )
                    counter += 1
                except Exception as e:
                    print(e)
        print("Populated {} user-friends".format(counter))

    def handle(self, *args, **options):
        self.populate_users()
        self.populate_domains()
        self.populate_user_domains()
        self.populate_user_friends()
