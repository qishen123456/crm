from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Market(Base):
    __tablename__ = "markets"
    code = Column(String(8), primary_key=True)
    name = Column(String(128), nullable=False)
    flag = Column(String(16), default="")


class Role(Base):
    __tablename__ = "roles"
    code = Column(String(32), primary_key=True)
    name_en = Column(String(64), nullable=False)
    name_zh = Column(String(64), default="")
    record_access_scope = Column(String(32), nullable=False, default="own")
    is_system = Column(Boolean, nullable=False, default=False)
    sort_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")


class Permission(Base):
    __tablename__ = "permissions"
    code = Column(String(64), primary_key=True)
    name_en = Column(String(128), nullable=False)
    name_zh = Column(String(128), default="")
    category = Column(String(64), default="")
    sort_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    role_code = Column(String(32), ForeignKey("roles.code", ondelete="CASCADE"), primary_key=True)
    permission_code = Column(String(64), ForeignKey("permissions.code", ondelete="CASCADE"), primary_key=True)
    granted = Column(Boolean, nullable=False, default=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(String(32), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(128), nullable=False)
    role = Column(String(64), default="")  # deprecated free-text label, kept for compatibility
    role_code = Column(String(32), ForeignKey("roles.code"), nullable=True)
    department = Column(String(64), nullable=False)
    market_code = Column(String(8), ForeignKey("markets.code"), nullable=True)
    avatar = Column(String(128), default="")
    status = Column(String(32), default="active")
    hashed_password = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    role_obj = relationship("Role")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(String(32), primary_key=True)
    code = Column(String(32), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    market_code = Column(String(8), ForeignKey("markets.code"), nullable=True)
    owner_id = Column(String(32), ForeignKey("users.id"), nullable=True)
    annual_target_usd = Column(Numeric(18, 2), default=0)
    year_to_date_usd = Column(Numeric(18, 2), default=0)
    contract_status = Column(String(32), default="active")
    contract_expires_at = Column(DateTime, nullable=True)
    business_type = Column(String(32), default="")
    opportunity_notes = Column(Text, default="")
    customer_resources = Column(Text, default="")
    next_dig_directions = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Opportunity(Base):
    __tablename__ = "opportunities"
    id = Column(String(32), primary_key=True)
    account_id = Column(String(32), ForeignKey("accounts.id"), nullable=False)
    company_name = Column(String(255), nullable=False)
    region_code = Column(String(64), default="")
    tags = Column(String(255), default="")
    amount = Column(String(64), default="")
    owner_name = Column(String(128), default="")
    stage = Column(String(16), nullable=False, default="prospect")
    is_no_follow_up = Column(Boolean, default=False)
    win_type = Column(String(16), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Order(Base):
    __tablename__ = "orders"
    id = Column(String(32), primary_key=True)
    order_number = Column(String(64), nullable=False, unique=True)
    pi_number = Column(String(128), default="")
    account_id = Column(String(32), ForeignKey("accounts.id"), nullable=False)
    requested_by_id = Column(String(32), ForeignKey("users.id"), nullable=True)
    subtotal_usd = Column(Numeric(18, 2), default=0)
    status = Column(String(32), nullable=False)
    order_type = Column(String(64), default="")
    order_kind = Column(String(64), default="")
    po_status = Column(String(32), default="")
    created_at = Column(DateTime, nullable=True)
    shipped_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(String(32), primary_key=True)
    order_id = Column(String(32), ForeignKey("orders.id"), nullable=False)
    sku = Column(String(64), default="")
    name = Column(String(255), default="")
    qty = Column(Integer, nullable=False, default=1)
    unit_price_usd = Column(Numeric(18, 2), default=0)

    order = relationship("Order", back_populates="items")
