import json

role_names = {
  "salesRep": "销售员",
  "salesManager": "销售经理",
  "countryManager": "国家负责人",
  "executive": "高管",
  "distributor": "经销商",
  "productManager": "产品经理",
  "marketing": "市场部",
  "finance": "财务",
  "supplyChain": "供应链",
  "orderOps": "订单运营",
  "readComment": "查看+评论",
  "readOnly": "仅查看",
  "admin": "系统管理员",
}

permission_names = {
  "viewSalesFunnel": "查看销售漏斗",
  "editAccountFields": "编辑客户字段",
  "reassignAccounts": "重新分配客户",
  "viewContractsPage": "查看合同页面",
  "viewTeamPage": "查看团队页面",
  "inviteUsers": "邀请新用户",
  "accessSystemSettings": "访问系统设置",
  "generateExecutiveReports": "生成高管报告",
  "viewAuditLogs": "查看审计日志",
}

scope_names = {
  "own": "仅用户本人负责的记录",
  "team": "用户团队负责的记录",
  "market": "用户所辖市场内的记录",
  "distributor": "其负责的经销商客户",
  "all": "全部记录",
}

translations = {
  "zh-CN": {
    "settings_roles_description": "编辑每个角色可执行的操作以及可查看的记录范围。修改立即对该角色下所有用户生效。",
    "settings_roles_locked": "已锁定",
    "settings_roles_save": "保存",
    "settings_roles_scope": "记录访问范围",
    **{f"role_{k}": v for k,v in role_names.items()},
    **{f"perm_{k}": v for k,v in permission_names.items()},
    **{f"scope_{k}": v for k,v in scope_names.items()},
  },
  "zh-HK": {
    "settings_roles_description": "編輯每個角色可執行的操作以及可查看的記錄範圍。修改立即對該角色下所有用戶生效。",
    "settings_roles_locked": "已鎖定",
    "settings_roles_save": "儲存",
    "settings_roles_scope": "記錄訪問範圍",
    **{f"role_{k}": v for k,v in {
      "salesRep": "銷售員", "salesManager": "銷售經理", "countryManager": "國家負責人",
      "executive": "高管", "distributor": "經銷商", "productManager": "產品經理",
      "marketing": "市場部", "finance": "財務", "supplyChain": "供應鏈",
      "orderOps": "訂單運營", "readComment": "查看+評論", "readOnly": "僅查看", "admin": "系統管理員",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "查看銷售漏斗", "editAccountFields": "編輯客戶字段", "reassignAccounts": "重新分配客戶",
      "viewContractsPage": "查看合同頁面", "viewTeamPage": "查看團隊頁面", "inviteUsers": "邀請新用戶",
      "accessSystemSettings": "訪問系統設置", "generateExecutiveReports": "生成高管報告", "viewAuditLogs": "查看審計日誌",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "僅用戶本人負責的記錄", "team": "用戶團隊負責的記錄", "market": "用戶所轄市場內的記錄",
      "distributor": "其負責的經銷商客戶", "all": "全部記錄",
    }.items()},
  },
  "en-US": {
    "settings_roles_description": "Edit the actions each role can perform and the record access scope. Changes take effect immediately for all users in that role.",
    "settings_roles_locked": "Locked",
    "settings_roles_save": "Save",
    "settings_roles_scope": "Record access scope",
    **{f"role_{k}": v for k,v in {
      "salesRep": "Sales Rep", "salesManager": "Sales Manager", "countryManager": "Country Manager",
      "executive": "Executive", "distributor": "Distributor", "productManager": "Product Manager",
      "marketing": "Marketing", "finance": "Finance", "supplyChain": "Supply Chain",
      "orderOps": "Order Operations", "readComment": "Read + Comment", "readOnly": "Read Only", "admin": "System Admin",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "View sales funnel", "editAccountFields": "Edit account fields", "reassignAccounts": "Reassign accounts",
      "viewContractsPage": "View contracts page", "viewTeamPage": "View team page", "inviteUsers": "Invite new users",
      "accessSystemSettings": "Access system settings", "generateExecutiveReports": "Generate executive reports", "viewAuditLogs": "View audit logs",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "Records owned by the user only", "team": "Records owned by the user's team", "market": "Records within the user's markets",
      "distributor": "Distributor accounts they own", "all": "All records",
    }.items()},
  },
  "th-TH": {
    "settings_roles_description": "แก้ไขการดำเนินการที่บทบาทแต่ละบทบาทสามารถทำได้และขอบเขตการเข้าถึงบันทึก การเปลี่ยนแปลงมีผลทันทีสำหรับผู้ใช้ทั้งหมดในบทบาทนั้น",
    "settings_roles_locked": "ล็อก",
    "settings_roles_save": "บันทึก",
    "settings_roles_scope": "ขอบเขตการเข้าถึงบันทึก",
    **{f"role_{k}": v for k,v in {
      "salesRep": "พนักงานขาย", "salesManager": "ผู้จัดการฝ่ายขาย", "countryManager": "ผู้จัดการประเทศ",
      "executive": "ผู้บริหาร", "distributor": "ตัวแทนจำหน่าย", "productManager": "ผู้จัดการผลิตภัณฑ์",
      "marketing": "ฝ่ายการตลาด", "finance": "การเงิน", "supplyChain": "ห่วงโซ่อุปทาน",
      "orderOps": "ปฏิบัติการคำสั่งซื้อ", "readComment": "อ่าน+แสดงความคิดเห็น", "readOnly": "อ่านอย่างเดียว", "admin": "ผู้ดูแลระบบ",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "ดูกรวยการขาย", "editAccountFields": "แก้ไขฟิลด์ลูกค้า", "reassignAccounts": "มอบหมายลูกค้าใหม่",
      "viewContractsPage": "ดูหน้าสัญญา", "viewTeamPage": "ดูหน้าทีม", "inviteUsers": "เชิญผู้ใช้ใหม่",
      "accessSystemSettings": "เข้าถึงการตั้งค่าระบบ", "generateExecutiveReports": "สร้างรายงานผู้บริหาร", "viewAuditLogs": "ดูบันทึกการตรวจสอบ",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "บันทึกที่ผู้ใช้รับผิดชอบเท่านั้น", "team": "บันทึกที่ทีมของผู้ใช้รับผิดชอบ", "market": "บันทึกภายในตลาดของผู้ใช้",
      "distributor": "ลูกค้าตัวแทนจำหน่ายที่พวกเขารับผิดชอบ", "all": "บันทึกทั้งหมด",
    }.items()},
  },
  "id-ID": {
    "settings_roles_description": "Edit tindakan yang dapat dilakukan setiap peran dan cakupan akses rekaman. Perubahan segera berlaku untuk semua pengguna dalam peran tersebut.",
    "settings_roles_locked": "Terkunci",
    "settings_roles_save": "Simpan",
    "settings_roles_scope": "Cakupan akses rekaman",
    **{f"role_{k}": v for k,v in {
      "salesRep": "Sales Rep", "salesManager": "Manajer Penjualan", "countryManager": "Manajer Negara",
      "executive": "Eksekutif", "distributor": "Distributor", "productManager": "Manajer Produk",
      "marketing": "Pemasaran", "finance": "Keuangan", "supplyChain": "Rantai Pasok",
      "orderOps": "Operasi Pesanan", "readComment": "Baca + Komentar", "readOnly": "Hanya Baca", "admin": "Admin Sistem",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "Lihat corong penjualan", "editAccountFields": "Edit bidang akun", "reassignAccounts": "Tugaskan ulang akun",
      "viewContractsPage": "Lihat halaman kontrak", "viewTeamPage": "Lihat halaman tim", "inviteUsers": "Undang pengguna baru",
      "accessSystemSettings": "Akses pengaturan sistem", "generateExecutiveReports": "Hasilkan laporan eksekutif", "viewAuditLogs": "Lihat log audit",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "Rekaman yang menjadi tanggung jawab pengguna saja", "team": "Rekaman yang menjadi tanggung jawab tim pengguna", "market": "Rekaman di dalam pasar pengguna",
      "distributor": "Akun distributor yang mereka tangani", "all": "Semua rekaman",
    }.items()},
  },
  "vi-VN": {
    "settings_roles_description": "Chỉnh sửa các hành động mỗi vai trò có thể thực hiện và phạm vi truy cập hồ sơ. Thay đổi có hiệu lực ngay lập tức đối với tất cả ngườidùng trong vai trò đó.",
    "settings_roles_locked": "Đã khóa",
    "settings_roles_save": "Lưu",
    "settings_roles_scope": "Phạm vi truy cập hồ sơ",
    **{f"role_{k}": v for k,v in {
      "salesRep": "Đại diện bán hàng", "salesManager": "Quản lý bán hàng", "countryManager": "Quản lý quốc gia",
      "executive": "Ban lãnh đạo", "distributor": "Nhà phân phối", "productManager": "Quản lý sản phẩm",
      "marketing": "Marketing", "finance": "Tài chính", "supplyChain": "Chuỗi cung ứng",
      "orderOps": "Vận hành đơn hàng", "readComment": "Xem + Bình luận", "readOnly": "Chỉ xem", "admin": "Quản trị viên",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "Xem phễu bán hàng", "editAccountFields": "Chỉnh sửa trường khách hàng", "reassignAccounts": "Chuyển giao khách hàng",
      "viewContractsPage": "Xem trang hợp đồng", "viewTeamPage": "Xem trang nhóm", "inviteUsers": "Mờingườidùng mới",
      "accessSystemSettings": "Truy cập cài đặt hệ thống", "generateExecutiveReports": "Tạo báo cáo lãnh đạo", "viewAuditLogs": "Xem nhật ký kiểm toán",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "Chỉ hồ sơ do ngườidùng chịu trách nhiệm", "team": "Hồ sơ do nhóm ngườidùng chịu trách nhiệm", "market": "Hồ sơ trong thị trường của ngườidùng",
      "distributor": "Khách hàng nhà phân phối do họ phụ trách", "all": "Tất cả hồ sơ",
    }.items()},
  },
  "fr-FR": {
    "settings_roles_description": "Modifiez les actions que chaque role peut effectuer et la portee d'acces aux enregistrements. Les modifications prennent effet immediatement pour tous les utilisateurs de ce role.",
    "settings_roles_locked": "Verrouille",
    "settings_roles_save": "Enregistrer",
    "settings_roles_scope": "Portee d'acces aux enregistrements",
    **{f"role_{k}": v for k,v in {
      "salesRep": "Commercial", "salesManager": "Responsable commercial", "countryManager": "Responsable pays",
      "executive": "Direction", "distributor": "Distributeur", "productManager": "Chef de produit",
      "marketing": "Marketing", "finance": "Finance", "supplyChain": "Supply Chain",
      "orderOps": "Operations commandes", "readComment": "Lecture + Commentaire", "readOnly": "Lecture seule", "admin": "Admin systeme",
    }.items()},
    **{f"perm_{k}": v for k,v in {
      "viewSalesFunnel": "Voir le pipeline", "editAccountFields": "Modifier les champs client", "reassignAccounts": "Reattribuer des comptes",
      "viewContractsPage": "Voir la page contrats", "viewTeamPage": "Voir la page equipe", "inviteUsers": "Inviter des utilisateurs",
      "accessSystemSettings": "Acceder aux parametres systeme", "generateExecutiveReports": "Generer rapports dirigeants", "viewAuditLogs": "Voir journaux d'audit",
    }.items()},
    **{f"scope_{k}": v for k,v in {
      "own": "Enregistrements dont l'utilisateur est responsable", "team": "Enregistrements de l'equipe", "market": "Enregistrements dans les marches de l'utilisateur",
      "distributor": "Comptes distributeurs geres", "all": "Tous les enregistrements",
    }.items()},
  },
}

for locale, trans in translations.items():
    path = f"{locale}.json"
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.setdefault('settings', {}).setdefault('roles', {})
    data['settings']['roles']['description'] = trans['settings_roles_description']
    data['settings']['roles']['locked'] = trans['settings_roles_locked']
    data['settings']['roles']['save'] = trans['settings_roles_save']
    data['settings']['roles']['scope'] = trans['settings_roles_scope']
    data.setdefault('roles', {})
    for k, v in role_names.items():
        data['roles'][k] = trans[f"role_{k}"]
    data.setdefault('permissions', {})
    for k, v in permission_names.items():
        data['permissions'][k] = trans[f"perm_{k}"]
    data.setdefault('scopes', {})
    for k, v in scope_names.items():
        data['scopes'][k] = trans[f"scope_{k}"]
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"updated {locale}")
