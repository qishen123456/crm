import { readFileSync, writeFileSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'
import { translate } from 'google-translate-api-x'

const __dirname = dirname(fileURLToPath(import.meta.url))
const localesDir = join(__dirname, '../src/locales')

function loadJson(name: string) {
  return JSON.parse(readFileSync(join(localesDir, `${name}.json`), 'utf-8'))
}

function saveJson(name: string, data: any) {
  writeFileSync(join(localesDir, name), JSON.stringify(data, null, 2) + '\n')
}

function hasChinese(s: string): boolean {
  return /[\u4e00-\u9fff]/.test(s)
}

function collectPaths(obj: any, path: string[] = []): string[] {
  if (typeof obj === 'string') return [path.join('.')]
  if (Array.isArray(obj)) return obj.flatMap((item, idx) => collectPaths(item, [...path, String(idx)]))
  if (obj && typeof obj === 'object') {
    return Object.entries(obj).flatMap(([key, value]) => collectPaths(value, [...path, key]))
  }
  return []
}

function getValue(obj: any, path: string[]): any {
  let cur = obj
  for (const p of path) {
    cur = cur?.[p]
    if (cur === undefined) return undefined
  }
  return cur
}

function setValue(obj: any, path: string[], value: any) {
  let cur = obj
  for (let i = 0; i < path.length - 1; i++) {
    cur[path[i]] = cur[path[i]] || {}
    cur = cur[path[i]]
  }
  cur[path[path.length - 1]] = value
}

const targets: Record<string, string> = {
  'en-US': 'en',
  'th-TH': 'th',
  'id-ID': 'id',
  'vi-VN': 'vi',
}

async function main() {
  const zhCN = loadJson('zh-CN')
  const paths = collectPaths(zhCN)

  for (const [file, lang] of Object.entries(targets)) {
    console.log(`Translating ${file} to ${lang}...`)
    const data = loadJson(file)
    const toTranslate: { path: string[]; value: string }[] = []

    for (const pathStr of paths) {
      const path = pathStr.split('.')
      const sourceValue = getValue(zhCN, path) as string
      const targetValue = getValue(data, path) as string
      if (typeof sourceValue === 'string' && hasChinese(sourceValue) && targetValue === sourceValue) {
        toTranslate.push({ path, value: sourceValue })
      }
    }

    console.log(`  ${toTranslate.length} strings to translate`)
    const batchSize = 5
    for (let i = 0; i < toTranslate.length; i += batchSize) {
      const batch = toTranslate.slice(i, i + batchSize)
      const results = await Promise.all(
        batch.map(async ({ value }) => {
          try {
            const res = await translate(value, { from: 'zh-CN', to: lang, autoCorrect: false })
            return res.text
          } catch (err) {
            console.error(`  Failed to translate: ${value}`, err)
            return value
          }
        }),
      )
      batch.forEach(({ path }, idx) => {
        setValue(data, path, results[idx])
      })
      console.log(`  Translated ${Math.min(i + batchSize, toTranslate.length)}/${toTranslate.length}`)
      await new Promise((resolve) => setTimeout(resolve, 300))
    }

    saveJson(file, data)
    console.log(`  Saved ${file}`)
  }
}

main().catch(console.error)
