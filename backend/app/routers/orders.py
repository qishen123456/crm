from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.core.security import get_current_active_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_active_user)],
)


def _order_scope(query, user: models.User):
    scope = user.role_obj.record_access_scope if user.role_obj else "all"
    if scope == "own":
        return query.filter(models.Order.requested_by_id == user.id)
    if scope in ("team", "market"):
        return query.join(models.Account, models.Order.account_id == models.Account.id).filter(
            models.Account.market_code == user.market_code
        )
    return query


@router.get("", response_model=List[schemas.OrderOut])
def list_orders(user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    query = _order_scope(db.query(models.Order), user)
    return query.order_by(models.Order.created_at.desc()).all()


@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=schemas.OrderOut, status_code=201)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    if db.query(models.Order).filter(models.Order.id == payload.id).first():
        raise HTTPException(status_code=409, detail="Order id already exists")
    data = payload.model_dump(exclude_unset=True)
    items = data.pop("items", [])
    order = models.Order(**data)
    for idx, it in enumerate(items):
        it_data = it.model_dump() if hasattr(it, "model_dump") else it
        order.items.append(models.OrderItem(
            id=f"{order.id}-i{idx}",
            sku=it_data.get("sku", ""),
            name=it_data.get("name", ""),
            qty=it_data.get("qty", 1),
            unit_price_usd=it_data.get("unit_price_usd"),
        ))
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.patch("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: str, payload: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    data = payload.model_dump(exclude_unset=True)
    items = data.pop("items", None)
    for key, value in data.items():
        setattr(order, key, value)
    if items is not None:
        order.items = []
        for idx, it in enumerate(items):
            it_data = it.model_dump() if hasattr(it, "model_dump") else it
            order.items.append(models.OrderItem(
                id=f"{order.id}-i{idx}",
                sku=it_data.get("sku", ""),
                name=it_data.get("name", ""),
                qty=it_data.get("qty", 1),
                unit_price_usd=it_data.get("unit_price_usd"),
            ))
    db.commit()
    db.refresh(order)
    return order
