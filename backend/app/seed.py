from datetime import datetime
from sqlalchemy.orm import Session
from app import models
from app.core.security import get_password_hash


DEFAULT_PASSWORD = "demo2026"

MARKETS = [
    {"code": "SG", "name": "新加坡", "flag": "🇸🇬"},
    {"code": "HK", "name": "中国香港", "flag": "🇭🇰"},
    {"code": "MY", "name": "马来西亚", "flag": "🇲🇾"},
    {"code": "TH", "name": "泰国", "flag": "🇹🇭"},
    {"code": "ID", "name": "印度尼西亚", "flag": "🇮🇩"},
    {"code": "MO", "name": "中国澳门", "flag": "🇲🇴"},
    {"code": "US", "name": "美国", "flag": "🇺🇸"},
]

ROLES = [
    {"code": "salesRep", "name_en": "Sales Rep", "name_zh": "销售员", "scope": "own", "sort": 10},
    {"code": "salesManager", "name_en": "Sales Manager", "name_zh": "销售经理", "scope": "team", "sort": 20},
    {"code": "countryManager", "name_en": "Country Manager", "name_zh": "国家负责人", "scope": "market", "sort": 30},
    {"code": "executive", "name_en": "Executive", "name_zh": "高管", "scope": "all", "sort": 40},
    {"code": "distributor", "name_en": "Distributor", "name_zh": "经销商", "scope": "distributor", "sort": 50},
    {"code": "productManager", "name_en": "Product Manager", "name_zh": "产品经理", "scope": "all", "sort": 60},
    {"code": "marketing", "name_en": "Marketing", "name_zh": "市场部", "scope": "market", "sort": 70},
    {"code": "finance", "name_en": "Finance", "name_zh": "财务", "scope": "all", "sort": 80},
    {"code": "supplyChain", "name_en": "Supply Chain", "name_zh": "供应链", "scope": "all", "sort": 90},
    {"code": "orderOps", "name_en": "Order Operations", "name_zh": "订单运营", "scope": "all", "sort": 100},
    {"code": "readComment", "name_en": "Read + Comment", "name_zh": "查看+评论", "scope": "all", "sort": 110},
    {"code": "readOnly", "name_en": "Read Only", "name_zh": "仅查看", "scope": "all", "sort": 120},
    {"code": "admin", "name_en": "System Admin", "name_zh": "系统管理员", "scope": "all", "sort": 130, "system": True},
]

PERMISSIONS = [
    {"code": "viewSalesFunnel", "name_en": "View sales funnel", "name_zh": "查看销售漏斗", "category": "sales", "sort": 10},
    {"code": "editAccountFields", "name_en": "Edit account fields", "name_zh": "编辑客户字段", "category": "accounts", "sort": 20},
    {"code": "reassignAccounts", "name_en": "Reassign accounts", "name_zh": "重新分配客户", "category": "accounts", "sort": 30},
    {"code": "viewContractsPage", "name_en": "View contracts page", "name_zh": "查看合同页面", "category": "contracts", "sort": 40},
    {"code": "viewTeamPage", "name_en": "View team page", "name_zh": "查看团队页面", "category": "team", "sort": 50},
    {"code": "inviteUsers", "name_en": "Invite new users", "name_zh": "邀请新用户", "category": "team", "sort": 60},
    {"code": "accessSystemSettings", "name_en": "Access system settings", "name_zh": "访问系统设置", "category": "settings", "sort": 70},
    {"code": "generateExecutiveReports", "name_en": "Generate executive reports", "name_zh": "生成高管报告", "category": "reports", "sort": 80},
    {"code": "viewAuditLogs", "name_en": "View audit logs", "name_zh": "查看审计日志", "category": "settings", "sort": 90},
]

# Matrix: role_code -> set of permission codes (must match PERMISSIONS codes)
ROLE_PERMISSIONS = {
    "salesRep": {"viewSalesFunnel"},
    "salesManager": {"viewSalesFunnel", "editAccountFields", "reassignAccounts", "viewContractsPage", "viewTeamPage", "generateExecutiveReports"},
    "countryManager": {"viewSalesFunnel", "editAccountFields", "reassignAccounts", "viewContractsPage", "viewTeamPage", "inviteUsers", "generateExecutiveReports", "viewAuditLogs"},
    "executive": {"viewSalesFunnel", "editAccountFields", "reassignAccounts", "viewContractsPage", "viewTeamPage", "inviteUsers", "generateExecutiveReports", "viewAuditLogs"},
    "distributor": {"viewContractsPage"},
    "productManager": {"viewSalesFunnel"},
    "marketing": {"viewSalesFunnel", "viewAuditLogs"},
    "finance": {"viewSalesFunnel", "viewContractsPage", "viewAuditLogs"},
    "supplyChain": {"viewSalesFunnel", "viewContractsPage"},
    "orderOps": {"viewSalesFunnel", "viewContractsPage", "viewTeamPage"},
    "readComment": {"viewSalesFunnel", "viewContractsPage"},
    "readOnly": {"viewSalesFunnel", "viewContractsPage"},
    "admin": set(),  # admin gets all permissions dynamically
}

USERS = [
    {"id": "u1", "name": "系统管理员", "email": "admin@angel.cn", "role_code": "admin", "department": "Admin", "market_code": "SG", "avatar": "管理"},
    {"id": "u2", "name": "杨文", "email": "yangwen@angel.cn", "role_code": "salesManager", "department": "Sales", "market_code": "SG", "avatar": "杨文"},
    {"id": "u3", "name": "刘世宏", "email": "liush@angel.cn", "role_code": "countryManager", "department": "Sales", "market_code": "TH", "avatar": "世宏"},
    {"id": "u4", "name": "杨森", "email": "yangsen@angel.cn", "role_code": "salesManager", "department": "Sales", "market_code": "HK", "avatar": "杨森"},
    {"id": "u5", "name": "Keith Harrington", "email": "keith@angel.cn", "role_code": "salesRep", "department": "Sales", "market_code": "US", "avatar": "KH"},
    {"id": "u6", "name": "苏蓬", "email": "supon@angel.cn", "role_code": "salesRep", "department": "Sales", "market_code": "TH", "avatar": "苏蓬"},
    {"id": "u7", "name": "Olivia Tan", "email": "olivia@angel.cn", "role_code": "marketing", "department": "Marketing", "market_code": "SG", "avatar": "OT"},
    {"id": "u8", "name": "Stephen Liu", "email": "stephen@angel.cn", "role_code": "executive", "department": "Executive", "market_code": "SG", "avatar": "SL"},
    {"id": "u9", "name": "张财务", "email": "finance@angel.cn", "role_code": "finance", "department": "Finance", "market_code": "SG", "avatar": "财务"},
    {"id": "u10", "name": "李法务", "email": "legal@angel.cn", "role_code": "readComment", "department": "Legal", "market_code": "SG", "avatar": "法务"},
    {"id": "u11", "name": "王供应链", "email": "supply@angel.cn", "role_code": "supplyChain", "department": "Supply Chain", "market_code": "SG", "avatar": "供应链"},
    {"id": "u12", "name": "陈安装", "email": "install@angel.cn", "role_code": "orderOps", "department": "Operations", "market_code": "TH", "avatar": "安装"},
]

ACCOUNTS = [
    {"id": "a1", "code": "RAFF", "name": "Raffles Hospitality", "market_code": "SG", "owner_id": "u2", "annual_target_usd": 800000, "year_to_date_usd": 620000, "contract_status": "active", "contract_expires_at": "2026-12-31", "business_type": "commercial", "opportunity_notes": "集团总部正在评估 5 年统一供应商方案。", "customer_resources": "集团旗下 14 家五星酒店。", "next_dig_directions": "1. 6 月底前完成集团框架协议初稿\n2. 推进 KL + BKK 分店试点装机"},
    {"id": "a2", "code": "MARI", "name": "Marina Bay Sands", "market_code": "SG", "owner_id": "u2", "annual_target_usd": 1200000, "year_to_date_usd": 540000, "contract_status": "expiring", "contract_expires_at": "2026-07-08", "business_type": "commercial", "opportunity_notes": "合同 22 天后到期，客户满意度高。", "customer_resources": "新加坡最大综合度假村。", "next_dig_directions": "1. 续约谈判中，争取 3 年期 + 涨价 5%"},
    {"id": "a3", "code": "GENT", "name": "Genting Group", "market_code": "MY", "owner_id": "u2", "annual_target_usd": 600000, "year_to_date_usd": 480000, "contract_status": "active", "contract_expires_at": "2026-11-15", "business_type": "commercial", "opportunity_notes": "年度框架谈判中，客户对零售场景也有兴趣。", "customer_resources": "马来西亚云顶集团。", "next_dig_directions": "1. 推进年度框架协议续签\n2. 介绍零售机型进入云顶商场"},
    {"id": "a4", "code": "BANG", "name": "Bangkok Mall Group", "market_code": "TH", "owner_id": "u3", "annual_target_usd": 500000, "year_to_date_usd": 240000, "contract_status": "active", "contract_expires_at": "2026-10-30", "business_type": "commercial", "opportunity_notes": "曼谷购物中心主餐饮层已安装 8 台 D2000。", "customer_resources": "曼谷核心商圈购物中心。", "next_dig_directions": "1. 完成剩余 4 台安装\n2. 地下室美食城电气容量问题跟进"},
    {"id": "a5", "code": "SOEK", "name": "Soekarno Retail Distribution", "market_code": "ID", "owner_id": "u3", "annual_target_usd": 400000, "year_to_date_usd": 110000, "contract_status": "expiring", "contract_expires_at": "2026-06-21", "business_type": "retail", "opportunity_notes": "印尼经销商 Q2 备货已发货，准备开斋节促销。", "customer_resources": "雅加达南区主要家电经销商。", "next_dig_directions": "1. 跟进终端动销\n2. 规划 Q3 返单"},
    {"id": "a6", "code": "HKHO", "name": "HK Hospitality Corp", "market_code": "HK", "owner_id": "u4", "annual_target_usd": 700000, "year_to_date_usd": 520000, "contract_status": "active", "contract_expires_at": "2026-09-15", "business_type": "commercial", "opportunity_notes": "集团总部要求 15% 一次性 discount。", "customer_resources": "香港酒店集团，旗下 8 家中高端酒店。", "next_dig_directions": "1. 申请折扣特例审批\n2. 准备 5 年框架协议草案"},
    {"id": "a7", "code": "MGMM", "name": "MGM Macau", "market_code": "MO", "owner_id": "u4", "annual_target_usd": 900000, "year_to_date_usd": 380000, "contract_status": "active", "contract_expires_at": "2026-12-20", "business_type": "commercial", "opportunity_notes": "方案阶段，客户对 pricing pushback。", "customer_resources": "澳门大型综合度假村。", "next_dig_directions": "1. 重新调整报价方案\n2. 安排高管拜访"},
    {"id": "a8", "code": "WEST", "name": "Westwind F&B", "market_code": "US", "owner_id": "u5", "annual_target_usd": 1500000, "year_to_date_usd": 980000, "contract_status": "active", "contract_expires_at": "2026-12-31", "business_type": "commercial", "opportunity_notes": "已批准合同，首单 $108k 大货订单 PO 待收。", "customer_resources": "美国连锁 F&B 集团，西部 23 家门店。", "next_dig_directions": "1. 催收 PO\n2. 准备生产排期"},
    {"id": "a9", "code": "PIVO", "name": "Pivot Industrial", "market_code": "US", "owner_id": "", "annual_target_usd": 900000, "year_to_date_usd": 0, "contract_status": "expired", "contract_expires_at": "2026-01-15", "business_type": "industrial", "opportunity_notes": "合同已到期，暂无续约计划。", "customer_resources": "美国工业客户。", "next_dig_directions": "1. 评估是否重新激活"},
    {"id": "a10", "code": "JOHO", "name": "Johor Bahru F&B Holdings", "market_code": "MY", "owner_id": "", "annual_target_usd": 250000, "year_to_date_usd": 0, "contract_status": "active", "contract_expires_at": "2026-12-31", "business_type": "commercial", "opportunity_notes": "新客户，待分配销售负责人。", "customer_resources": "柔佛州 F&B 集团。", "next_dig_directions": "1. 分配负责人\n2. 首次拜访"},
]

OPPORTUNITY_CARDS = [
    {"id": "oc-1", "company_name": "Raffles Hospitality", "region_code": "SG · RAFF", "tags": "fnb · distributor", "amount": "$120k", "owner_name": "杨文", "stage": "prospect"},
    {"id": "oc-2", "company_name": "Bangkok Mall Group", "region_code": "TH · BANG", "tags": "public · direct", "amount": "$65k", "owner_name": "世宏", "stage": "prospect"},
    {"id": "oc-3", "company_name": "HK Hospitality Corp", "region_code": "HK · HKHO", "tags": "residential · rental", "amount": "$45k", "owner_name": "杨森", "stage": "prospect", "is_no_follow_up": True},
    {"id": "oc-4", "company_name": "Marina Bay Sands", "region_code": "SG · MARI", "tags": "fnb · direct", "amount": "$240k", "owner_name": "杨文", "stage": "qualify"},
    {"id": "oc-5", "company_name": "Soekarno Retail Distribution", "region_code": "ID · SOEK", "tags": "residential · distributor", "amount": "$95k", "owner_name": "世宏", "stage": "qualify"},
    {"id": "oc-6", "company_name": "Genting Group", "region_code": "MY · GENT", "tags": "industrial · direct", "amount": "$180k", "owner_name": "杨森", "stage": "qualify", "is_no_follow_up": True},
    {"id": "oc-7", "company_name": "MGM Macau", "region_code": "MO · MGMM", "tags": "fnb · direct", "amount": "$320k", "owner_name": "杨森", "stage": "proposal"},
    {"id": "oc-8", "company_name": "Westwind F&B", "region_code": "US · WEST", "tags": "fnb · distributor", "amount": "$410k", "owner_name": "Keith", "stage": "proposal"},
    {"id": "oc-9", "company_name": "Bangkok Mall Group", "region_code": "TH · BANG", "tags": "industrial · rental", "amount": "$150k", "owner_name": "世宏", "stage": "proposal", "is_no_follow_up": True},
    {"id": "oc-10", "company_name": "Soekarno Retail Distribution", "region_code": "ID · SOEK", "tags": "public · direct", "amount": "$85k", "owner_name": "世宏", "stage": "proposal"},
    {"id": "oc-11", "company_name": "Raffles Hospitality", "region_code": "SG · RAFF", "tags": "fnb · direct", "amount": "$280k", "owner_name": "杨文", "stage": "negotiate"},
    {"id": "oc-12", "company_name": "HK Hospitality Corp", "region_code": "HK · HKHO", "tags": "industrial · direct", "amount": "$510k", "owner_name": "杨森", "stage": "negotiate"},
    {"id": "oc-13", "company_name": "Marina Bay Sands", "region_code": "SG · MARI", "tags": "fnb · direct", "amount": "$240k", "owner_name": "杨文", "stage": "negotiate"},
    {"id": "oc-14", "company_name": "Raffles Hospitality", "region_code": "SG · RAFF", "tags": "fnb · direct", "amount": "$460k", "owner_name": "杨文", "stage": "closedWon", "win_type": "first"},
    {"id": "oc-15", "company_name": "Genting Group", "region_code": "MY · GENT", "tags": "residential · distributor", "amount": "$220k", "owner_name": "杨文", "stage": "closedWon", "win_type": "first"},
    {"id": "oc-16", "company_name": "Westwind F&B", "region_code": "US · WEST", "tags": "fnb · direct", "amount": "$680k", "owner_name": "Keith", "stage": "closedWon", "win_type": "first"},
    {"id": "oc-17", "company_name": "Raffles Hospitality", "region_code": "SG · RAFF", "tags": "fnb · direct", "amount": "$180k", "owner_name": "杨文", "stage": "closedWon", "win_type": "reorder"},
]

ORDERS = [
    {
        "id": "ord-1", "order_number": "AHT-ORD-2026-0001", "pi_number": "PI-TH20260614", "account_id": "a4",
        "requested_by_id": "u6", "subtotal_usd": 31440, "status": "piIssued", "order_type": "preWin", "order_kind": "bulk", "po_status": "received",
        "created_at": "2026-06-13", "items": [
            {"sku": "ANG-FB-D2000", "name": "Angel D2000 Commercial Dispenser", "qty": 12, "unit_price_usd": 2400},
            {"sku": "ANG-INSTALL-STD", "name": "Standard Installation Service", "qty": 12, "unit_price_usd": 220},
        ]
    },
    {
        "id": "ord-2", "order_number": "AHT-ORD-2026-0002", "pi_number": "PI-SG20260529", "account_id": "a1",
        "requested_by_id": "u2", "subtotal_usd": 23700, "status": "completed", "order_type": "firstOrder", "order_kind": "sample", "po_status": "received",
        "created_at": "2026-05-27", "shipped_at": "2026-06-02", "items": [
            {"sku": "ANG-FB-D3000", "name": "Angel D3000 Pro Commercial Dispenser", "qty": 6, "unit_price_usd": 3600},
            {"sku": "ANG-INSTALL-STD", "name": "Standard Installation Service", "qty": 6, "unit_price_usd": 350},
        ]
    },
    {
        "id": "ord-3", "order_number": "AHT-ORD-2026-0003", "pi_number": "-", "account_id": "a8",
        "requested_by_id": "u5", "subtotal_usd": 108000, "status": "pendingPI", "order_type": "firstOrder", "order_kind": "bulk", "po_status": "pending",
        "created_at": "2026-06-15", "items": [
            {"sku": "ANG-FB-D3000", "name": "Angel D3000 Pro Commercial Dispenser", "qty": 30, "unit_price_usd": 3600},
        ]
    },
    {
        "id": "ord-4", "order_number": "AHT-ORD-2026-0004", "pi_number": "PI-SG20260609", "account_id": "a1",
        "requested_by_id": "u2", "subtotal_usd": 13680, "status": "completed", "order_type": "reorder", "order_kind": "reorder", "po_status": "received",
        "created_at": "2026-06-08", "shipped_at": "2026-06-10", "items": [
            {"sku": "ANG-FB-D3000", "name": "Angel D3000 Pro Commercial Dispenser", "qty": 3, "unit_price_usd": 3600},
            {"sku": "ANG-FILTER-12M", "name": "12-month Filter Pack", "qty": 6, "unit_price_usd": 680},
        ]
    },
    {
        "id": "ord-5", "order_number": "AHT-ORD-2026-0005", "pi_number": "PI-ID20260527", "account_id": "a5",
        "requested_by_id": "u3", "subtotal_usd": 72000, "status": "completed", "order_type": "preWin", "order_kind": "bulk", "po_status": "received",
        "created_at": "2026-05-25", "shipped_at": "2026-05-30", "items": [
            {"sku": "ANG-RES-H500", "name": "Angel H500 Residential Whole-Home System", "qty": 24, "unit_price_usd": 1800},
            {"sku": "ANG-RES-U200", "name": "Angel U200 Under-Sink Filter", "qty": 60, "unit_price_usd": 480},
        ]
    },
]


def _to_datetime(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)


def _account_id_from_region(region_code: str, account_lookup: dict) -> str:
    parts = [p.strip() for p in region_code.split("·")]
    code = parts[-1] if parts else ""
    return account_lookup.get(code, account_lookup.get("RAFF"))


def run_seed(db: Session):
    if db.query(models.Market).first():
        return

    for m in MARKETS:
        db.add(models.Market(**m))

    role_lookup = {}
    for r in ROLES:
        role = models.Role(
            code=r["code"],
            name_en=r["name_en"],
            name_zh=r["name_zh"],
            record_access_scope=r["scope"],
            is_system=r.get("system", False),
            sort_order=r["sort"],
        )
        db.add(role)
        role_lookup[r["code"]] = role

    permission_lookup = {}
    for p in PERMISSIONS:
        perm = models.Permission(
            code=p["code"],
            name_en=p["name_en"],
            name_zh=p["name_zh"],
            category=p["category"],
            sort_order=p["sort"],
        )
        db.add(perm)
        permission_lookup[p["code"]] = perm

    db.flush()

    for role_code, perm_codes in ROLE_PERMISSIONS.items():
        granted_codes = set(perm_codes)
        if role_lookup[role_code].is_system:
            granted_codes = set(permission_lookup.keys())
        for perm_code, perm in permission_lookup.items():
            db.add(models.RolePermission(
                role_code=role_code,
                permission_code=perm_code,
                granted=perm_code in granted_codes,
            ))

    hashed = get_password_hash(DEFAULT_PASSWORD)
    for u in USERS:
        data = {**u}
        data["hashed_password"] = hashed
        data["status"] = "active"
        db.add(models.User(**data))

    db.flush()

    account_lookup = {}
    for a in ACCOUNTS:
        data = {**a}
        data["owner_id"] = data["owner_id"] or None
        data["contract_expires_at"] = _to_datetime(data.get("contract_expires_at"))
        account = models.Account(**data)
        db.add(account)
        account_lookup[a["code"]] = a["id"]

    db.flush()

    for oc in OPPORTUNITY_CARDS:
        data = {**oc}
        data.setdefault("is_no_follow_up", False)
        data["account_id"] = _account_id_from_region(data["region_code"], account_lookup)
        db.add(models.Opportunity(**data))

    for o in ORDERS:
        data = {**o}
        data["requested_by_id"] = data.get("requested_by_id") or None
        data["created_at"] = _to_datetime(data.get("created_at"))
        data["shipped_at"] = _to_datetime(data.get("shipped_at"))
        items = data.pop("items", [])
        order = models.Order(**data)
        for idx, it in enumerate(items):
            item = models.OrderItem(
                id=f"{order.id}-i{idx}",
                sku=it["sku"],
                name=it["name"],
                qty=it["qty"],
                unit_price_usd=it.get("unit_price_usd"),
            )
            order.items.append(item)
        db.add(order)

    db.commit()
