from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.models import UserManager
from backend1.helpers import deposit_should_be_multiply_5

# Create your models here.
from account.models import User


class Product(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    product_name = models.CharField(max_length=150)
    cost = models.PositiveIntegerField(validators=[deposit_should_be_multiply_5])
    amount_available = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
