"""DemijohnBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DemijohnBackend import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", views.signup),
    path("login/", views.login),
    path("get_previous_orders/", views.get_previous_orders),
    path("get_cart/", views.get_cart),
    path("get_user_address/", views.get_user_address),
    path("place_order/", views.place_order),
    path("change_address/", views.change_address),
    path("change_recurring_order_period/", views.change_recurring_order_period),
    path("change_recurring_order_bottle/", views.change_recurring_order_bottle),
    path("add_item_to_cart/", views.add_item_to_cart),
    path("remove_item_from_cart/", views.remove_item_from_cart),
    path("get_recurring_order_period/", views.get_recurring_order_period),
    path("get_recurring_order_bottle/", views.get_recurring_order_bottle),
    
]
