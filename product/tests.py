from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from model_mommy import mommy

# Create your tests here.
from product.models import Product


class ProductTest(APITestCase):
    fixtures = ["roles"]

    def setUp(self) -> None:
        self.buyer_user = mommy.make(get_user_model(), deposit=150, groups=[Group.objects.get(name="buyer")])
        self.seller_user = mommy.make(get_user_model(), deposit=150,
                                      groups=[Group.objects.get(name="seller")])
        # self.product1 = mommy.make(Product, cost=45, amount_available=8, user=self.seller_user)
        # self.product2 = mommy.make(Product, cost=145, amount_available=3, user=self.seller_user)

    def test_buyer_can_not_access_fail(self):
        self.client.force_login(self.buyer_user)
        url = "/products/"
        payload = {
            "product_name": "xxx",
            "cost": 10,
            "amount_available": 12
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_product_price_should_be_multiple_5_fail(self):
        self.client.force_login(self.seller_user)
        url = "/products/"
        payload = {
            "product_name": "xxx",
            "cost": 11,
            "amount_available": 12,
        }
        response = self.client.post(url, data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list(self):
        self.product1 = mommy.make(Product, user=self.seller_user, _quantity=3)
        # self.client.force_login(self.seller_user)
        url = "/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_product_retrive(self):
        product1 = mommy.make(Product, user=self.seller_user)
        self.client.force_login(self.seller_user)
        url = f"/products/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
