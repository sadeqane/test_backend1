from django.db.models import ProtectedError
from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from django.utils.translation import gettext as _

from account.models import User
from account.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated

from backend1.permissions import CustomUserPermission


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [CustomUserPermission]
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        if self.request.method in ["PUT", "PATCH"]:
            return UserUpdateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
        except ProtectedError as e:
            raise ValidationError(_("The user has many products in the store, so delete the products first"))
