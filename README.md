# mini_kiosk

해당 프로젝트는 카페의 미니 키오스크를 구현하고자 한다.

DB는 음료 데이터를 담고 있는 ``Menu``와 주문 데이터를 담고 있는 ``Order``, 그리고 손님 데이터를 담고 있는 ``Customer``로 이루어져 있다.

## Menu

``Menu`` 테이블은 ``menu_name``, ``menu_price``, ``menu_category`` 컬럼으로 이루어져 있다.

``menu_name``에는 문자형으로 메뉴 이름이 들어가며, ``menu_price``는 정수형으로 해당 메뉴의 가격, ``menu_category``는 문자형으로 메뉴의 분류를 담고 있다.


## Customer

``Customer`` 테이블은 ``customer_name``, ``order_type`` 컬럼으로 이루어져 있다.

``customer_name``에는 문자형으로 고객 이름이 들어가며, ``order_type``에는 문자형으로 결제 방식이 들어간다.


## Order

``Order`` 테이블은 ``order_date``와 함께 외래키로 ``customer_id``, ``menu_id``를 가진다.

``order_date``에는 날짜형으로 주문한 시각이 들어가며, ``customer_id``는 어떤 고객이 주문했는지, ``menu_id``는 어떤 메뉴를 주문했는지 외래키로 작성한다.