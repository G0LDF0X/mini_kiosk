from django.db import models

# Create your models here.

# 음료의 이름, 가격이 적힌 테이블
class Menu(models.Model):
    menu_name = models.CharField(max_length=200)
    menu_price = models.IntegerField()
    menu_category = models.CharField(default="None", max_length=200) 

    def __str__(self):
        return self.menu_name
    
class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_count = models.IntegerField(default=0)
    order_id = models.IntegerField(default=1)
    order_date = models.DateTimeField("order_date")

    def __str__(self):
        return self.menu.menu_name

# 장바구니
class Current_Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu_count = models.IntegerField(default=0)
    order_date = models.DateTimeField("order_date", null=True)

    def __str__(self):
        return self.menu.menu_name