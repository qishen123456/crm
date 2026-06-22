import { readFileSync, writeFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const localesDir = join(__dirname, '../src/locales')

function loadJson(name: string) {
  return JSON.parse(readFileSync(join(localesDir, name), 'utf-8'))
}

function saveJson(name: string, data: any) {
  writeFileSync(join(localesDir, name), JSON.stringify(data, null, 2) + '\n')
}

function setPath(obj: any, path: string, value: any) {
  const parts = path.split('.')
  let cur = obj
  for (let i = 0; i < parts.length - 1; i++) {
    cur[parts[i]] = cur[parts[i]] || {}
    cur = cur[parts[i]]
  }
  cur[parts[parts.length - 1]] = value
}

const translations: Record<string, Record<string, string>> = {
  'zh-CN': {
    'pipeline.noFollowUp': '无跟进',
    'pipeline.searchPlaceholder': '搜索客户 / 合同编号',
    'pipeline.newOpp': '+ 新建商机',
    'pipeline.firstWin': '首次赢单',
    'pipeline.reorder': '翻单',
    'pipeline.firstWinGroup': '首次赢单',
    'pipeline.reorderGroup': '翻单（老客户）',
    'pipeline.regionAll': '全部',
  },
  'zh-HK': {
    'pipeline.noFollowUp': '無跟進',
    'pipeline.searchPlaceholder': '搜尋客戶 / 合同編號',
    'pipeline.newOpp': '+ 新增商機',
    'pipeline.firstWin': '首次贏單',
    'pipeline.reorder': '翻單',
    'pipeline.firstWinGroup': '首次贏單',
    'pipeline.reorderGroup': '翻單（老客戶）',
    'pipeline.regionAll': '全部',
  },
  'en-US': {
    'pipeline.noFollowUp': 'No follow-up',
    'pipeline.searchPlaceholder': 'Search account / contract no.',
    'pipeline.newOpp': '+ New Opportunity',
    'pipeline.firstWin': 'First Win',
    'pipeline.reorder': 'Reorder',
    'pipeline.firstWinGroup': 'First Win',
    'pipeline.reorderGroup': 'Reorder (Existing)',
    'pipeline.regionAll': 'All',
  },
  'th-TH': {
    'pipeline.noFollowUp': 'ไม่มีการติดตาม',
    'pipeline.searchPlaceholder': 'ค้นหาลูกค้า / หมายเลขสัญญา',
    'pipeline.newOpp': '+ สร้างโอกาสใหม่',
    'pipeline.firstWin': 'ชนะครั้งแรก',
    'pipeline.reorder': 'สั่งซื้อซ้ำ',
    'pipeline.firstWinGroup': 'ชนะครั้งแรก',
    'pipeline.reorderGroup': 'สั่งซื้อซ้ำ (ลูกค้าเก่า)',
    'pipeline.regionAll': 'ทั้งหมด',
  },
  'id-ID': {
    'pipeline.noFollowUp': 'Tidak ada tindak lanjut',
    'pipeline.searchPlaceholder': 'Cari akun / nomor kontrak',
    'pipeline.newOpp': '+ Peluang Baru',
    'pipeline.firstWin': 'Menang Pertama',
    'pipeline.reorder': 'Pesanan Ulang',
    'pipeline.firstWinGroup': 'Menang Pertama',
    'pipeline.reorderGroup': 'Pesanan Ulang (Pelanggan Lama)',
    'pipeline.regionAll': 'Semua',
  },
  'vi-VN': {
    'pipeline.noFollowUp': 'Chưa theo dõi',
    'pipeline.searchPlaceholder': 'Tìm khách hàng / số hợp đồng',
    'pipeline.newOpp': '+ Cơ hội mới',
    'pipeline.firstWin': 'Thắng đầu tiên',
    'pipeline.reorder': 'Đơn hàng lặp lại',
    'pipeline.firstWinGroup': 'Thắng đầu tiên',
    'pipeline.reorderGroup': 'Đơn hàng lặp lại (Khách hàng cũ)',
    'pipeline.regionAll': 'Tất cả',
  },
}

for (const [file, adds] of Object.entries(translations)) {
  const data = loadJson(`${file}.json`)
  for (const [path, value] of Object.entries(adds)) {
    if (!path.split('.').reduce((o, p) => o?.[p], data)) {
      setPath(data, path, value)
    }
  }
  saveJson(`${file}.json`, data)
  console.log(`Updated ${file}.json`)
}
