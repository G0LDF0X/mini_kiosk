from django.contrib import admin
from .models import Menu, Order, Current_Order

# Register your models here.
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Current_Order)