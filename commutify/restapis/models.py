import bcrypt
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
from django.db import models
from commutify.restapis.util import get_hashed_password


class Gender(models.Model):
    value = models.CharField(
        max_length=20, unique=True, null=True, validators=[MinLengthValidator(1)]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Gender, self).save(*args, **kwargs)

    class Meta:
        db_table = "gender"


class FriendshipStatus(models.Model):
    value = models.CharField(
        max_length=30, unique=True, null=True, validators=[MinLengthValidator(1)]
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(FriendshipStatus, self).save(*args, **kwargs)

    class Meta:
        db_table = "friendship_status"


class User(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        validators=[EmailValidator("Invalid email")],
    )
    phone = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex="^\\d+$",
                message="Phone number can only contain numbers",
                code="invalid_phonee",
            ),
        ],
    )
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
    dob = models.DateField(blank=False, null=True)
    gender = models.ForeignKey(
        Gender, models.DO_NOTHING, db_column="gender", null=True, blank=True
    )
    photo = models.CharField(max_length=255, null=True, blank=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    def check_password(self, plain_text_password):
        return bcrypt.checkpw(plain_text_password, self.password)

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.email is None and self.phone is None:
            raise ValidationError("One of email or phone is required")

        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = "user"


class Domain(models.Model):
    name = models.CharField(
        max_length=50, unique=True, null=True, validators=[MinLengthValidator(2)]
    )
    info = models.CharField(max_length=254, null=True, blank=True)
    created_by = models.ForeignKey(
        User, models.DO_NOTHING, db_column="created_by", null=True, blank=True
    )
    image = models.CharField(max_length=254, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Domain, self).save(*args, **kwargs)

    class Meta:
        db_table = "domain"


class UserDomains(models.Model):
    domain = models.ForeignKey(
        Domain, models.DO_NOTHING, db_column="domain", blank=False, null=False
    )
    user = models.ForeignKey(
        User, models.DO_NOTHING, db_column="user", null=False, blank=False
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(UserDomains, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_domains"
        unique_together = ("user", "domain")


class UserFriend(models.Model):
    user1 = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="user1",
        related_name="user1",
        blank=False,
        null=False,
    )
    user2 = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="user2",
        related_name="user2",
        blank=False,
        null=False,
    )
    status = models.ForeignKey(
        FriendshipStatus, models.DO_NOTHING, db_column="status", blank=False, null=False
    )
    initiator = models.ForeignKey(
        User, models.DO_NOTHING, db_column="initiator", blank=False, null=False
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.user1.id >= self.user2.id:
            raise ValidationError(
                "User 1 should be less than User 2 to avoid duplications"
            )
        super(UserFriend, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_friend"
        unique_together = ("user1", "user2")


class UserChats(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="from_user",
        related_name="from_user",
        blank=False,
        null=False,
    )
    to_user = models.ForeignKey(
        User,
        models.DO_NOTHING,
        db_column="to_user",
        related_name="to_user",
        blank=False,
        null=False,
    )
    message = models.CharField(
        max_length=200, blank=False, validators=[MinLengthValidator(1)]
    )
    read = models.BooleanField(default=False, blank=False, null=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(UserChats, self).save(*args, **kwargs)

    class Meta:
        db_table = "user_chats"
