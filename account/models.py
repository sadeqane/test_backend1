from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import UserManager
from backend1.helpers import deposit_should_be_multiply_5
# Create your models here.



class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "username"
    username = models.CharField(_("username"),max_length=150,unique=True)
    password = models.CharField(_("password"), max_length=128)
    deposit = models.PositiveIntegerField(default=0, validators=[deposit_should_be_multiply_5])
    objects = UserManager()