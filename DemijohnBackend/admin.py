from django.contrib import admin
from .models import User, Cart, PreviousOrder


admin.site.register(User)
admin.site.register(Cart)
admin.site.register(PreviousOrder)
