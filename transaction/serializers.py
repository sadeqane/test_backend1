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


class DepositSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=False)

    deposit = serializers.IntegerField()

    def validate_deposit(self, value):
        if value < 0 or value not in [5, 10, 20, 50, 100]:
            raise ValidationError(_("Deposit Must be 5, 10, 20, 50, 100"))
        return value

    @transaction.atomic
    def create(self, validated_data):
        deposit = validated_data.get("deposit", 0)
        user = validated_data.get("user")
        user.deposit = user.deposit + deposit
        user.save()
        return user

    def update(self, instance, validated_data):
        pass


class BuySerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product_id")
    amount = serializers.IntegerField()

    def validate_amount(self, value):
        if value < 1:
            raise ValidationError(_("Amount should be more than 0"))
        return value

    def validate(self, attrs):
        super().validate(attrs)
        user = attrs.get('user')
        product = attrs.get('product_id')
        amount = attrs.get('amount')
        if user.deposit < product.cost * amount:
            raise ValidationError(_(f"You need {product.cost * amount - user.deposit} more for this purchase"))
        if product.amount_available < amount:
            raise ValidationError(_(f"The remained product is: {int(product.amount_available)}"))
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.get("user")
        product = validated_data.get('product_id')
        amount = validated_data.get('amount')
        if user.deposit >= product.cost * amount:
            user.deposit = user.deposit - (product.cost * amount)
            user.save()
            product.amount_available = product.amount_available - int(amount)
            product.save()
        return user

    def update(self, instance, validated_data):
        pass

    def to_representation(self, instance):
        return {
            "balance": instance.deposit,
            "buy_status": "successful"
        }


class ResetDepositSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), write_only=False)

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data.get("user")
        user.deposit = 0
        user.save()
        return user

    def to_representation(self, instance):
        return {
            "balance": instance.deposit,
        }
