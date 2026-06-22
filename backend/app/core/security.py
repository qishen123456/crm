import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db import get_db
from app import models

SECRET_KEY = os.getenv("SECRET_KEY", "angelcrm-dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", "7"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def _apply_preview_role(user: models.User, payload: dict, db: Session) -> models.User:
    """If the token represents a role preview, temporarily attach the target role
    to the user object so that permissions and serialization reflect the preview."""
    preview_role_code = payload.get("role")
    if payload.get("preview") and preview_role_code:
        preview_role = db.query(models.Role).filter(models.Role.code == preview_role_code).first()
        if preview_role:
            user.role_code = preview_role.code
            user.role_obj = preview_role
    return user


def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[models.User]:
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    return _apply_preview_role(user, payload, db)


def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    user = get_current_user_optional(token, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", headers={"WWW-Authenticate": "Bearer"})
    return user


def get_current_active_user(user: models.User = Depends(get_current_user)) -> models.User:
    if user.status != "active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
    return user


def user_permissions(user: models.User, db: Session) -> set[str]:
    if user.role and user.role.is_system:
        return {p.code for p in db.query(models.Permission).all()}
    granted = db.query(models.RolePermission.permission_code).filter(
        models.RolePermission.role_code == user.role_code,
        models.RolePermission.granted == True,
    ).all()
    return {p[0] for p in granted}


def require_permission(permission_code: str):
    def checker(user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
        perms = user_permissions(user, db)
        if permission_code not in perms:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Missing permission: {permission_code}")
        return user
    return checker
