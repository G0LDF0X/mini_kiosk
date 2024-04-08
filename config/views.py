from django.shortcuts import render, redirect
from django.http import HttpResponse
from kiosk.models import Customer
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        customer_password = request.POST['customer_password']
        
        try:
            customer = Customer.objects.get(customer_id=customer_id, customer_password=customer_password)
            # 로그인 성공 시 처리 로직, 예를 들어 세션에 사용자 정보 저장
            request.session['customer_id'] = customer.customer_id
            return redirect('home')  # 로그인 성공 후 리다이렉트할 페이지
        except Customer.DoesNotExist:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
