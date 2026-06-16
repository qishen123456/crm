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

const additions: Record<string, string> = {
  'dailyReport.title': '今日日报',
  'dailyReport.hint': '保持简短 – 3 分钟搞定。让经理了解你今天做了什么、明天准备做什么。',
  'dailyReport.workTitle': '今日工作(逐条记录,每条一件事) *',
  'dailyReport.workPlaceholder': '例如:拜访 Marina Bay,推进到方案报价阶段',
  'dailyReport.planTitle': '明日计划(逐条记录,每条一件事) *',
  'dailyReport.planPlaceholder': '例如:跟进 Raffles 报价',
  'dailyReport.paymentTitle': '回款进展(可选,可加多条)',
  'dailyReport.paymentPlaceholder': '例如:Marina Bay 第二期款 $50k 已到账',
  'dailyReport.problemTitle': '遇到的问题(可选,可加多条 – 会通知上级)',
  'dailyReport.problemPlaceholder': '例如:客户卡在采购审批,需要协助加速',
  'dailyReport.addRow': '再加一条',
  'dailyReport.delete': '删除',
  'dailyReport.followupTitle': '今日客户跟进',
  'dailyReport.followupDesc': '在这里登记你今天接触过的客户 —— 不用再单独到每条商机里逐一录入，系统会自动把它们写入对应商机的跟进记录。',
  'dailyReport.followupEmpty': '今天还没登记客户跟进。点击下方「+ 添加跟进」记录一次电话/微信/拜访/方案。',
  'dailyReport.followupPlaceholder': '例如:电话拜访 Marina Bay,确认方案需求',
  'dailyReport.followupAdd': '+ + 添加一条客户跟进',
  'dailyReport.issueTitle': '重大事项 / 需协助跟进(可加多条)',
  'dailyReport.issueDesc': '今天有什么需要领导或其他部门关注、拍板、协调的事项？一天可能有多件 —— 例如：大单卡审批 / 客户高层投诉 / 跨部门资源调度 / 集团政策征询。填写后会同步显示在 Today 页面，相关方可立即看到并跟进。',
  'dailyReport.issueEmpty': '今天没有需要上报的事项。如有，点击下方「+ 添加」',
  'dailyReport.issuePlaceholder': '例如:HK Hospitality 15% discount 需 CSO 拍板',
  'dailyReport.issueAdd': '+ + 新增一条事项',
  'dailyReport.moodTitle': '今日心情',
  'dailyReport.mood.sad': '难过/生气',
  'dailyReport.mood.upset': '委屈',
  'dailyReport.mood.neutral': '平淡',
  'dailyReport.mood.happy': '开心',
  'dailyReport.mood.excited': '大笑/兴奋',
  'dailyReport.cancel': '取消',
  'dailyReport.save': '保存日报',
  'dailyReport.error.workRequired': '请至少填写一项今日工作',
  'dailyReport.error.planRequired': '请至少填写一项明日计划',
}

const locales = ['zh-CN.json', 'zh-HK.json', 'en-US.json', 'th-TH.json', 'id-ID.json', 'vi-VN.json']
for (const file of locales) {
  const data = loadJson(file)
  for (const [path, value] of Object.entries(additions)) {
    if (!path.split('.').reduce((o, p) => o?.[p], data)) {
      setPath(data, path, value)
    }
  }
  saveJson(file, data)
  console.log(`Updated ${file}`)
}
