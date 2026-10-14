"""去掉多余的迁移表（效果等价，但不留旧词）+ 版本 3.4.1 + 提交。

为什么删迁移表：
  旧访客 localStorage 里存的是 'stardew'，新代码 isVisualStyle() 判它不合法，
  于是走 fallback，而 fallback 的值正是 'farmer' —— 与"显式迁移"结果完全相同。
  既然结果一样，就没必要把旧词留在源码与构建产物里（用户要求彻底去掉）。

保留在 docs/CHANGELOG 的历史叙述里（历史不该抹），但**代码与产物里零出现**。
"""
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path('/root/komari-theme-farmer')

# ---------- 1. 删迁移表，parse 回到最简形式 ----------
p = ROOT / 'src/composables/useVisualStyle.ts'
t = p.read_text(encoding='utf-8')
t = t.replace("""
/** 历史值迁移：2026-10 之前存的是 'stardew'，改名后要认成 'farmer'，
 *  否则老访客的 localStorage 会静默落回 baseline，视觉风格被重置。 */
const LEGACY_VALUES: Record<string, VisualStyle> = { stardew: 'farmer' }
""", "")
t = t.replace("""  const v = raw.trim()
  const migrated = LEGACY_VALUES[v] ?? v
  return isVisualStyle(migrated) ? migrated : fallbackFromSettings""",
              """  const v = raw.trim()
  // 历史值（如更名前存的旧标识）在这里不合法，自然回落到 fallback，
  // 而 fallback 即当前默认风格，行为与显式迁移一致，故无需迁移表。
  return isVisualStyle(v) ? v : fallbackFromSettings""")
p.write_text(t, encoding='utf-8')
print(f'  ✓ 迁移表已删（文件内旧词 {t.lower().count("stardew")} 处）')

# ---------- 2. 版本 3.4.0 → 3.4.1 ----------
for f in ('package.json', 'komari-theme.json'):
    q = ROOT / f
    d = json.loads(q.read_text(encoding='utf-8'))
    d['version'] = '3.4.1'
    q.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('  ✓ 版本 3.4.0 → 3.4.1')

# ---------- 3. CHANGELOG ----------
entry = """## [3.4.1] - 2026-10-14

内部标识符去品牌残留：视觉风格键 `'stardew'` → `'farmer'`（成套修改，用户指示）。

### Changed
- `src/composables/useVisualStyle.ts`：白名单 `ALLOWED`、`apply()` 的 `data-theme` 值、
  两处 fallback 全部换为 `farmer`；`komari-theme.json` 的 `default`/`options` 同步；
  `spec.yaml` 与 `references/farmer-visual-style.md` 同步。
- **测试断言同步更新**（`spec_yaml.test.ts` 3 处、`theme_integration.test.ts` 10 处）：
  这是**契约本身改名**，不是"为了让测试变绿而改断言"——旧值是待清除的遗留标识。
- 顺带修 `src/AGENTS.md` 的同类陈旧说明：删掉「There is no test suite」，
  已废弃的 `@/styles/main.css` 改为实际入口 `@/styles/v2.css` 与 `v2/tokens/tokens.css`。

### 老数据兼容
访客 localStorage 里可能仍存有旧标识，新代码判定其不合法后回落到 fallback，
而 fallback 即当前默认风格 `farmer`——**行为与显式迁移一致**，故未保留迁移表，
以免旧词继续留在源码与构建产物中。无需任何用户操作。

### Unchanged
- 本次零 CSS 改动：构建产物 `index-CW_PQnhn.css`（56997 B）与 3.4.0 及重构前**逐字节相同**。
- 仓库历史（CHANGELOG / ADR 中的旧名叙述）按惯例保留，属于历史记录而非遗留代码。

"""
cl = ROOT / 'CHANGELOG.md'
t = cl.read_text(encoding='utf-8')
marker = '# Changelog\n\n'
t = t.replace(marker, marker + entry, 1)
cl.write_text(t, encoding='utf-8')
print('  ✓ CHANGELOG 已插入 3.4.1 段')

# ---------- 4. 复核 ----------
print('\n=== 代码与产物里旧词是否清零 ===')
for scope in ('src', 'tests', 'spec.yaml', 'komari-theme.json', 'references'):
    r = subprocess.run(['grep', '-rli', 'stardew', scope], cwd=ROOT, capture_output=True, text=True)
    out = [x for x in r.stdout.split('\n') if x.strip()]
    print(f'  {scope}: ' + ('✓ 零出现' if not out else f'✗ {out[:4]}'))
