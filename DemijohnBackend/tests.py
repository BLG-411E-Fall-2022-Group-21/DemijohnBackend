from http import server
import json
from .models import User, Cart, PreviousOrder
from rest_framework import status
from rest_framework.test import APITestCase
import hashlib


class SignupTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {"username": "test", "password": "test"}

    def test_signup_valid(self):
        response = self.client.post("/signup/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().username, "test")

    def test_signup_invalid_password(self):
        data = {"username": "test", "password": ""}
        response = self.client.post("/signup/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_signup_invalid_username(self):
        data = {"username":  None, "password": "test"}
        response = self.client.post("/signup/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_already_user(self):
        response = self.client.post("/signup/", self.data, format="json")
        self.assertEqual(201, response.status_code)
        data_2 = {"username": "test", "password": "test"}
        response = self.client.post("/signup/", data_2, format="json")
        self.assertEqual(400, response.status_code)


class Login(APITestCase):
    def setUp(self):
        self.user_data = {"username": "test", "password": "test"}
        self.user_data_wrong = {"username": "test2", "password": "test"}
        self.user_data_none_name = {"username": None, "password": "test"}

    def test_login(self):
        self.client.post("/signup/", self.user_data, format="json")
        response = self.client.post("/login/", self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get().username, "test")

    def test_login_wrong_name(self):
        self.client.post("/signup/", self.user_data, format="json")
        response = self.client.post("/login/", self.user_data_wrong, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertNotEqual(User.objects.get().username, "test2")

    def test_login_none_name(self):
        self.client.post("/signup/", self.user_data, format="json")
        response = self.client.post("/login/", self.user_data_none_name, format="json")
        self.assertEqual(response.status_code, 400)

class AddItemtoCardTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test", "password": "test", "bottle":"15", "type":"still"}
        self.res_json = {"message": "success"}
        self.user_data_invalid = {"username": None , "password": "test"}
        self.item = {"bottle":"15","type":"still"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")

    def test_add_item_to_card_with_invalid_username(self):
        response = self.client.post('/add_item_to_cart/', self.user_data_invalid, format="json")
        self.assertEqual(response.status_code, 400)

    def test_add_item_to_card(self):
        response = self.client.post('/add_item_to_cart/', self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.res_json)

class GetCartTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_sezer", "password": "test_sezer"}
        self.blank_json = {'orders': []}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
        
    def test_get_cart_without_order(self):
        response = self.client.post('/get_cart/', self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.blank_json)
    
    def test_get_cart_invalid_username(self):
        response = self.client.post('/get_cart/', {"username": "xx", "password": "yy"}, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_get_cart(self):
        self.customer = {"username": "test_sezer", "password": "test_sezer", "bottle":"2", "type":"ekşi_su"}
        self.order = { "orders": [{  "bottle": 2,  "water_type": "ekşi_su"}]}
        response_add_item = self.client.post('/add_item_to_cart/', self.customer, format="json")
        response_get_cart = self.client.post('/get_cart/', self.user_data, format="json")
        self.assertEqual(response_add_item.status_code, 200)
        self.assertEqual(response_get_cart.status_code, 200)
        self.assertEqual(response_get_cart.json(), self.order)

class PlaceOrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_sezer", "password": "test_sezer"}
    




"""
class GetPreviousOrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_sezer", "password": "test_sezer"}
        self.user_data_2 = {"username": "test_sezer", "password": "test_sezer", "bottle":"1","type":"Erzinca_Ekşi_Su"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
        self.invalid_user_name = {"username": None, "password": "test"}
        self.previous_orders = { "orders": [
                                    { "bottle": 1, "water_type": "sparkling"},
                                    { "bottle": 19, "water_type": "esad"},
                                    {  "bottle": 90,  "water_type": "testsu"},
                                    {  "bottle": 34,  "water_type": "acı"}]
                                }
    def test_get_previous_order_invalid_name(self):
        response = self.client.post("/get_previous_orders/", self.invalid_user_name, format="json")
        self.assertEqual(response.status_code, 400)

    def test_get_previous_order_without_add_item(self):
        blank_order_json = {'orders': []}
        response = self.client.post("/get_previous_orders/", self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(blank_order_json.items()) , sorted(response.json().items()))
    
    def test_get_previous_order_wihout_signup(self):
        self.user_data_ = {"username": "xx", "password": "xx"}
        response_cart = self.client.post("/get_previous_orders/", self.user_data_, format="json")
        self.assertEqual(response_cart.status_code, 400)
    
    def test_test_get_previous_order(self):
        
        self.client.post("/login/", self.user_data_2, format="json")
        response_cart = self.client.post("/add_item_to_cart/", self.user_data_2, format="json")
        response_previous_order = self.client.post("/get_previous_orders/", self.user_data, format="json")
        self.assertEqual(response_cart.status_code, 200)
        self.assertEqual(response_previous_order.status_code, 200)
        self.assertEqual(response_cart.json(), {"message": "success"})
        self.assertEqual(response_previous_order.json(), {"bottle":"1","type":"Erzinca_Ekşi_Su"})

        



"""
