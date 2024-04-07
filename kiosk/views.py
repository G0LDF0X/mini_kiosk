from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from kiosk.models import Menu, Order, Customer, Current_Customer

class MenuList(ListView):
    model = Menu
    template_name = "kiosk/menu_list.html"
    context_object_name = "menu_list"

class MenuOrderList(DetailView):
    model = Menu
    template_name = "kiosk/menu_order.html"
    context_object_name = "menu_order"

class Index(ListView):
    model = Current_Customer
    template_name = "kiosk/index.html"
    context_object_name = "object"

class OrderList(DetailView):
    model = Order
    template_name = "kiosk/order.html"
    context_object_name = "order"

class All_OrderList(ListView):
    model = Order
    template_name = "kiosk/all_order.html"
    context_object_name = "all_order"

class ChangePay(DetailView):
    model = Customer