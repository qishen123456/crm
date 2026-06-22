from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app import models, schemas

router = APIRouter(prefix="/markets", tags=["markets"])


@router.get("", response_model=List[schemas.MarketOut])
def list_markets(db: Session = Depends(get_db)):
    return db.query(models.Market).order_by(models.Market.code).all()
