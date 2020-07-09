from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    public_id = models.CharField(
        max_length=255,
        default=token_urlsafe,
        unique=True,
        help_text="Random sequence to be used as a public identifier.",
    )
    email = models.EmailField(_("email address"), unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
