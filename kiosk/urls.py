from django.urls import path
from . import views

app_name = "kiosk"
urlpatterns = [
    path("", views.Index, name="index"),
    # 메뉴 및 주문
    path("menu/", views.get_menu, name="menu"),
    path("menu/<int:menu_id>/", views.show_cart, name="menu_order"),
    # 영수증 조회
    path("receipt/", views.show_receipt, name="receipt"),
    path("all/receipt/", views.ReceiptList.as_view(), name="all_receipt"),
    path("all/receipt/date", views.ReceiptDAV.as_view(), name="all_receipt_date"),
    path("all/receipt/date/<int:year>/<int:month>/<int:day>", views.ReceiptDAV.as_view(), name="all_receipt_date_detail"),
    path("all/receipt/id", views.ReceiptList.as_view(), name="all_receipt"),
    path("all/receipt/id/<int:order_id>", views.ReceiptList.as_view(), name="all_receipt"),
]