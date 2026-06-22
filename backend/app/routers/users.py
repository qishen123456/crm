from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas
from app.core.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[schemas.UserOut])
def list_users(
    db: Session = Depends(get_db),
    _=Depends(get_current_active_user),
):
    return db.query(models.User).order_by(models.User.name).all()
