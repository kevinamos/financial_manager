import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import validate_email
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, password=None):
        pass_hash = make_password(password)
        user = self.model(
            email=email,
            phone_number=phone_number,
            password=pass_hash
        )
        user.save()
        return user

    def create_superuser(self, email, password, ** kwargs):
        pass_hash = make_password(password)
        user = self.model(
            email=email, password=pass_hash
        )
        user.active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(
        null=True,
        blank=True,
        max_length=255
    )
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        max_length=40,
        null=True,
        blank=True,
        unique=True,

    )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='The time the transaction was done.'
    )
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.updated_at:
            self.updated_at = timezone.now()
        if not self.username:
            if self.phone_number is None:
                self.username = self.email
            else:
                self.username = self.phone_number
        if self.phone_number is not None and not self.phone_number.is_valid():
            raise ValidationError(_('Invalid phone number.'))
        if self.email:
            validate_email(self.email)
        return super(User, self).save()

    @property
    def full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '%s %s - %s' % (self.first_name, self.last_name, self.email)
