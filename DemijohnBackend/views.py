from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
import hashlib


@api_view(["POST"])
def signup(request):
    print(request.data)
    username: str = request.data["username"]
    user = User.objects.filter(username=username).count()
    if user > 0:
        return JsonResponse({"message": "Username already exists."}, status=400)
    hashed_password = hashlib.md5(request.data["password"].encode()).hexdigest()
    User.objects.create(username=username, password=hashed_password)
    return JsonResponse({"user": username}, status=201)


@api_view(["POST"])
def login(request):
    """
    check request.data["username"] and hashlib.md5(request.data["password"].encode()).hexdigest() against
    database if true return HTTP 200 else return HTTP 400
    """
    pass


@api_view(["GET"])
def get_previous_orders(request):
    """
    check user request.data["username"] previous orders. If user exists return HTTP 200 and previous orders
    {orders:[{bottle:5, water_type:still}, {bottle:10, water_type:sparkling}]} else return HTTP 400
    else return HTTP 400
    """
    pass


@api_view(["GET"])
def get_cart(request):
    """
    check user request.data["username"] cart. If user exists return HTTP 200 and previous orders
    {orders:[{bottle:5, water_type:still}, {bottle:10, water_type:sparkling}]} else return HTTP 400
    else return HTTP 400
    """
    pass


@api_view(["GET"])
def get_user_address(request):
    """
    check user request.data["username"] address. If user exists return HTTP 200 and user address
    else return HTTP 400
    """
    pass


@api_view(["POST"])
def place_order(request):
    """
    check user request.data["username"] cart. If user exists add items in the cart to previous orders and empty cart and return HTTP 200
    if user not exists return HTTP 400
    """
    pass


@api_view(["POST"])
def change_address(request):
    """
    check user request.data["username"] address. if user exisst change address  to request.data["new_address"] and return http 200
    if user not exists return http 400
    """
    pass


@api_view(["POST"])
def change_recurring_order_period(request):
    """
    check user request.data["username"] username. if user exists change reccuring order to request.data["new_period"] and return http 200
    if user not exists return http 400
    """
    pass


@api_view(["POST"])
def change_recurring_order_bottle(request):
    """
    check user request.data["username"] username. if user exists change reccuring order to request.data["new_bottle"] and return http 200
    if user not exists return http 400
    """
    pass


@api_view(["POST"])
def add_item_to_cart(request):
    """
    check user request.data["username"] username. if user exists add item (request.data["item"] will be like {"bottle":"15","type":"still"})
    to the user's cart and return http 200
    if user not exists return http 400
    """
    pass
