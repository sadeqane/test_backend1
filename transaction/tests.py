from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy

# Create your tests here.
from product.models import Product


class Deposit(APITestCase):
    def setUp(self) -> None:
        self.user = mommy.make(get_user_model(), username="test")

    def test_deposit_valid_coin_success(self):
        self.client.force_login(self.user)
        url = "/deposit/"
        payload = {
            "deposit": 100
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("deposit"), payload.get("deposit"))

    def test_deposit_un_valid_coin_fail(self):
        self.client.force_login(self.user)
        url = "/deposit/"
        payload = {
            "deposit": 11
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deposit_un_authorize_403_fail(self):
        url = "/deposit/"
        payload = {
            "deposit": 10
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class Buy(APITestCase):
    fixtures = ["roles"]

    def setUp(self) -> None:
        self.buyer_user = mommy.make(get_user_model(), deposit=150, groups=[Group.objects.get(name="buyer")])
        self.seller_user = mommy.make(get_user_model(), deposit=150,
                                      groups=[Group.objects.get(name="seller")])
        self.product1 = mommy.make(Product, cost=45, amount_available=8, user=self.seller_user)
        self.product2 = mommy.make(Product, cost=145, amount_available=3, user=self.seller_user)

    def test_buy_seller_instead_buyer_403_fail(self):
        self.client.force_login(self.seller_user)
        url = "/buy/"
        payload = {
            "product": 1,
            "amount": 70
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_buy_without_enough_money_fail(self):
        self.client.force_login(self.buyer_user)
        url = "/buy/"
        payload = {
            "product": self.product1.pk,
            "amount": self.product1.amount_available
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_more_than_product_capacity_fail(self):
        buyer_user = mommy.make(get_user_model(), deposit=2500, groups=[Group.objects.get(name="buyer")])
        self.client.force_login(buyer_user)
        url = "/buy/"
        payload = {
            "product": self.product1.pk,
            "amount": self.product1.amount_available + 1
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_unvalid_amount_fail(self):
        buyer_user = mommy.make(get_user_model(), deposit=2500, groups=[Group.objects.get(name="buyer")])
        self.client.force_login(buyer_user)
        url = "/buy/"
        payload = {
            "product": self.product1.pk,
            "amount": -1
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_buy_successfully(self):
        budget = 2500
        all_price = self.product1.amount_available * self.product1.cost
        buyer_user = mommy.make(get_user_model(), deposit=budget, groups=[Group.objects.get(name="buyer")])
        self.client.force_login(buyer_user)
        url = "/buy/"
        payload = {
            "product": self.product1.pk,
            "amount": self.product1.amount_available
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product1.refresh_from_db()
        buyer_user.refresh_from_db()
        self.assertEqual(self.product1.amount_available, 0)
        self.assertEqual(buyer_user.deposit, budget - (all_price))
