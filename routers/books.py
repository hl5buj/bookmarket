# routers/books.py
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_admin_user, pagination_params

# 공개 라우터 (누구나 접근)
public_router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# 관리자 라우터 (관리자만 접근)
admin_router = APIRouter(
    prefix="/admin/books",
    tags=["books-admin"],
    dependencies=[Depends(get_admin_user)]  # 모든 엔드포인트에 관리자 확인
)

# 가짜 책 DB
books_db = [
    {"id": 1, "title": "파이썬 마스터하기", "category": "프로그래밍", "price": 35000, "stock": 50},
    {"id": 2, "title": "FastAPI 완벽 가이드", "category": "프로그래밍", "price": 42000, "stock": 30},
    {"id": 3, "title": "해리포터", "category": "소설", "price": 15000, "stock": 100},
]

# === 공개 API (누구나 접근) ===

@public_router.get("/")
def get_books(pagination: dict = Depends(pagination_params)):
    """
    책 목록 조회 (페이지네이션 적용)
    
    예시: GET /books?skip=0&limit=10
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    
    books = books_db[skip : skip + limit]
    
    return {
        "total": len(books_db),
        "skip": skip,
        "limit": limit,
        "books": books
    }

@public_router.get("/{book_id}")
def get_book(book_id: int):
    """특정 책 상세 조회"""
    for book in books_db:
        if book["id"] == book_id:
            return book
    
    raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")

@public_router.get("/search/category")
def search_by_category(
    category: str,
    pagination: dict = Depends(pagination_params)
):
    """
    카테고리별 검색
    
    예시: GET /books/search/category?category=프로그래밍
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    
    # 카테고리 필터링
    filtered = [b for b in books_db if b["category"] == category]
    
    # 페이지네이션
    results = filtered[skip : skip + limit]
    
    return {
        "category": category,
        "total": len(filtered),
        "results": results
    }

# === 관리자 API (관리자만 접근) ===

@admin_router.post("/")
def create_book(
    title: str,
    category: str,
    price: int,
    stock: int,
    email: str  # 관리자 이메일 (의존성으로 이미 검증됨)
):
    """
    새 책 등록 (관리자 전용)
    
    예시:
    POST /admin/books?email=admin@bookmarket.com
    Body: {"title": "...", "category": "...", "price": 30000, "stock": 50}
    """
    # 새 ID 생성
    new_id = max(b["id"] for b in books_db) + 1 if books_db else 1
    
    # 새 책 추가
    new_book = {
        "id": new_id,
        "title": title,
        "category": category,
        "price": price,
        "stock": stock
    }
    
    books_db.append(new_book)
    
    return {
        "message": "책 등록 완료",
        "book": new_book
    }

@admin_router.patch("/{book_id}/stock")
def update_stock(book_id: int, stock: int, email: str):
    """
    재고 수정 (관리자 전용)
    
    예시:
    PATCH /admin/books/1/stock?email=admin@bookmarket.com&stock=100
    """
    for book in books_db:
        if book["id"] == book_id:
            book["stock"] = stock
            return {
                "message": "재고 업데이트 완료",
                "book": book
            }
    
    raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")

@admin_router.delete("/{book_id}")
def delete_book(book_id: int, email: str):
    """
    책 삭제 (관리자 전용)
    
    예시:
    DELETE /admin/books/1?email=admin@bookmarket.com
    """
    global books_db
    
    original_len = len(books_db)
    books_db = [b for b in books_db if b["id"] != book_id]
    
    if len(books_db) == original_len:
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다")
    
    return {"message": f"책 {book_id} 삭제 완료"}