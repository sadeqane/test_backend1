from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import CharField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField
from rest_framework import serializers
from django.utils.translation import gettext as _

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['deposite', 'password', 'groups', 'user_permissions']


class UserCreateSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    confirm_password = ReadOnlyField()
    username = serializers.CharField()
    password = serializers.CharField()
    groups = serializers.CharField(write_only=True)

    class Meta:
        fields = [
            'username',
            'password',
            'confirm_password',
            'groups',
            # 'first_name',
            # 'last_name',
            # 'email',
            # 'is_active',
        ]

    def validate_username(self, value):
        if value in get_user_model().objects.values_list("username", flat=True):
            raise ValidationError({"username": _("username is duplicate")})
        return value

    # def validate_confirm_password(self, value):
    #     if self.get_initial().get('password') != value:
    #         raise ValidationError({"confirm_password": _("The password does not match")})
    #     return value

    def validate_password(self, value):
        data = self.initial_data.copy()
        confirm_password = data.pop('confirm_password')
        # user = get_user_model()(**data)
        if confirm_password != value:
            raise ValidationError(_("The confirm_password does not match"))
        try:
            validate_password(password=data['password'])
        except ValidationError as err:
            raise ValidationError({"password": str(err)})
        return value

    def validate_groups(self, value):
        if not value in ["seller", 'buyer']:
            raise ValidationError("The available groups are 'buyer' and 'seller'")
        return value

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')
        group = validated_data.pop('groups', "buyer")

        validated_data.pop('confirm_password', None)
        user = get_user_model()(**validated_data)
        user.set_password(password)
        user.save()
        user.groups.add(Group.objects.get(name=group))
        return user

    # def to_representation(self, instance):
    #     return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'groups',
            'deposit',
        ]
        read_only_fields = ['groups',
                            'deposit', ]

    def validate_username(self, value):
        if value in get_user_model().objects.values_list("username", flat=True):
            raise ValidationError({"username": _("username is duplicate")})
        return value
