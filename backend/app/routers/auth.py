from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
from app.core.security import (
    create_access_token,
    decode_token,
    get_password_hash,
    verify_password,
    get_current_active_user,
    oauth2_scheme,
    user_permissions,
)
from app.schemas import LoginPayload, SwitchRolePayload, TokenOut, UserWithPermissions

router = APIRouter(prefix="/auth", tags=["auth"])


def _serialize_user(user: models.User, db: Session) -> UserWithPermissions:
    role = user.role_obj
    perms = user_permissions(user, db)
    return UserWithPermissions(
        id=user.id,
        name=user.name,
        email=user.email,
        role_code=user.role_code,
        department=user.department,
        market_code=user.market_code,
        avatar=user.avatar,
        status=user.status,
        role_name=role.name_zh or role.name_en if role else None,
        permissions=list(perms),
        record_access_scope=role.record_access_scope if role else None,
    )


@router.post("/login", response_model=TokenOut)
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not user.hashed_password or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if user.status != "active":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive")
    access_token = create_access_token({"sub": user.id, "role": user.role_code})
    return TokenOut(access_token=access_token, user=_serialize_user(user, db))


@router.post("/token", response_model=TokenOut)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 form endpoint for tools like Swagger UI
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not user.hashed_password or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.id, "role": user.role_code})
    return TokenOut(access_token=access_token, user=_serialize_user(user, db))


@router.get("/me", response_model=UserWithPermissions)
def me(user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return _serialize_user(user, db)


@router.post("/switch-role", response_model=TokenOut)
def switch_role(
    payload: SwitchRolePayload,
    user: models.User = Depends(get_current_active_user),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    # Permission is checked against the original user, not the currently previewed role.
    # The token carries the original role so that a previewed session can still switch back.
    payload_data = decode_token(token) or {}
    original_role_code = payload_data.get("original_role") or user.role_code
    original_role = db.query(models.Role).filter(models.Role.code == original_role_code).first()
    can_preview = False
    if original_role:
        if original_role.is_system:
            can_preview = True
        else:
            can_preview = (
                db.query(models.RolePermission)
                .filter_by(role_code=original_role.code, permission_code="accessSystemSettings", granted=True)
                .first()
                is not None
            )
    if not can_preview:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to preview roles")
    target_role = db.query(models.Role).filter(models.Role.code == payload.role_code).first()
    if not target_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    access_token = create_access_token(
        {"sub": user.id, "role": target_role.code, "preview": True, "original_role": original_role_code}
    )
    # temporarily attach target role for serialization
    previous_role = user.role_obj
    user.role_obj = target_role
    user.role_code = target_role.code
    result = TokenOut(access_token=access_token, user=_serialize_user(user, db))
    user.role_obj = previous_role
    user.role_code = previous_role.code if previous_role else None
    return result
