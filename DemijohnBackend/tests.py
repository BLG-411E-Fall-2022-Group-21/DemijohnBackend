from .models import User, Cart, PreviousOrder
from rest_framework import status
from rest_framework.test import APITestCase


class SignupTestCase(APITestCase):
    def test_signup(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post("/signup/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, "test")


class Login(APITestCase):
    def test_login(self):
        data = {"username": "test", "password": "test"}
        self.client.post("/signup/", data, format="json")
        response = self.client.post("/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, "test")
