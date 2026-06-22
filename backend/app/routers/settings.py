from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models
from app.core.security import require_permission
from app.schemas import RoleOut, RoleUpdate

router = APIRouter(prefix="/settings", tags=["settings"])


def _role_out(role: models.Role, db: Session) -> RoleOut:
    granted = {
        rp.permission_code: rp.granted
        for rp in db.query(models.RolePermission).filter(models.RolePermission.role_code == role.code).all()
    }
    permissions = [
        {"permission_code": p.code, "granted": granted.get(p.code, False)}
        for p in db.query(models.Permission).order_by(models.Permission.sort_order).all()
    ]
    return RoleOut(
        code=role.code,
        name_en=role.name_en,
        name_zh=role.name_zh,
        record_access_scope=role.record_access_scope,
        is_system=role.is_system,
        sort_order=role.sort_order,
        is_active=role.is_active,
        permissions=permissions,
    )


@router.get("/roles", response_model=List[RoleOut])
def list_roles(
    db: Session = Depends(get_db),
    _=Depends(require_permission("accessSystemSettings")),
):
    roles = db.query(models.Role).order_by(models.Role.sort_order).all()
    return [_role_out(r, db) for r in roles]


@router.patch("/roles/{role_code}", response_model=RoleOut)
def update_role(
    role_code: str,
    payload: RoleUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("accessSystemSettings")),
):
    role = db.query(models.Role).filter(models.Role.code == role_code).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    if role.is_system:
        raise HTTPException(status_code=403, detail="System role cannot be modified")

    if payload.record_access_scope is not None:
        role.record_access_scope = payload.record_access_scope

    if payload.permissions is not None:
        existing = {
            rp.permission_code: rp
            for rp in db.query(models.RolePermission).filter(models.RolePermission.role_code == role_code).all()
        }
        for perm_code, granted in payload.permissions.items():
            if perm_code in existing:
                existing[perm_code].granted = bool(granted)
            else:
                db.add(models.RolePermission(role_code=role_code, permission_code=perm_code, granted=bool(granted)))

    db.commit()
    db.refresh(role)
    return _role_out(role, db)
