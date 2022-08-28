# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend1.permissions import CustomBuyPermisstion
from transaction.serializers import DepositSerializer, BuySerializer, ResetDepositSerializer


class DepositView(CreateAPIView):
    serializer_class = DepositSerializer
    permission_classes = [IsAuthenticated]


class BuyView(CreateAPIView):
    serializer_class = BuySerializer
    permission_classes = [CustomBuyPermisstion]


class ResetDepositView(CreateAPIView):
    serializer_class = ResetDepositSerializer
    permission_classes = [IsAuthenticated]
