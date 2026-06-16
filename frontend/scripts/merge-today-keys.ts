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
  'today.reportSubmitted': '今日日报已提交',
  'today.reportSavedHint': '日报已保存，可随时点击右侧按钮查看或修改。',
  'today.viewReport': '查看日报',
  'today.streakDays': '已连续{count}天提交',
  'today.reportSaveSuccess': '日报已保存',
  'today.followUps': '今日待跟进',
  'today.alertLevel.urgent': '紧急',
  'today.alertLevel.high': '高',
  'today.alertText.hkHospitalityDiscount': 'HK Hospitality 集团总部要求 15% 一次性 discount 作为框架协议条件，涉及 5 年合作金额 $3.8M。当前我们的折扣权限是 8%，需 CSO 决策。',
  'today.alertText.marinaBayContract': 'Marina Bay 合同 22 天后到期，客户 CFO Olivia 要求增加「3 年内任意 1 次免费更换主件」条款，涉及成本约 $80k。需法务和高管决策是否接受。',
  'today.todoTitle.noFollowUp': '无跟进',
  'today.todoTitle.expiring': '即将到期',
  'today.todoTitle.reminder': '提醒',
  'today.todoText.hkHospitalityNoFollowUp': 'HK Hospitality Corp — 已 28 天未更新',
  'today.todoText.gentingNoFollowUp': 'Genting Group — 已 25 天未更新',
  'today.todoText.bangkokMallNoFollowUp': 'Bangkok Mall Group — 已 31 天未更新',
  'today.todoText.marinaBayExpiring': 'Marina Bay Sands 合同 21 天后到期',
  'today.todoText.soekarnoExpiring': 'Soekarno Retail Distribution 合同 5 天后到期',
  'today.todoText.rafflesEndUserInfo': '请收集 Raffles Hospitality 的终端用户信息（赢单后 95 天）',
  'today.followUpStage.proposal': '方案',
  'today.followUpStage.contact': '联系',
  'today.followUpTask.mgmPricingPushback': 'Follow up on pricing pushback',
  'today.followUpTask.rafflesCatalogue': 'Send F&B catalogue + reference list',
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
