import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import get_db
from app import models, schemas
from app.core.security import get_current_active_user

router = APIRouter(
    prefix="/opportunities",
    tags=["opportunities"],
    dependencies=[Depends(get_current_active_user)],
)


def _opportunity_scope(query, user: models.User):
    scope = user.role_obj.record_access_scope if user.role_obj else "all"
    if scope == "own":
        return query.join(models.Account, models.Opportunity.account_id == models.Account.id).filter(
            models.Account.owner_id == user.id
        )
    if scope in ("team", "market"):
        return query.join(models.Account, models.Opportunity.account_id == models.Account.id).filter(
            models.Account.market_code == user.market_code
        )
    return query


@router.get("", response_model=List[schemas.OpportunityOut])
def list_opportunities(
    stage: Optional[str] = Query(None),
    q: Optional[str] = Query(None),
    region_code: Optional[str] = Query(None),
    user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    query = _opportunity_scope(db.query(models.Opportunity), user)
    if stage:
        query = query.filter(models.Opportunity.stage == stage)
    if region_code:
        query = query.filter(models.Opportunity.region_code.ilike(f"%{region_code}%"))
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                models.Opportunity.company_name.ilike(like),
                models.Opportunity.region_code.ilike(like),
                models.Opportunity.tags.ilike(like),
            )
        )
    return query.order_by(models.Opportunity.created_at.desc()).all()


@router.get("/{opportunity_id}", response_model=schemas.OpportunityOut)
def get_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp


@router.post("", response_model=schemas.OpportunityOut, status_code=201)
def create_opportunity(payload: schemas.OpportunityCreate, db: Session = Depends(get_db)):
    data = payload.model_dump(exclude_unset=True)
    if not data.get("id"):
        data["id"] = f"oc-{uuid.uuid4().hex[:8]}"
    opp = models.Opportunity(**data)
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp


@router.patch("/{opportunity_id}", response_model=schemas.OpportunityOut)
def update_opportunity(opportunity_id: str, payload: schemas.OpportunityUpdate, db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(opp, key, value)
    db.commit()
    db.refresh(opp)
    return opp


@router.delete("/{opportunity_id}", status_code=204)
def delete_opportunity(opportunity_id: str, db: Session = Depends(get_db)):
    opp = db.query(models.Opportunity).filter(models.Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    db.delete(opp)
    db.commit()
    return None
