from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    previous_orders = models.ForeignKey(
        "PreviousOrder", on_delete=models.CASCADE, null=True
    )
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=50, default="")
    recurring_order = models.IntegerField(
        default=0
    )  # default 0 otherwise the frequency of the recurring order
    recurring_order_type = models.CharField(
        max_length=50, default=""
    )  # sparkling, still
    recurring_order_bottle = models.IntegerField(
        default=0
    )  # default 0 otherwise the number of bottle of the recurring order

    def __str__(self) -> str:
        return self.username


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    bottle = models.IntegerField()  # 5 10 15 30L
    water_type = models.CharField(max_length=50)  # still, sparkling

    def __str__(self) -> str:
        return f"User {self.id}: {self.bottle}L {self.water_type}"


class PreviousOrder(models.Model):
    id = models.AutoField(primary_key=True)
    bottle = models.IntegerField()  # 5 10 15 30L
    water_type = models.CharField(max_length=50)  # still, sparkling

    def __str__(self) -> str:
        return f"User {self.id}: {self.bottle}L {self.water_type}"
