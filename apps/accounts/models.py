from django.db import models

# Create your models here.

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin
)

from .managers import UserManager


class User(
    AbstractBaseUser,
    PermissionsMixin
):

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
