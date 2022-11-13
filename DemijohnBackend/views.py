from django.http import JsonResponse
from .models import User, PreviousOrder, Cart
from .serializers import UserSerializer
from rest_framework.decorators import api_view
import hashlib


@api_view(["POST"])
def signup(request):
    print(request.data)
    username: str = request.data.get("username")
    user = User.objects.filter(username=username).count()
    if user > 0:
        return JsonResponse({"message": "Username already exists."}, status=400)
    hashed_password = hashlib.md5(request.data.get("password").encode()).hexdigest()
    User.objects.create(username=username, password=hashed_password)
    return JsonResponse({"user": username}, status=201)


@api_view(["POST"])
def login(request):
    """
    check request.data["username"] and hashlib.md5(request.data["password"].encode()).hexdigest() against
    database if true return HTTP 200 else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        return JsonResponse({"user": username}, status=200)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["GET"])
def get_previous_orders(request):
    """
    check user request.data["username"] previous orders. If user exists return HTTP 200 and previous orders
    {orders:[{bottle:5, water_type:still}, {bottle:10, water_type:sparkling}]} else return HTTP 400
    else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user_id = User.objects.get(username=username).id
        orders = list(PreviousOrder.objects.filter(user_id=user_id).values())
        for i in range(len(orders)):
            orders[i].pop("user_id_id")
            orders[i].pop("id")
        return JsonResponse({"orders": orders}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["GET"])
def get_cart(request):
    """
    check user request.data["username"] cart. If user exists return HTTP 200 and previous orders
    {orders:[{bottle:5, water_type:still}, {bottle:10, water_type:sparkling}]} else return HTTP 400
    else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user_id = User.objects.get(username=username).id
        cart = list(Cart.objects.filter(user_id=user_id).values())
        for i in range(len(cart)):
            cart[i].pop("user_id_id")
            cart[i].pop("id")
        return JsonResponse({"orders": cart}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["GET"])
def get_user_address(request):
    """
    check user request.data["username"] address. If user exists return HTTP 200 and user address
    else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        address = User.objects.get(username=username).address
        return JsonResponse({"address": address}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["POST"])
def place_order(request):
    """
    check user request.data["username"] cart. If user exists add items in the cart to previous orders and empty cart and return HTTP 200
    if user not exists return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        cart = list(Cart.objects.filter(user_id=user.id).values())
        Cart.objects.filter(user_id=user.id).delete()
        for i in range(len(cart)):
            PreviousOrder.objects.create(user_id=user, bottle=cart[i]["bottle"], water_type=cart[i]["water_type"])
        return JsonResponse({"message": "success"}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["POST"])
def change_address(request):
    """
    check user request.data["username"] address. if user exisst change address  to request.data["new_address"] and return http 200
    if user not exists return http 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        user.address = request.data.get("new_address")
        user.save()
        return JsonResponse({"message": "success"}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["GET"])
def get_recurring_order_period(request):
    """
    check user request.data["username"] address. If user exists return HTTP 200 and user recurring order period
    else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        period = User.objects.get(username=username).recurring_order
        return JsonResponse({"period": period}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)

@api_view(["POST"])
def change_recurring_order_period(request):
    """
    check user request.data["username"] username. if user exists change reccuring order to request.data["new_period"] and return http 200
    if user not exists return http 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        user.recurring_order = request.data.get("new_period")
        user.save()
        return JsonResponse({"message": "success"}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["GET"])
def get_recurring_order_bottle(request):
    """
    check user request.data["username"] address. If user exists return HTTP 200 and user recurring order period
    else return HTTP 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        bottle = User.objects.get(username=username).recurring_order_bottle
        return JsonResponse({"bottle": bottle}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)

@api_view(["POST"])
def change_recurring_order_bottle(request):
    """
    check user request.data["username"] username. if user exists change reccuring order to request.data["new_bottle"] and return http 200
    if user not exists return http 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        user.recurring_order = request.data.get("new_bottle")
        user.save()
        return JsonResponse({"message": "success"}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


@api_view(["POST"])
def add_item_to_cart(request):
    """
    check user request.data["username"] username. if user exists add item (request.data["item"] will be like {"bottle":"15","type":"still"})
    to the user's cart and return http 200
    if user not exists return http 400
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        item = Cart.objects.create(user_id=user, bottle=request.data.get("bottle"), water_type=request.data.get("type"))
        return JsonResponse({"message": "success"}, status=200, safe=False)
    return JsonResponse({"message": "Invalid username or password."}, status=400)

@api_view(["POST"])
def remove_item_from_cart(request):
    """
    check user request.data["username"] username and request.data["item"]. if user exists and item in cart remove item 
    from the user's cart and return http 200
    if user does not exist or item not in cart return http 400
    (request.data will be like {"username":"test", "password":"test", "bottle":"15","type":"still"})
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if check_user(username) and check_password(username, password):
        user = User.objects.get(username=username)
        if Cart.objects.filter(user_id=user, bottle=request.data.get("bottle"), water_type=request.data.get("type")):
            item = Cart.objects.filter(user_id=user, bottle=request.data.get("bottle"), water_type=request.data.get("type")).first().delete()
            return JsonResponse({"message": "success"}, status=200, safe=False)
        return JsonResponse({"message": "Item not in cart."}, status=400)
    return JsonResponse({"message": "Invalid username or password."}, status=400)


def check_user(username) -> bool:
    print(username)
    if username is None:
        return False
    user = User.objects.filter(username=username).count()
    if user > 0:
        return True
    return False


def check_password(username, password) -> bool:
    if password is None or username is None:
        return False
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    user = User.objects.filter(username=username, password=hashed_password).count()
    if user > 0:
        return True
    return False
