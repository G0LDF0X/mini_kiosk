from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, DayArchiveView
from kiosk.models import Menu, Order, Current_Order
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Max

def Index(request):
    context = {"status": "OK"}
    return render(request, "kiosk/index.html", context)

def get_menu(request):
    menu_items = Menu.objects.all().order_by("-menu_category")
    return render(request, "kiosk/menu_list.html", {"menu_items": menu_items})

@csrf_exempt
@require_POST
def show_cart(request, menu_id):
    menu, created = Current_Order.objects.get_or_create(menu_id=menu_id, defaults={"menu_count": 0, "order_date": timezone.now()},)

    if not created:
        menu.menu_count = F("menu_count") + 1
    else:
        menu.menu_count = 1

    menu.save()
    cart_items = Current_Order.objects.all()
    menus = Menu.objects.all()
    total_sum = sum(menu.menu_price * order.menu_count for menu in menus for order in menu.current_order_set.all())
    context = {"cart_items": cart_items, "menu_id": menu_id, "menus": menus, "total_sum": total_sum}
    return render(request, "kiosk/menu_order.html", context)

def show_receipt(request):
    max_order_id = Order.objects.aggregate(max_order_id=Max('order_id'))["max_order_id"]
    current_order = Current_Order.objects.all().values("menu_count", "order_date", "menu_id")
    
    # Order 테이블에 데이터가 안 들어와 있는 경우
    if max_order_id == None:
        all_orders_to_add = []
        for order in current_order:
            new_order = Order(menu_count=order["menu_count"], order_id=1, order_date=order["order_date"], menu_id=order["menu_id"])
            all_orders_to_add.append(new_order)
            max_order_id = 1
        Order.objects.bulk_create(all_orders_to_add)
        Current_Order.objects.all().delete()
    
    # Order 테이블에 데이터는 있지만 Current_Order 테이블을 비운 뒤로 아직 주문이 안 들어왔을 경우
    elif not current_order.exists():
        print("신규 주문 없음")
    else:
        recently_order = Order.objects.filter(order_id=max_order_id).values("menu_count", "order_date", "menu_id")
        
        if list(recently_order) != list(current_order):
            all_orders_to_add = []
            for order in current_order:
                new_order = Order(menu_count=order["menu_count"], order_id=max_order_id+1, order_date=order["order_date"], menu_id=order["menu_id"])
                all_orders_to_add.append(new_order)
            Order.objects.bulk_create(all_orders_to_add)
            max_order_id += 1
            Current_Order.objects.all().delete()

    cart_items = Order.objects.filter(order_id=max_order_id).values("menu_count", "order_date", "menu_id")
    menus = Menu.objects.all()

    order_dict = {order["menu_id"]: order for order in cart_items}
    total_sum = sum(menu.menu_price * order_dict[menu.id]["menu_count"] for menu in menus if menu.id in order_dict)
    context = {"cart_items": cart_items, "menus": menus, "total_sum": total_sum, "max_order_id": max_order_id}
    return render(request, "kiosk/receipt_list.html", context)

class ReceiptDAV(DayArchiveView):
    model = Order
    data_field = "order_date"
    template_name = "kiosk/receipt_day_list.html"

class ReceiptList(ListView):
    model = Order
    template_name = "kiosk/all_order.html"
    context_object_name = "all_order"
