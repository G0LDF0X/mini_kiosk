from django.urls import path
from . import views

app_name = "kiosk"
urlpatterns = [
    path("", views.Index, name="index"),
    # 메뉴 및 주문
    path("menu/<int:pk>/", views.get_menu_category, name="menu_category"),
    path("order/", views.show_cart, name="order"),
    # 영수증 조회
    path("receipt/", views.show_receipt, name="receipt"),
    path("all/receipt/", views.ReceiptList.as_view(), name="all_receipt"),
    path("all/receipt/date", views.ReceiptDAV.as_view(), name="all_receipt_date"),
    path("all/receipt/date/<int:year>/<int:month>/<int:day>", views.ReceiptDAV.as_view(), name="all_receipt_date_detail"),
    path("all/receipt/id", views.ReceiptList.as_view(), name="all_receipt"),
    path("all/receipt/id/<int:order_id>", views.ReceiptList.as_view(), name="all_receipt"),
    
    path("add_menu/", views.add_menu, name="add_menu"),
    path("detail_menu/<int:pk>/", views.detail_menu, name="detail_menu"),
    path("delete_menu/<int:pk>/", views.delete_menu, name="delete_menu"),
]