from django.shortcuts import render, redirect
from django.views.generic import ListView, DayArchiveView
from kiosk.models import Menu, Order, Current_Order, Category
from django.utils import timezone
from django.db.models import F
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

def Index(request):
    context = {"status": "OK"}
    return render(request, "kiosk/index.html", context)

def get_menu_category(request, pk):
    if request.method == 'GET':
        all_category = Category.objects.all()
        get_category_items = Menu.objects.filter(menu_category=pk)
        order_items = Current_Order.objects.all()
        menus = Menu.objects.all()
        total_sum = 0
        for order in order_items:
            total_sum += order.menu.menu_price * order.menu_count
        context = {
            "categories": all_category,
            "category_items": get_category_items,
            "order_items": order_items,
            "menus": menus,
            "current_page": pk,
            "total_sum": total_sum,
        }
        return render(request, "kiosk/menu_list.html", context)
    elif request.method == 'POST':
        menu_id = request.POST['menu_id']
        menu, created = Current_Order.objects.get_or_create(menu_id=menu_id, defaults={"menu_count": 0, "order_date": timezone.now()},)
        if not created:
            menu.menu_count = F("menu_count") + 1
        else:
            menu.menu_count = 1
        menu.save()
        return redirect('kiosk:menu_category', pk=pk)

def show_cart(request):

    cart_items = Current_Order.objects.all()
    menus = Menu.objects.all()
    total_sum = sum(menu.menu_price * order.menu_count for menu in menus for order in menu.current_order_set.all())
    context = {"cart_items": cart_items, "menus": menus, "total_sum": total_sum}
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

@login_required
def add_menu(request):
    if request.method == 'GET':
        return render(request, 'kiosk/add_menu.html')
    elif request.method == 'POST':
        menu_name = request.POST['name']
        menu_price = request.POST['price']
        menu_category = request.POST['category']

        Menu.objects.create(menu_name=menu_name, menu_price=menu_price, menu_category_id=menu_category)
        return redirect('kiosk:menu_category',pk=menu_category)

def detail_menu(request, pk):
    object = Menu.objects.get(pk=pk)
    context = {'object': object}
    return render(request, 'kiosk/menu_detail.html', context)

@login_required(login_url='/login/')
def delete_menu(request, pk):
    object = Menu.objects.get(pk=pk)
    item_id = object.menu_category.id
    object.delete()
    return redirect('kiosk:menu_category', pk=item_id)

class ReceiptDAV(DayArchiveView):
    model = Order
    data_field = "order_date"
    template_name = "kiosk/receipt_day_list.html"

class ReceiptList(ListView):
    model = Order
    template_name = "kiosk/all_order.html"
    context_object_name = "all_order"
