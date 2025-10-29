# main.py
from fastapi import FastAPI
from routers import books, orders

app = FastAPI(
    title="북마켓 API",
    description="온라인 서점 API - 책 조회, 주문, 관리자 기능",
    version="1.0.0"
)

# 라우터 등록
app.include_router(books.public_router)    # 공개 책 API
app.include_router(books.admin_router)     # 관리자 책 API
app.include_router(orders.router)          # 주문 API

@app.get("/")
def root():
    return {
        "message": "북마켓 API에 오신 것을 환영합니다!",
        "docs": "http://127.0.0.1:8000/docs",
        "users": {
            "admin": "admin@bookmarket.com",
            "user": "user@bookmarket.com"
        }
    }