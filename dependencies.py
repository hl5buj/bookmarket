# dependencies.py
from fastapi import HTTPException, status

# 가짜 사용자 DB
users_db = {
    "admin@bookmarket.com": {
        "email": "admin@bookmarket.com",
        "name": "관리자",
        "role": "admin"
    },
    "user@bookmarket.com": {
        "email": "user@bookmarket.com",
        "name": "김독자",
        "role": "user"
    },
}

def get_current_user(email: str):
    """
    이메일로 현재 사용자 가져오기
    
    실무에서는 JWT 토큰을 사용하지만,
    여기서는 간단하게 이메일로 사용자를 식별합니다
    """
    user = users_db.get(email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다"
        )
    
    return user

def get_admin_user(email: str):
    """
    관리자 권한 확인
    """
    user = get_current_user(email)
    
    if user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    return user

def pagination_params(skip: int = 0, limit: int = 10):
    """
    페이지네이션 파라미터
    """
    if limit > 50:
        limit = 50  # 최대 50개까지만
    
    return {"skip": skip, "limit": limit}