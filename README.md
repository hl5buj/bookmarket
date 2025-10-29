# 📚 BookMarket API

FastAPI 기반 온라인 서점 API - 학습 프로젝트

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)](https://www.python.org/)

## 📋 프로젝트 소개

FastAPI를 학습하기 위한 온라인 서점 API 프로젝트입니다.
책 조회, 주문, 관리자 기능을 포함한 RESTful API를 구현했습니다.

### 주요 기능

- 📖 **책 관리**: 목록 조회, 상세 조회, 카테고리별 검색
- 🛒 **주문 시스템**: 주문 생성, 주문 내역 조회, 재고 자동 관리
- 🔐 **관리자 기능**: 책 등록, 재고 수정, 책 삭제
- 📄 **API 문서**: Swagger UI 자동 생성

## 🚀 빠른 시작

### 설치

```bash
# 저장소 클론
git clone https://github.com/hl5buj/bookmarket.git
cd bookmarket

# 의존성 설치
pip install fastapi uvicorn
```

### 실행

```bash
# 개발 서버 실행
uvicorn main:app --reload

# 브라우저에서 접속
# API 문서: http://127.0.0.1:8000/docs
# 메인: http://127.0.0.1:8000/
```

## 📁 프로젝트 구조

```
bookmarket/
├── main.py              # FastAPI 앱 진입점
├── dependencies.py      # 공통 의존성 (인증, 페이지네이션)
├── routers/
│   ├── books.py        # 책 관련 API (공개 + 관리자)
│   └── orders.py       # 주문 관련 API
└── claudedocs/
    └── PROJECT_DOCUMENTATION.md  # 상세 문서
```

## 🔑 테스트 계정

```python
# 일반 사용자
email: user@bookmarket.com

# 관리자
email: admin@bookmarket.com
```

## 📖 API 엔드포인트

### 공개 API (인증 불필요)

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/books` | 책 목록 조회 (페이지네이션) |
| GET | `/books/{book_id}` | 책 상세 조회 |
| GET | `/books/search/category` | 카테고리별 검색 |

### 주문 API (로그인 필요)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/orders` | 주문 생성 |
| GET | `/orders/my-orders` | 내 주문 내역 조회 |

### 관리자 API (관리자 권한 필요)

| Method | Endpoint | 설명 |
|--------|----------|------|
| POST | `/admin/books` | 책 등록 |
| PATCH | `/admin/books/{book_id}/stock` | 재고 수정 |
| DELETE | `/admin/books/{book_id}` | 책 삭제 |

## 💡 사용 예시

### 책 목록 조회
```bash
curl http://127.0.0.1:8000/books?skip=0&limit=10
```

### 주문 생성
```bash
curl -X POST "http://127.0.0.1:8000/orders?email=user@bookmarket.com&book_id=1&quantity=2"
```

### 책 등록 (관리자)
```bash
curl -X POST "http://127.0.0.1:8000/admin/books?email=admin@bookmarket.com&title=새책&category=소설&price=20000&stock=100"
```

## 📚 문서

- **상세 문서**: [claudedocs/PROJECT_DOCUMENTATION.md](claudedocs/PROJECT_DOCUMENTATION.md)
- **API 문서**: http://127.0.0.1:8000/docs (서버 실행 후)

## 🛠️ 기술 스택

- **Framework**: FastAPI 0.100+
- **Server**: Uvicorn
- **Language**: Python 3.8+
- **API Documentation**: Swagger UI (자동 생성)

## ⚠️ 주의사항

이 프로젝트는 **학습 목적**으로 제작되었습니다.

**실제 배포 시 반드시 개선해야 할 사항**:
- ✅ JWT 토큰 기반 인증으로 변경
- ✅ 메모리 DB → 실제 데이터베이스 (PostgreSQL, MySQL)
- ✅ 비밀번호 해싱 및 보안 강화
- ✅ HTTPS 사용
- ✅ 에러 처리 및 로깅 시스템

## 📝 라이선스

학습 프로젝트 - 자유롭게 사용 가능

## 👤 작성자

- **GitHub**: [@hl5buj](https://github.com/hl5buj)
- **Email**: admin@bookmarket.com