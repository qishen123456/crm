from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.core.security import get_current_active_user

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    dependencies=[Depends(get_current_active_user)],
)


def _account_scope(query, user: models.User):
    scope = user.role_obj.record_access_scope if user.role_obj else "all"
    if scope == "own":
        return query.filter(models.Account.owner_id == user.id)
    if scope in ("team", "market"):
        return query.filter(models.Account.market_code == user.market_code)
    # "distributor" / "all" => no additional filter
    return query


@router.get("", response_model=List[schemas.AccountOut])
def list_accounts(user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    query = _account_scope(db.query(models.Account), user)
    return query.order_by(models.Account.name).all()


@router.get("/{account_id}", response_model=schemas.AccountOut)
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.post("", response_model=schemas.AccountOut)
def create_account(payload: schemas.AccountCreate, db: Session = Depends(get_db)):
    if db.query(models.Account).filter(models.Account.id == payload.id).first():
        raise HTTPException(status_code=409, detail="Account id already exists")
    account = models.Account(**payload.model_dump(exclude_unset=True))
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.patch("/{account_id}", response_model=schemas.AccountOut)
def update_account(account_id: str, payload: schemas.AccountUpdate, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(account, key, value)
    db.commit()
    db.refresh(account)
    return account
