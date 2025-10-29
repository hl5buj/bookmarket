# BookMarket API - 프로젝트 종합 문서

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [시스템 아키텍처](#시스템-아키텍처)
3. [설치 및 실행](#설치-및-실행)
4. [API 엔드포인트](#api-엔드포인트)
5. [컴포넌트 상세](#컴포넌트-상세)
6. [데이터 구조](#데이터-구조)
7. [인증 및 권한](#인증-및-권한)
8. [개발 가이드](#개발-가이드)

---

## 프로젝트 개요

### 📌 프로젝트 정보
- **이름**: BookMarket API
- **버전**: 1.0.0
- **설명**: 온라인 서점 API - 책 조회, 주문, 관리자 기능
- **프레임워크**: FastAPI
- **목적**: FastAPI 학습 및 실습

### 🎯 주요 기능
- **책 관리**: 책 조회, 검색, 카테고리별 필터링
- **주문 시스템**: 주문 생성, 주문 내역 조회
- **관리자 기능**: 책 등록, 재고 관리, 책 삭제
- **사용자 인증**: 이메일 기반 간단 인증 (학습용)

---

## 시스템 아키텍처

### 📁 프로젝트 구조
```
bookmarket/
├── main.py              # FastAPI 애플리케이션 진입점
├── dependencies.py      # 공통 의존성 (인증, 페이지네이션)
├── routers/
│   ├── __init__.py
│   ├── books.py        # 책 관련 API (공개 + 관리자)
│   └── orders.py       # 주문 관련 API
├── claudedocs/         # 프로젝트 문서
└── README.md           # 프로젝트 소개
```

### 🏗️ 계층 구조
```
┌─────────────────────────────────────┐
│         main.py (진입점)             │
│   - FastAPI 앱 생성                 │
│   - 라우터 등록                      │
└────────────┬────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌────▼─────┐
│ books  │      │ orders   │
│ router │      │ router   │
└───┬────┘      └────┬─────┘
    │                │
    └────────┬───────┘
             │
    ┌────────▼────────┐
    │ dependencies.py │
    │  - 인증         │
    │  - 페이지네이션  │
    └─────────────────┘
```

---

## 설치 및 실행

### 📦 필수 요구사항
```bash
Python 3.8+
FastAPI
Uvicorn
```

### 🚀 설치 방법
```bash
# 1. 저장소 클론
git clone https://github.com/hl5buj/bookmarket.git
cd bookmarket

# 2. 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install fastapi uvicorn
```

### ▶️ 실행 방법
```bash
# 개발 서버 실행
uvicorn main:app --reload

# 실행 완료 후 접속
# - API 문서: http://127.0.0.1:8000/docs
# - 루트: http://127.0.0.1:8000/
```

---

## API 엔드포인트

### 🌐 기본 정보
- **Base URL**: `http://127.0.0.1:8000`
- **API 문서**: `http://127.0.0.1:8000/docs` (Swagger UI)

### 📚 Books API (공개)

#### 1. 책 목록 조회
```http
GET /books?skip=0&limit=10
```
**설명**: 모든 책 목록을 페이지네이션하여 조회

**Query Parameters**:
- `skip` (int, optional): 건너뛸 항목 수 (기본값: 0)
- `limit` (int, optional): 가져올 항목 수 (기본값: 10, 최대: 50)

**Response**:
```json
{
  "total": 3,
  "skip": 0,
  "limit": 10,
  "books": [
    {
      "id": 1,
      "title": "파이썬 마스터하기",
      "category": "프로그래밍",
      "price": 35000,
      "stock": 50
    }
  ]
}
```

#### 2. 책 상세 조회
```http
GET /books/{book_id}
```
**설명**: 특정 책의 상세 정보 조회

**Path Parameters**:
- `book_id` (int): 책 ID

**Response**:
```json
{
  "id": 1,
  "title": "파이썬 마스터하기",
  "category": "프로그래밍",
  "price": 35000,
  "stock": 50
}
```

#### 3. 카테고리별 검색
```http
GET /books/search/category?category=프로그래밍&skip=0&limit=10
```
**설명**: 특정 카테고리의 책만 필터링하여 조회

**Query Parameters**:
- `category` (str): 카테고리 이름
- `skip` (int, optional): 건너뛸 항목 수
- `limit` (int, optional): 가져올 항목 수

**Response**:
```json
{
  "category": "프로그래밍",
  "total": 2,
  "results": [
    {
      "id": 1,
      "title": "파이썬 마스터하기",
      "category": "프로그래밍",
      "price": 35000,
      "stock": 50
    }
  ]
}
```

### 🔐 Books API (관리자 전용)

#### 4. 책 등록
```http
POST /admin/books?email=admin@bookmarket.com&title=...&category=...&price=30000&stock=50
```
**설명**: 새로운 책을 시스템에 등록 (관리자 권한 필요)

**Query Parameters**:
- `email` (str): 관리자 이메일
- `title` (str): 책 제목
- `category` (str): 카테고리
- `price` (int): 가격
- `stock` (int): 재고 수량

**Response**:
```json
{
  "message": "책 등록 완료",
  "book": {
    "id": 4,
    "title": "새로운 책",
    "category": "소설",
    "price": 30000,
    "stock": 50
  }
}
```

#### 5. 재고 수정
```http
PATCH /admin/books/{book_id}/stock?email=admin@bookmarket.com&stock=100
```
**설명**: 특정 책의 재고 수량 업데이트

**Path Parameters**:
- `book_id` (int): 책 ID

**Query Parameters**:
- `email` (str): 관리자 이메일
- `stock` (int): 새로운 재고 수량

**Response**:
```json
{
  "message": "재고 업데이트 완료",
  "book": {
    "id": 1,
    "title": "파이썬 마스터하기",
    "category": "프로그래밍",
    "price": 35000,
    "stock": 100
  }
}
```

#### 6. 책 삭제
```http
DELETE /admin/books/{book_id}?email=admin@bookmarket.com
```
**설명**: 시스템에서 책 삭제

**Path Parameters**:
- `book_id` (int): 책 ID

**Query Parameters**:
- `email` (str): 관리자 이메일

**Response**:
```json
{
  "message": "책 1 삭제 완료"
}
```

### 🛒 Orders API

#### 7. 주문 생성
```http
POST /orders?email=user@bookmarket.com&book_id=1&quantity=2
```
**설명**: 새로운 주문 생성 (로그인 필요)

**Query Parameters**:
- `email` (str): 사용자 이메일
- `book_id` (int): 주문할 책 ID
- `quantity` (int): 주문 수량

**Response**:
```json
{
  "message": "주문이 완료되었습니다",
  "order": {
    "id": 1,
    "user_email": "user@bookmarket.com",
    "book_id": 1,
    "book_title": "파이썬 마스터하기",
    "quantity": 2,
    "total_price": 70000,
    "status": "주문완료"
  }
}
```

#### 8. 내 주문 내역 조회
```http
GET /orders/my-orders?email=user@bookmarket.com
```
**설명**: 현재 사용자의 모든 주문 내역 조회

**Query Parameters**:
- `email` (str): 사용자 이메일

**Response**:
```json
{
  "user": "김독자",
  "total_orders": 1,
  "orders": [
    {
      "id": 1,
      "user_email": "user@bookmarket.com",
      "book_id": 1,
      "book_title": "파이썬 마스터하기",
      "quantity": 2,
      "total_price": 70000,
      "status": "주문완료"
    }
  ]
}
```

---

## 컴포넌트 상세

### 📄 main.py
**역할**: FastAPI 애플리케이션의 진입점

**주요 기능**:
- FastAPI 앱 인스턴스 생성 및 메타데이터 설정
- 라우터 등록 (books 공개/관리자, orders)
- 루트 엔드포인트 제공 (환영 메시지 및 사용자 정보)

**코드 위치**: `main.py:1-25`

**라우터 등록 순서**:
1. `books.public_router` - 공개 책 API
2. `books.admin_router` - 관리자 책 API
3. `orders.router` - 주문 API

---

### 🔧 dependencies.py
**역할**: 공통 의존성 함수 및 데이터베이스 모킹

**주요 컴포넌트**:

#### 1. `users_db` (dict)
**설명**: 가짜 사용자 데이터베이스
**위치**: `dependencies.py:5-16`
**데이터**:
- `admin@bookmarket.com`: 관리자 계정
- `user@bookmarket.com`: 일반 사용자 계정

#### 2. `get_current_user(email: str)`
**설명**: 이메일로 사용자 조회 및 인증
**위치**: `dependencies.py:18-33`
**반환**: 사용자 딕셔너리 또는 401 에러

#### 3. `get_admin_user(email: str)`
**설명**: 관리자 권한 확인
**위치**: `dependencies.py:35-47`
**반환**: 관리자 사용자 또는 403 에러

#### 4. `pagination_params(skip: int = 0, limit: int = 10)`
**설명**: 페이지네이션 파라미터 검증
**위치**: `dependencies.py:49-56`
**제한**: 최대 limit는 50
**반환**: `{"skip": skip, "limit": limit}`

---

### 📚 routers/books.py
**역할**: 책 관련 API 엔드포인트

**라우터 구조**:
- `public_router`: `/books` prefix, 누구나 접근
- `admin_router`: `/admin/books` prefix, 관리자만 접근

**데이터베이스**: `books_db` (list)
**초기 데이터**:
- 파이썬 마스터하기 (프로그래밍, 35,000원, 재고 50)
- FastAPI 완벽 가이드 (프로그래밍, 42,000원, 재고 30)
- 해리포터 (소설, 15,000원, 재고 100)

**공개 엔드포인트**:
- `GET /books` - 책 목록 조회 (`books.py:27-44`)
- `GET /books/{book_id}` - 책 상세 조회 (`books.py:46-53`)
- `GET /books/search/category` - 카테고리 검색 (`books.py:55-78`)

**관리자 엔드포인트**:
- `POST /admin/books` - 책 등록 (`books.py:82-114`)
- `PATCH /admin/books/{book_id}/stock` - 재고 수정 (`books.py:116-132`)
- `DELETE /admin/books/{book_id}` - 책 삭제 (`books.py:134-150`)

---

### 🛒 routers/orders.py
**역할**: 주문 관련 API 엔드포인트

**라우터 구조**:
- `router`: `/orders` prefix, 로그인 사용자만 접근

**데이터베이스**: `orders_db` (list)
**외부 참조**: `books_db` (routers.books에서 임포트)

**엔드포인트**:

#### 1. `POST /orders` - 주문 생성
**위치**: `orders.py:14-63`
**로직**:
1. 책 존재 여부 확인
2. 재고 충분 여부 확인
3. 주문 생성 및 저장
4. 책 재고 감소

**비즈니스 규칙**:
- 재고가 부족하면 400 에러
- 존재하지 않는 책이면 404 에러
- 주문 완료 시 자동으로 재고 차감

#### 2. `GET /orders/my-orders` - 내 주문 내역
**위치**: `orders.py:65-83`
**로직**:
1. 현재 사용자 인증
2. 사용자의 주문만 필터링
3. 주문 목록 반환

---

## 데이터 구조

### 📦 Book (책)
```python
{
  "id": int,           # 책 고유 ID
  "title": str,        # 책 제목
  "category": str,     # 카테고리 (예: "프로그래밍", "소설")
  "price": int,        # 가격 (원)
  "stock": int         # 재고 수량
}
```

### 📦 Order (주문)
```python
{
  "id": int,              # 주문 고유 ID
  "user_email": str,      # 주문한 사용자 이메일
  "book_id": int,         # 주문한 책 ID
  "book_title": str,      # 주문한 책 제목 (스냅샷)
  "quantity": int,        # 주문 수량
  "total_price": int,     # 총 가격 (price × quantity)
  "status": str           # 주문 상태 (예: "주문완료")
}
```

### 📦 User (사용자)
```python
{
  "email": str,        # 사용자 이메일 (고유 식별자)
  "name": str,         # 사용자 이름
  "role": str          # 역할 ("admin" 또는 "user")
}
```

---

## 인증 및 권한

### 🔐 인증 방식
**현재 구현**: 간단 이메일 기반 인증 (학습용)
**실무 권장**: JWT 토큰 기반 인증

### 👤 사용자 역할

#### 1. 일반 사용자 (user)
**이메일**: `user@bookmarket.com`
**권한**:
- ✅ 책 목록 조회
- ✅ 책 상세 조회
- ✅ 카테고리 검색
- ✅ 주문 생성
- ✅ 내 주문 내역 조회
- ❌ 책 등록/수정/삭제

#### 2. 관리자 (admin)
**이메일**: `admin@bookmarket.com`
**권한**:
- ✅ 모든 일반 사용자 권한
- ✅ 책 등록
- ✅ 재고 수정
- ✅ 책 삭제

### 🛡️ 권한 체크 메커니즘

#### 의존성 주입을 통한 권한 검증
```python
# 로그인 필요
user = Depends(get_current_user)

# 관리자 권한 필요
user = Depends(get_admin_user)

# 라우터 레벨 의존성 (모든 엔드포인트에 적용)
admin_router = APIRouter(
    dependencies=[Depends(get_admin_user)]
)
```

---

## 개발 가이드

### 🔧 새로운 엔드포인트 추가하기

#### 1. 공개 엔드포인트 추가
```python
# routers/books.py
@public_router.get("/new-endpoint")
def new_public_endpoint():
    return {"message": "누구나 접근 가능"}
```

#### 2. 인증 필요 엔드포인트 추가
```python
# routers/orders.py
@router.get("/protected")
def protected_endpoint(user: dict = Depends(get_current_user)):
    return {"message": f"안녕하세요, {user['name']}님"}
```

#### 3. 관리자 전용 엔드포인트 추가
```python
# routers/books.py
@admin_router.post("/admin-only")
def admin_endpoint(email: str):
    # email 파라미터로 자동 관리자 검증됨
    return {"message": "관리자 전용"}
```

### 📝 새로운 라우터 추가하기

```python
# 1. routers/reviews.py 생성
from fastapi import APIRouter

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.get("/")
def get_reviews():
    return {"reviews": []}

# 2. main.py에 라우터 등록
from routers import reviews
app.include_router(reviews.router)
```

### 🧪 API 테스트 방법

#### Swagger UI 사용 (권장)
```
1. http://127.0.0.1:8000/docs 접속
2. 테스트할 엔드포인트 선택
3. "Try it out" 클릭
4. 파라미터 입력 후 "Execute"
```

#### curl 사용
```bash
# 책 목록 조회
curl http://127.0.0.1:8000/books

# 주문 생성
curl -X POST "http://127.0.0.1:8000/orders?email=user@bookmarket.com&book_id=1&quantity=2"

# 책 등록 (관리자)
curl -X POST "http://127.0.0.1:8000/admin/books?email=admin@bookmarket.com&title=신간&category=소설&price=20000&stock=100"
```

### 🐛 디버깅 팁

#### 1. 로그 확인
Uvicorn 콘솔에서 실시간 요청/응답 로그 확인

#### 2. Interactive API Docs
`/docs`에서 각 엔드포인트의 스키마 및 예제 확인

#### 3. 일반적인 에러

**401 Unauthorized**
- 원인: 이메일이 users_db에 없음
- 해결: `admin@bookmarket.com` 또는 `user@bookmarket.com` 사용

**403 Forbidden**
- 원인: 일반 사용자가 관리자 API 접근
- 해결: `admin@bookmarket.com`으로 요청

**404 Not Found**
- 원인: 존재하지 않는 book_id
- 해결: `/books`로 존재하는 ID 확인 후 사용

**400 Bad Request (재고 부족)**
- 원인: 주문 수량이 재고보다 많음
- 해결: 책 상세 조회로 재고 확인 후 적절한 수량 주문

### 🚀 프로덕션 배포 시 고려사항

⚠️ **현재 코드는 학습용입니다. 실제 배포 시 다음을 반드시 개선하세요:**

1. **인증 시스템**
   - JWT 토큰 기반 인증으로 변경
   - 비밀번호 해싱 (bcrypt)
   - 세션 관리

2. **데이터베이스**
   - 메모리 DB → PostgreSQL/MySQL
   - ORM (SQLAlchemy) 사용
   - 마이그레이션 관리

3. **보안**
   - HTTPS 사용
   - CORS 설정
   - Rate limiting
   - Input validation

4. **성능**
   - 캐싱 (Redis)
   - 데이터베이스 인덱싱
   - 페이지네이션 최적화

5. **모니터링**
   - 로깅 시스템
   - 에러 트래킹
   - 성능 모니터링

---

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [FastAPI 한글 문서](https://fastapi.tiangolo.com/ko/)
- [Uvicorn 문서](https://www.uvicorn.org/)
- [Pydantic 문서](https://docs.pydantic.dev/)

---

**문서 버전**: 1.0.0
**최종 수정일**: 2025-10-29
**작성자**: Claude Code
