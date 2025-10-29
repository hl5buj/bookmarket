# routers/orders.py
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_current_user
from routers.books import books_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

# 가짜 주문 DB
orders_db = []

@router.post("/")
def create_order(
    book_id: int,
    quantity: int,
    user: dict = Depends(get_current_user)
):
    """
    주문 생성 (로그인 필요)
    
    예시:
    POST /orders?email=user@bookmarket.com&book_id=1&quantity=2
    """
    # 책 찾기
    book = None
    for b in books_db:
        if b["id"] == book_id:
            book = b
            break
    
    if not book:
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")
    
    # 재고 확인
    if book["stock"] < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"재고가 부족합니다 (현재 재고: {book['stock']})"
        )
    
    # 주문 생성
    order_id = len(orders_db) + 1
    order = {
        "id": order_id,
        "user_email": user["email"],
        "book_id": book_id,
        "book_title": book["title"],
        "quantity": quantity,
        "total_price": book["price"] * quantity,
        "status": "주문완료"
    }
    
    orders_db.append(order)
    
    # 재고 감소
    book["stock"] -= quantity
    
    return {
        "message": "주문이 완료되었습니다",
        "order": order
    }

@router.get("/my-orders")
def get_my_orders(user: dict = Depends(get_current_user)):
    """
    내 주문 내역 조회 (로그인 필요)
    
    예시:
    GET /orders/my-orders?email=user@bookmarket.com
    """
    # 현재 사용자의 주문만 필터링
    my_orders = [
        o for o in orders_db 
        if o["user_email"] == user["email"]
    ]
    
    return {
        "user": user["name"],
        "total_orders": len(my_orders),
        "orders": my_orders
    }