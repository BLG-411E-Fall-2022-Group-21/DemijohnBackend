from itertools import chain
from tkinter.messagebox import NO
from DemijohnBackend.views import get_user_address, place_order
from http import server
from .models import User, Cart, PreviousOrder
from rest_framework import status
from rest_framework.test import APITestCase
import hashlib

#################################### TESTS VIEW ####################################

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

class RemoveItemFromCartTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_remove_item_from_cart", "password": "test_remove_item_from_cart"}
        self.blank_json = {'orders': []}
        self.item = {"bottle":"15","type":"still"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
        
    def test_remvoe_item_from_cart_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/remove_item_from_cart/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_remove_item_from_cart_without_add_item(self):
        response_get_cart = self.client.post('/get_cart/', self.user_data, format="json")
        response_remove_item = self.client.post('/remove_item_from_cart/', self.user_data, format="json")

        self.assertEqual(response_get_cart.json(), self.blank_json)
        self.assertEqual(response_remove_item.status_code, 400)
    
    def test_remove_item_from_cart(self):
        self.user_data['bottle'] = 32
        self.user_data['type'] = "MineralWater"
        self.client.post('/add_item_to_cart/', self.user_data, format="json")
        self.user_data['bottle'] = 64
        self.user_data['type'] = "Sparkling"
        self.client.post('/add_item_to_cart/', self.user_data, format="json")

        response_get_cart = self.client.post('/get_cart/', {"username": "test_remove_item_from_cart", "password": "test_remove_item_from_cart"}, format="json")
        
        self.assertEqual(len(response_get_cart.json()['orders']), 2)

        remove_user_data = {"username":"test_remove_item_from_cart", "password":"test_remove_item_from_cart", "bottle":"32","type":"MineralWater"}
        response_remove_item = self.client.post('/remove_item_from_cart/', remove_user_data, format="json")
        self.assertEqual(response_remove_item.status_code, 200)
        self.assertEqual(response_remove_item.json(), {"message": "success"})

        response_get_cart = self.client.post('/get_cart/', {"username": "test_remove_item_from_cart", "password": "test_remove_item_from_cart"}, format="json")
        self.assertEqual(len(response_get_cart.json()['orders']), 1)

        
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
        self.user_data = {"username": "test_sezer_place_order", "password": "test_sezer_place_order"}
        self.user_data_items = {"username": "test_sezer_place_order", "password": "test_sezer_place_order", "bottle":"31", "type":"Ekşi"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_place_order_invalid_name(self):
        response = self.client.post('/place_order/', {"username": "invalid", "password": "invalid"}, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_place_order(self):
        response_add_item_to_cart =  self.client.post('/add_item_to_cart/', self.user_data_items, format="json")
        response_get_cart = self.client.post('/get_cart/', self.user_data, format="json")
        response_place_order = self.client.post('/place_order/', self.user_data, format="json")

        self.assertEqual(response_add_item_to_cart.status_code, 200)
        self.assertEqual(response_get_cart.status_code, 200)
        self.assertEqual(response_place_order.status_code, 200)
        self.assertEqual(response_add_item_to_cart.json(), {"message": "success"})
        self.assertEqual(response_get_cart.json(), { "orders": [{  "bottle": 31,  "water_type": "Ekşi"}]})
        self.assertEqual(response_place_order.json(), {"message": "success"})


class GetPreviousOrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_get_previous_order", "password": "test_get_previous_order"}
        self.user_data_2 = {"username": "test_get_previous_order", "password": "test_get_previous_order", "bottle":"1","type":"Erzinca_Ekşi_Su"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
        self.invalid_user_name = {"username": None, "password": "test"}
        self.blank_order_json = {'orders': []}

    def test_get_previous_order_invalid_name(self):
        response = self.client.post("/get_previous_orders/", self.invalid_user_name, format="json")
        self.assertEqual(response.status_code, 400)

    def test_get_previous_order_without_add_item(self):
        blank_order_json = {'orders': []}
        response = self.client.post("/get_previous_orders/", self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted(blank_order_json.items()) , sorted(response.json().items()))
    
    def test_previous_order_without_place_order(self):    
        response_cart = self.client.post("/add_item_to_cart/", self.user_data_2, format="json")
        response_previous_order = self.client.post("/get_previous_orders/", self.user_data, format="json")
        
        self.assertEqual(response_cart.status_code, 200)
        self.assertEqual(response_cart.json(), {"message": "success"})
        self.assertEqual(response_previous_order.status_code, 200)
        self.assertEqual(response_previous_order.json(), self.blank_order_json)   

    def test_get_previous_order(self):
        response_cart = self.client.post("/add_item_to_cart/", self.user_data_2, format="json")
        get_cart = self.client.post("/get_cart/", self.user_data, format="json")    
        place_order_ = self.client.post("/place_order/", self.user_data, format="json")

        self.assertEqual(get_cart.status_code, 200)
        self.assertEqual(response_cart.status_code, 200)
        self.assertEqual(get_cart.json(), { "orders": [{  "bottle": 1,  "water_type": "Erzinca_Ekşi_Su"}]})
        self.assertEqual(place_order_.status_code, 200)
        self.assertEqual(place_order_.json(),  {"message": "success"}) 

        get_previous_orders = self.client.post("/get_previous_orders/", self.user_data, format="json")
        
        self.assertEqual(get_previous_orders.status_code, 200)
        self.assertEqual(get_previous_orders.json(),  get_cart.json())

    def test_get_previous_orders_consecutive_order(self):
        self.user_item_2 = {"username": "test_get_previous_order", "password": "test_get_previous_order", "bottle":"21","type":"Avşar_Ekşi_Su"}
        self.client.post("/add_item_to_cart/", self.user_data_2, format="json")
        self.client.post("/add_item_to_cart/", self.user_item_2, format="json")
        self.client.post("/place_order/", self.user_data, format="json")

        response_get_pre_orders = self.client.post("/get_previous_orders/", self.user_data, format="json")
        
        self.assertEqual(response_get_pre_orders.status_code, 200)
        self.assertEqual(response_get_pre_orders.json(), { "orders": [{  "bottle": 1,  "water_type": "Erzinca_Ekşi_Su"},
                                                                         {"bottle":21, "water_type": "Avşar_Ekşi_Su"}]})

        # after calling get_previous_orders cart must be blank.
        response_get_card = self.client.post("/get_cart/", self.user_data, format="json")  
        self.assertEqual(response_get_card.json(), self.blank_order_json)


class ChangeAdressTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_change_adress", "password": "test_change_adress"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_change_adress_invalid_name(self):
        self.user_data['username'] = None
        response_change_adress = self.client.post("/change_address/", self.user_data, format="json")
        self.assertEqual(response_change_adress.status_code, 400)

    def test_change_adress(self):
        self.user_data['new_address'] = "Başakşehir"
        response_change_adress = self.client.post("/change_address/", self.user_data, format="json")
        self.assertEqual(response_change_adress.status_code, 200)

class GetUserAdressTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_get_user_adress", "password": "test_get_user_adress"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_get_user_adress_invalid_name(self):
        self.user_data['username'] = None
        response_get_user_address = self.client.post("/get_user_address/", self.user_data, format="json")
        self.assertEqual(response_get_user_address.status_code, 400)

    def test_get_user_adress(self):
        self.user_data['new_address'] = "Başakşehir"
        response_change_adress = self.client.post("/change_address/", self.user_data, format="json")
        del self.user_data['new_address']
        response_get_user_adress = self.client.post("/get_user_address/", self.user_data, format="json")

        self.assertEqual(response_change_adress.status_code, 200)
        self.assertEqual(response_get_user_adress.status_code, 200)
        self.assertEqual(response_get_user_adress.json(), {"address": "Başakşehir"})


class ChangeRecurringOrderPeriodTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_change_recurring_order_period", "password": "test_change_recurring_order_period"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")

    def test_change_rec_order_period_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/change_recurring_order_period/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_change_rec_order_period(self):
        self.user_data['new_period'] = 3
        response = self.client.post('/change_recurring_order_period/', self.user_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})
    
class GetRecurringOrderPeriodTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_get_recurring_order_period", "password": "test_get_recurring_order_period"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")

    def test_get_recurring_order_period_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/get_recurring_order_period/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_get_recurring_order_period(self):
        self.user_data['new_period'] = 4
        self.client.post('/change_recurring_order_period/', self.user_data, format="json")
        del self.user_data['new_period']
        response = self.client.post('/get_recurring_order_period/', self.user_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"period": 4})
    
class ChangeRecurringOrderTypeTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_change_recurring_order_type", "password": "test_change_recurring_order_type"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_change_recurring_order_type_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/change_recurring_order_type/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_change_recurring_order_type(self):
        self.user_data['new_type'] = "sparkling"
        response = self.client.post('/change_recurring_order_type/', self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})

class GetRecurringOrderTypeTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_get_recurring_order_type", "password": "test_get_recurring_order_type"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_change_recurring_order_type_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/get_recurring_order_type/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_change_recurring_order_type(self):
        self.user_data['new_type'] = "sparkling"
        self.client.post('/change_recurring_order_type/', self.user_data, format="json")
        del self.user_data['new_type']
        
        response = self.client.post('/get_recurring_order_type/', self.user_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"type": "sparkling"})
    
class ChangeRecurringOrderBottle(APITestCase):
    def setUp(self) -> None:
        
        self.user_data = {"username": "test_change_recurring_order_bottle", "password": "test_change_recurring_order_bottle"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_change_recurring_order_type_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/change_recurring_order_bottle/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400) 
    
    def test_change_recurring_order_type(self):
        self.user_data['new_bottle'] = 20
        response = self.client.post('/change_recurring_order_bottle/', self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})
    
class GetRecurringOrderTypeTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_get_recurring_order_bottle", "password": "test_get_recurring_order_bottle"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
    
    def test_change_recurring_order_type_with_invalid_name(self):
        self.user_data['username'] = None
        response = self.client.post('/get_recurring_order_bottle/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_change_recurring_order_type(self):
        self.user_data['new_bottle'] = 12
        self.client.post('/change_recurring_order_bottle/', self.user_data, format="json")
        del self.user_data['new_bottle']
        
        response = self.client.post('/get_recurring_order_bottle/', self.user_data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"bottle": 12})

class CancelRecurringOrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.user_data = {"username": "test_cancel_recurring_order", "password": "test_cancel_recurring_order"}
        self.client.post("/signup/", self.user_data, format="json")
        self.client.post("/login/", self.user_data, format="json")
        # create recurring order
        self.user_data['new_type'] = "sparkling"
        self.client.post('/change_recurring_order_type/', self.user_data, format="json")
        del self.user_data['new_type']
        self.user_data['new_period'] = 3
        self.client.post('/change_recurring_order_period/', self.user_data, format="json")
        del self.user_data['new_period']
        self.user_data['new_bottle'] = 20
        self.client.post('/change_recurring_order_bottle/', self.user_data, format="json")
        del self.user_data['new_bottle']

    def test_cancel_recurring_order_wrong_password(self):
        self.user_data['password'] = "wrong_password"
        response = self.client.post('/cancel_recurring_order/', self.user_data, format="json")
        self.assertEqual(response.status_code, 400)
    
    def test_cancel_recurring_order(self):
        response = self.client.post('/cancel_recurring_order/', self.user_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "success"})

#################################### END TEST VIEW ####################################
