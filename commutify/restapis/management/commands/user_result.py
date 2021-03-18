# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = UserResultfromdict(json.loads(json_string))

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, TypeVar, Type, cast, Callable
from uuid import UUID
import dateutil.parser


T = TypeVar("T")


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Dob:
    date: datetime

    @staticmethod
    def from_dict(obj: Any) -> "Dob":
        assert isinstance(obj, dict)
        date = from_datetime(obj.get("date"))
        return Dob(date)

    def to_dict(self) -> dict:
        result: dict = {}
        result["date"] = self.date.isoformat()
        return result


@dataclass
class Login:
    uuid: UUID

    @staticmethod
    def from_dict(obj: Any) -> "Login":
        assert isinstance(obj, dict)
        uuid = UUID(obj.get("uuid"))
        return Login(uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = str(self.uuid)
        return result


@dataclass
class Name:
    title: str
    first: str
    last: str

    @staticmethod
    def from_dict(obj: Any) -> "Name":
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        first = from_str(obj.get("first"))
        last = from_str(obj.get("last"))
        return Name(title, first, last)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["first"] = from_str(self.first)
        result["last"] = from_str(self.last)
        return result


@dataclass
class Picture:
    large: str

    @staticmethod
    def from_dict(obj: Any) -> "Picture":
        assert isinstance(obj, dict)
        large = from_str(obj.get("large"))
        return Picture(large)

    def to_dict(self) -> dict:
        result: dict = {}
        result["large"] = from_str(self.large)
        return result


@dataclass
class Result:
    name: Name
    email: str
    login: Login
    dob: Dob
    registered: Dob
    phone: str
    picture: Picture

    @staticmethod
    def from_dict(obj: Any) -> "Result":
        assert isinstance(obj, dict)
        name = Name.from_dict(obj.get("name"))
        email = from_str(obj.get("email"))
        login = Login.from_dict(obj.get("login"))
        dob = Dob.from_dict(obj.get("dob"))
        registered = Dob.from_dict(obj.get("registered"))
        phone = from_str(obj.get("phone"))
        picture = Picture.from_dict(obj.get("picture"))
        return Result(name, email, login, dob, registered, phone, picture)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = to_class(Name, self.name)
        result["email"] = from_str(self.email)
        result["login"] = to_class(Login, self.login)
        result["dob"] = to_class(Dob, self.dob)
        result["registered"] = to_class(Dob, self.registered)
        result["phone"] = from_str(self.phone)
        result["picture"] = to_class(Picture, self.picture)
        return result


@dataclass
class UserResult:
    results: List[Result]

    @staticmethod
    def from_dict(obj: Any) -> "UserResult":
        assert isinstance(obj, dict)
        results = from_list(Result.from_dict, obj.get("results"))
        return UserResult(results)

    def to_dict(self) -> dict:
        result: dict = {}
        result["results"] = from_list(lambda x: to_class(Result, x), self.results)
        return result


def UserResultfromdict(s: Any) -> UserResult:
    return UserResult.from_dict(s)


def UserResulttodict(x: UserResult) -> Any:
    return to_class(UserResult, x)
