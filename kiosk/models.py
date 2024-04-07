from django.db import models

# Create your models here.

# 음료의 이름, 가격이 적힌 테이블
class Menu(models.Model):
    menu_name = models.CharField(max_length=200)
    menu_price = models.IntegerField()
    menu_category = models.CharField(default="None", max_length=200) 

    def __str__(self):
        return self.menu_name

# 손님 테이블
# 주문 번호에 대응
class Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    order_type = models.CharField(max_length=200)

# 주문 테이블
# 주문 번호에 대한 음료 여럿이 들어가있음
class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField("order_date")

class Current_Customer(models.Model):
    customer_name = models.CharField(max_length=200)
    order_type = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)