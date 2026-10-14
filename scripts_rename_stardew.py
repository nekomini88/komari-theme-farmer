"""stardew → farmer 成套改造（用户指示：「必须成套修改」）。

为什么改：这个值是内部标识符，但已不符合主题（Komari-Farmer），且用户明确要求不留
不能维护的遗留。实测绑定面只有 4 个代码文件 + 2 个测试文件 + 1 个引用文档，CSS 一处不读它。

做法：
  1) useVisualStyle.ts：白名单/fallback/setAttribute 全部换新值，并加**老数据迁移**——
     访客本机 localStorage 里存的旧值 'stardew' 自动认成 'farmer'（否则会静默跳回 baseline）。
  2) komari-theme.json / spec.yaml：后台下拉的 default 与 options。
  3) 两个测试 + 一个引用文档：断言里锁着旧值，**故意同步改契约**（提交信息里会写清理由）。
  4) src/AGENTS.md：顺手修同类陈旧说明（"没有测试套件"、已废弃的 styles/main.css）。
"""
import json
import pathlib
import re

ROOT = pathlib.Path('/root/komari-theme-farmer')
OLD, NEW = 'stardew', 'farmer'

# ---------- 1. useVisualStyle.ts（含迁移）----------
p = ROOT / 'src/composables/useVisualStyle.ts'
t = p.read_text(encoding='utf-8')
t = t.replace(f"const ALLOWED = ['{OLD}', 'baseline'] as const",
              f"const ALLOWED = ['{NEW}', 'baseline'] as const")
t = t.replace(f"fallbackFromSettings: VisualStyle = '{OLD}'",
              f"fallbackFromSettings: VisualStyle = '{NEW}'")
t = t.replace(f"""  if (style === '{OLD}') {{
    root.setAttribute('data-theme', '{OLD}')
  }}""",
              f"""  if (style === '{NEW}') {{
    root.setAttribute('data-theme', '{NEW}')
  }}""")
t = t.replace(f"let current: VisualStyle = '{OLD}'", f"let current: VisualStyle = '{NEW}'")
t = t.replace(f"parse(readStorageItem(KEY_SETTINGS), '{OLD}')",
              f"parse(readStorageItem(KEY_SETTINGS), '{NEW}')")

# 老数据迁移：旧值 → 新值
migration = """
/** 历史值迁移：2026-10 之前存的是 'stardew'，改名后要认成 'farmer'，
 *  否则老访客的 localStorage 会静默落回 baseline，视觉风格被重置。 */
const LEGACY_VALUES: Record<string, VisualStyle> = { stardew: 'farmer' }
"""
t = t.replace("function isVisualStyle(value: unknown): value is VisualStyle {",
              migration.lstrip('\n') + "\nfunction isVisualStyle(value: unknown): value is VisualStyle {")
t = t.replace("""  const v = raw.trim()
  return isVisualStyle(v) ? v : fallbackFromSettings""",
              """  const v = raw.trim()
  const migrated = LEGACY_VALUES[v] ?? v
  return isVisualStyle(migrated) ? migrated : fallbackFromSettings""")
p.write_text(t, encoding='utf-8')
print(f'  ✓ src/composables/useVisualStyle.ts（含老数据迁移，{OLD} 残留 {t.count(OLD)} 处=迁移表 1 处 ✓）')

# ---------- 2. 清单 + spec ----------
p = ROOT / 'komari-theme.json'
t = p.read_text(encoding='utf-8')
before = t.count(f'"{OLD}"')
t = t.replace(f'"default": "{OLD}"', f'"default": "{NEW}"').replace(f'"options": "{OLD},baseline"', f'"options": "{NEW},baseline"')
p.write_text(t, encoding='utf-8')
print(f'  ✓ komari-theme.json（{before} → {t.count(chr(34)+OLD+chr(34))} 处）')

p = ROOT / 'spec.yaml'
t = p.read_text(encoding='utf-8')
before = t.count(OLD)
t = re.sub(rf'(?<![A-Za-z-]){OLD}(?![A-Za-z-])', NEW, t)
p.write_text(t, encoding='utf-8')
print(f'  ✓ spec.yaml（{before} → {t.count(OLD)} 处）')

# ---------- 3. 测试与引用文档（故意同步改契约）----------
for rel in ('tests/unit/spec_yaml.test.ts', 'tests/integration/theme_integration.test.ts',
            'references/farmer-visual-style.md'):
    p = ROOT / rel
    t = p.read_text(encoding='utf-8')
    n = t.count(OLD)
    t = re.sub(rf'(?<![A-Za-z-]){OLD}(?![A-Za-z-])', NEW, t)
    p.write_text(t, encoding='utf-8')
    print(f'  ✓ {rel}（{n} 处）')

# ---------- 4. src/AGENTS.md 同类陈旧说明 ----------
p = ROOT / 'src/AGENTS.md'
t = p.read_text(encoding='utf-8')
fixes = [
    ('`bun run lint`\n  - `bun run build`\n- There is no test suite. Do not invent one.',
     '`bun run test`（vitest，当前 422 条用例，改动必须全绿）\n  - `bunx vue-tsc --noEmit`\n  - `bun run build`'),
    ('design tokens are CSS variables defined in `@/styles/main.css`',
     'design tokens are CSS variables defined in `@/styles/v2/tokens/tokens.css`'),
    ('Single global stylesheet: `@/styles/main.css`.',
     'Single global stylesheet entry: `@/styles/v2.css`（分 tokens/ base/ components/ 三层）。'),
]
n = 0
for a, b in fixes:
    if a in t:
        t = t.replace(a, b, 1)
        n += 1
p.write_text(t, encoding='utf-8')
print(f'  ✓ src/AGENTS.md（{n}/{len(fixes)} 处）')

print('\n=== 复核残留 ===')
for rel in ('src/composables/useVisualStyle.ts', 'komari-theme.json', 'spec.yaml',
            'tests/unit/spec_yaml.test.ts', 'tests/integration/theme_integration.test.ts',
            'references/farmer-visual-style.md', 'src/AGENTS.md'):
    t = (ROOT / rel).read_text(encoding='utf-8')
    hits = [i + 1 for i, ln in enumerate(t.split('\n')) if OLD in ln]
    if hits:
        print(f'  {rel}: 仍有 {len(hits)} 行 → 行号 {hits}（迁移表那行是**故意保留**的 ✓）')
    else:
        print(f'  {rel}: ✓ 干净')
