from django.contrib import admin
from .models import Menu, Customer, Order

# Register your models here.
admin.site.register(Menu)
admin.site.register(Customer)
admin.site.register(Order)