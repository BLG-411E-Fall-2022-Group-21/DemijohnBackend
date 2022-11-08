from rest_framework import serializers
from .models import User, Cart, PreviousOrder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "cart",
            "previous_orders",
            "recurring_order",
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "bottle",
            "watter_type",
        ]


class PreviousOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousOrder
        fields = [
            "id",
            "bottle",
            "watter_type",
        ]
