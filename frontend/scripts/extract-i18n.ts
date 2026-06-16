import { bundles } from '../src/i18n'
import { writeFileSync, mkdirSync } from 'fs'
import { join, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const outDir = join(__dirname, '../src/locales')
mkdirSync(outDir, { recursive: true })

const mapping: Record<string, keyof typeof bundles> = {
  'zh-CN': 'zh',
  'en-US': 'en',
}

for (const [file, key] of Object.entries(mapping)) {
  const data = bundles[key]
  writeFileSync(join(outDir, `${file}.json`), JSON.stringify(data, null, 2) + '\n')
  console.log(`Wrote ${file}.json`)
}

// Write fr to a temporary file for reference, later we'll merge into en-US or keep separately
writeFileSync(join(outDir, 'fr-FR.json'), JSON.stringify(bundles.fr, null, 2) + '\n')
console.log('Wrote fr-FR.json (reference)')
