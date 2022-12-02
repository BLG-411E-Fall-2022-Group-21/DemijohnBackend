from .models import User, Cart, PreviousOrder
from rest_framework import status
from rest_framework.test import APITestCase
import hashlib

data = {"username": "test", "password": "test"}

 
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

class GetPreviousOrders(APITestCase):
    pass



#TODO: test get_previous_orders
# class GetPreviousOrders(APITestCase):
#     def test_get_previous_orders(self):
#         data = {"username": "test", "password": "test"}
#         self.client.post("/signup/", data, format="json")
#         response = self.client.post("/login/", data, format="json")
#         self.assertEqual(response.status_code, 200)
#         user = User.objects.get(username="test")
#         self.assertEqual(user.username, "test") 
#         # PreviousOrder.objects.create(user_id=user, bottle=5, water_type="still")
#         hashed_password = hashlib.md5("test".encode()).hexdigest()
#         aa =  User.objects.filter(username="test").count()

#         user_count = User.objects.filter(username="test", password=hashed_password).count()
#         self.assertEqual(aa, 1)
#         response = self.client.get("/get_previous_orders/", data, format="json")
#         # # self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), {"orders": [{"bottle": 5, "water_type": "still"}]})