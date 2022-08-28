from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from account.models import User
from account.serializers import UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated

from backend1.permissions import CustomUserPermission, CustomProductPermisstion
from product.models import Product
from product.serializers import ProductSerializer, ProductCreateSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [CustomProductPermisstion]
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer
