import { readFileSync, writeFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
// @ts-ignore
import * as OpenCC from 'opencc-js'

const __dirname = dirname(fileURLToPath(import.meta.url))
const localesDir = join(__dirname, '../src/locales')

const zhCN = JSON.parse(readFileSync(join(localesDir, 'zh-CN.json'), 'utf-8'))

function traverse(obj: any, converter: (s: string) => string): any {
  if (typeof obj === 'string') return converter(obj)
  if (Array.isArray(obj)) return obj.map((item) => traverse(item, converter))
  if (obj && typeof obj === 'object') {
    const result: any = {}
    for (const [key, value] of Object.entries(obj)) {
      result[key] = traverse(value, converter)
    }
    return result
  }
  return obj
}

const converter = OpenCC.Converter({ from: 'cn', to: 'tw' })
const zhHK = traverse(zhCN, converter)
writeFileSync(join(localesDir, 'zh-HK.json'), JSON.stringify(zhHK, null, 2) + '\n')
console.log('Wrote zh-HK.json')

// Placeholder locales for th-TH, id-ID, vi-VN
function makePlaceholder(locale: string, prefix: string) {
  return traverse(zhCN, (s: string) => {
    // For nested keys that are object keys or non-text, keep as-is
    // Simple heuristic: if string looks like a code/number, keep it
    if (/^\s*\{.*\}\s*$/.test(s) || /^[0-9$%#\.\-\\/]+$/.test(s)) return s
    return `${prefix}${s}`
  })
}

for (const [locale, prefix] of [
  ['th-TH', '[th] '],
  ['id-ID', '[id] '],
  ['vi-VN', '[vi] '],
]) {
  const data = makePlaceholder(locale, prefix)
  writeFileSync(join(localesDir, `${locale}.json`), JSON.stringify(data, null, 2) + '\n')
  console.log(`Wrote ${locale}.json`)
}
