import { onMounted, watch } from 'vue'

const KEY = 'komaritheme:theme'
const KEY_DEFAULT = 'komaritheme:theme-default'
const KEY_SETTINGS = 'komaritheme:theme-visual-style-settings'
const ALLOWED = ['farmer', 'baseline'] as const
export type VisualStyle = (typeof ALLOWED)[number]

function isVisualStyle(value: unknown): value is VisualStyle {
  return typeof value === 'string' && (ALLOWED as readonly string[]).includes(value)
}

function readStorageItem(key: string): string | null {
  try { return localStorage.getItem(key) }
  catch { return null }
}

function writeStorageItem(key: string, value: string) {
  try { localStorage.setItem(key, value) }
  catch {}
}

function parse(raw: string | null, fallbackFromSettings: VisualStyle = 'farmer'): VisualStyle {
  if (!raw)
    return fallbackFromSettings
  const v = raw.trim()
  // 历史值（如更名前存的旧标识）在这里不合法，自然回落到 fallback，
  // 而 fallback 即当前默认风格，行为与显式迁移一致，故无需迁移表。
  return isVisualStyle(v) ? v : fallbackFromSettings
}

function apply(style: VisualStyle) {
  const root = document.documentElement
  if (style === 'farmer') {
    root.setAttribute('data-theme', 'farmer')
  }
  else {
    root.removeAttribute('data-theme')
  }
}

let current: VisualStyle = 'farmer'
let isReady = false

export function useVisualStyle() {
  const explicit = (): VisualStyle => {
    const raw = readStorageItem(KEY)
    if (raw !== null)
      return parse(raw)
    const fallback = readStorageItem(KEY_DEFAULT)
    if (fallback !== null)
      return parse(fallback)
    return parse(readStorageItem(KEY_SETTINGS), 'farmer')
  }

  onMounted(() => {
    current = explicit()
    apply(current)
    isReady = true
  })

  watch(
    () => current,
    (next) => {
      apply(next)
      writeStorageItem(KEY, next)
      isReady = true
    },
  )

  const setVisualStyle = (next: VisualStyle) => {
    current = next
  }

  const resetToDefault = () => {
    const def = parse(readStorageItem(KEY_DEFAULT))
    current = def
    apply(def)
    writeStorageItem(KEY, def)
    isReady = true
  }

  return {
    get current() { return current },
    setVisualStyle,
    resetToDefault,
  }
}
