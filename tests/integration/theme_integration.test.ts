import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'

// 契约对齐（2026-10-13 v3.3.x：v1 legacy 分层已删除，断言全部指向活的 v2 层）：
// - 主题键真身 = 'Komari-Farmer'（komari-theme.json short）。
// - 视觉风格由 useVisualStyle 把 data-theme='farmer' 挂到 document.documentElement
//   （该键为内部标识符，与主题名无关，刻意沿用）；Provider.vue 消费 manifest 的 themeVisualStyle。
// - 活的样式层 = src/styles/v2.css 的 @import 集合（src/styles/v2/*.css）；
//   v1 的 main.css / visual-styles.css / matte-pixel.css / hard-pixel-core.css 已随 v1 层退役删除。
// - 顶栏为 src/v2/components/TopBar.vue（含 admin 入口）。

describe('theme integration', () => {
  it('exposes the farmer visual style through the manifest + useVisualStyle contract', () => {
    // 依据：komari-theme.json configuration.data → themeVisualStyle（type=select, default=farmer, options 含 farmer）
    const manifest = JSON.parse(readFileSync('komari-theme.json', 'utf-8'))
    const visual = manifest.configuration.data.find((d: { key?: string }) => d.key === 'themeVisualStyle')
    expect(visual?.type).toBe('select')
    expect(visual?.default).toBe('farmer')
    expect(String(visual?.options).split(',')).toContain('farmer')

    // 依据：src/composables/useVisualStyle.ts → ALLOWED=['farmer','baseline'] 且 apply() setAttribute('data-theme','farmer')
    const util = readFileSync('src/composables/useVisualStyle.ts', 'utf-8')
    expect(util).toContain('[\'farmer\', \'baseline\']')
    expect(util).toContain('setAttribute(\'data-theme\', \'farmer\')')
  })

  it('defines the design tokens in the live v2 token layers', () => {
    // 2026-10-13 迁移：原断言读 v1 的 visual-styles.css / main.css（已删）。
    // 不变量不变 —— 面板视觉令牌仍必须存在且落在活的 v2 样式层里。
    const tokens = readFileSync('src/styles/v2/tokens/tokens.css', 'utf-8')
    expect(tokens).toContain('--vk-')
    const card = readFileSync('src/styles/v2/components/card.css', 'utf-8')
    expect(card).toContain('--vk-panel')
  })
})

describe('matte pixel surfaces in the live v2 card layer', () => {
  it('mUST keep matte surfaces: pixel hard shadow and no glass blur', () => {
    // 2026-10-13 迁移：原断言读 v1 的 matte-pixel.css（已删）。
    // 不变量不变 —— 卡片必须是哑光像素面：有硬像素阴影、不得回退成玻璃模糊。
    const card = readFileSync('src/styles/v2/components/card.css', 'utf8')
    expect(card).toContain('box-shadow: 3px 3px 0 0')
    expect(card).not.toContain('backdrop-filter')
  })
})
