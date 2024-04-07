from django.urls import path
from . import views

app_name = "kiosk"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("menu/", views.MenuList.as_view(), name="menu"),
    path("menu/order", views.MenuOrderList.as_view(), name="menu_order"),
    path("order/", views.MenuList.as_view(), name="order"),
    path("all/order/", views.MenuList.as_view(), name="all_order"),
]