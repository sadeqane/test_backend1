from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import CharField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework import serializers
from django.utils.translation import gettext as _

from account.models import User
from product.models import Product
from backend1.helpers import deposit_should_be_multiply_5


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Product
        fields = [
            'user',
            'product_name',
            'cost',
            'amount_available'
        ]
        read_only_fields = ["user"]



class ProductCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=False)

    class Meta:
        model = Product
        fields = "__all__"

    def validate_cost(self, value):
        deposit_should_be_multiply_5(value)
        return value
