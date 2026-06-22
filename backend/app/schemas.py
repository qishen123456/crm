from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MarketOut(BaseModel):
    code: str
    name: str
    flag: str

    model_config = ConfigDict(from_attributes=True)


class PermissionOut(BaseModel):
    code: str
    name_en: str
    name_zh: Optional[str] = None
    category: Optional[str] = None
    sort_order: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RolePermissionOut(BaseModel):
    permission_code: str
    granted: bool

    model_config = ConfigDict(from_attributes=True)


class RoleOut(BaseModel):
    code: str
    name_en: str
    name_zh: Optional[str] = None
    record_access_scope: str
    is_system: bool
    sort_order: int
    is_active: bool
    permissions: List[RolePermissionOut] = []

    model_config = ConfigDict(from_attributes=True)


class RoleUpdate(BaseModel):
    record_access_scope: Optional[str] = None
    permissions: Optional[dict[str, bool]] = None


class UserOut(BaseModel):
    id: str
    name: str
    email: str
    role_code: Optional[str] = None
    department: str
    market_code: Optional[str] = None
    avatar: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class UserWithPermissions(UserOut):
    role_name: Optional[str] = None
    permissions: List[str] = []
    record_access_scope: Optional[str] = None


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserWithPermissions


class LoginPayload(BaseModel):
    email: str
    password: str


class SwitchRolePayload(BaseModel):
    role_code: str


class AccountOut(BaseModel):
    id: str
    code: str
    name: str
    market_code: Optional[str] = None
    owner_id: Optional[str] = None
    annual_target_usd: Optional[Decimal] = None
    year_to_date_usd: Optional[Decimal] = None
    contract_status: Optional[str] = None
    contract_expires_at: Optional[datetime] = None
    business_type: Optional[str] = None
    opportunity_notes: Optional[str] = None
    customer_resources: Optional[str] = None
    next_dig_directions: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AccountCreate(BaseModel):
    id: str
    code: str
    name: str
    market_code: Optional[str] = None
    owner_id: Optional[str] = None
    annual_target_usd: Optional[float] = None
    year_to_date_usd: Optional[float] = None
    contract_status: Optional[str] = "active"
    contract_expires_at: Optional[datetime] = None
    business_type: Optional[str] = None
    opportunity_notes: Optional[str] = None
    customer_resources: Optional[str] = None
    next_dig_directions: Optional[str] = None


class AccountUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    market_code: Optional[str] = None
    owner_id: Optional[str] = None
    annual_target_usd: Optional[float] = None
    year_to_date_usd: Optional[float] = None
    contract_status: Optional[str] = None
    contract_expires_at: Optional[datetime] = None
    business_type: Optional[str] = None
    opportunity_notes: Optional[str] = None
    customer_resources: Optional[str] = None
    next_dig_directions: Optional[str] = None


class OpportunityOut(BaseModel):
    id: str
    account_id: str
    company_name: str
    region_code: str
    tags: str
    amount: str
    owner_name: str
    stage: str
    is_no_follow_up: bool
    win_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class OpportunityCreate(BaseModel):
    id: Optional[str] = None
    account_id: str
    company_name: str
    region_code: Optional[str] = ""
    tags: Optional[str] = ""
    amount: Optional[str] = ""
    owner_name: Optional[str] = ""
    stage: Optional[str] = "prospect"
    is_no_follow_up: Optional[bool] = False
    win_type: Optional[str] = None


class OpportunityUpdate(BaseModel):
    account_id: Optional[str] = None
    company_name: Optional[str] = None
    region_code: Optional[str] = None
    tags: Optional[str] = None
    amount: Optional[str] = None
    owner_name: Optional[str] = None
    stage: Optional[str] = None
    is_no_follow_up: Optional[bool] = None
    win_type: Optional[str] = None


class OrderItemOut(BaseModel):
    id: str
    sku: str
    name: str
    qty: int
    unit_price_usd: Optional[Decimal] = None

    model_config = ConfigDict(from_attributes=True)


class OrderItemCreate(BaseModel):
    id: Optional[str] = None
    sku: str
    name: str
    qty: int
    unit_price_usd: Optional[float] = None


class OrderOut(BaseModel):
    id: str
    order_number: str
    pi_number: Optional[str] = None
    account_id: str
    requested_by_id: Optional[str] = None
    subtotal_usd: Optional[Decimal] = None
    status: str
    order_type: Optional[str] = None
    order_kind: Optional[str] = None
    po_status: Optional[str] = None
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    items: List[OrderItemOut] = []

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    id: str
    order_number: str
    pi_number: Optional[str] = ""
    account_id: str
    requested_by_id: Optional[str] = None
    subtotal_usd: Optional[float] = None
    status: str
    order_type: Optional[str] = ""
    order_kind: Optional[str] = ""
    po_status: Optional[str] = ""
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    items: List[OrderItemCreate] = []


class OrderUpdate(BaseModel):
    order_number: Optional[str] = None
    pi_number: Optional[str] = None
    account_id: Optional[str] = None
    requested_by_id: Optional[str] = None
    subtotal_usd: Optional[float] = None
    status: Optional[str] = None
    order_type: Optional[str] = None
    order_kind: Optional[str] = None
    po_status: Optional[str] = None
    created_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    items: Optional[List[OrderItemCreate]] = None
