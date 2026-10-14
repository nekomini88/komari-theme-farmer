"""P6 第一步：版本号 3.3.2 → 3.4.0 + 写 CHANGELOG（照仓库既有格式）。
按用户铁律「批量验收全绿才发布」：本步只落本地提交，**不推送**，
待只读质检子代理通过后再推（推送会触发 Release On Version Bump 工作流）。
"""
import json
import pathlib

ROOT = pathlib.Path('/root/komari-theme-farmer')

# ① 版本号
for f in ('package.json', 'komari-theme.json'):
    p = ROOT / f
    d = json.loads(p.read_text(encoding='utf-8'))
    old = d.get('version')
    d['version'] = '3.4.0'
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'  ✓ {f}: {old} → 3.4.0')

# ② CHANGELOG 插到最前（保持仓库的 [版本] - 日期 + Changed/Added 格式）
entry = """## [3.4.0] - 2026-10-14

全量重构：**只动结构，不动行为**。每个阶段独立提交、可单独回退，全部以
「测试全绿 + 类型零错 + 构建产物零变化」验收。

### Added
- 测试套件 243 → **422 条**（新增 region-helper 40 / rpc-api 87 / stores 52 等），
  作为重构的契约；`regionHelper.ts` 覆盖率 100%（语句/分支/函数）。
- `docs/known-quirks.md`：记录重构期间推导断言时发现的 5 个既有古怪行为，
  **故意未修**（改行为不属重构范围），附每条的修法与修前必查项。

### Changed
- `src/utils/regionHelper.ts` 1709 → **156 行**：1556 行地区映射数据表拆至
  `src/data/regionMap.ts`。数据按行原样搬运并**逐字节校验一致**（258 条一条未丢），
  原文件保留转导出，既有 import 零改动。
- `src/utils/` 按职责分层为 `api/ region/ media/ format/ misc/`（11 个文件 `git mv`，历史保留）。
  `serverClock.ts` 刻意保留原位：有测试断言 `App.vue` 源码含 `@/utils/serverClock` 字面量。
- `src/stores/app.ts` 416 → **97 行**、`nodes.ts` 415 → **53 行**，内部按职责拆分，
  **公开 state/action/getter 契约与行为零变更**（由 52 条 store 断言锁定）。
- `src/styles/v2/` 分层为 `tokens/ base/ components/`，构建产物
  `index-CW_PQnhn.css`（56997 B）与重构前**逐字节相同**——CSS 字节一致即渲染不可能变。

### Fixed
- 仓库说明的误导项：删除「There is no test suite / Do not invent bun test」错误告示
  （本仓库实有 422 条用例），旧项目名 `emerald` 与旧 zip 命名一并归正。
- 4 处测试的样式表路径与 1 处非递归目录扫描（样式表进入子目录后必须递归），
  属**引用同步**，断言语义未变。

### Unchanged
- `data-theme='stardew'` 与 `useVisualStyle` 白名单原样保留（沿用 3.3.0 的 A 档口径；
  该键绑定 12 个 legacy 样式文件的选择器与 3 条既有测试断言）。
- 5 个既有古怪行为未修，已归档至 `docs/known-quirks.md`。

"""
cl = ROOT / 'CHANGELOG.md'
t = cl.read_text(encoding='utf-8')
marker = '# Changelog\n\n'
assert marker in t, 'CHANGELOG 头部格式与预期不符，请人工处理'
t = t.replace(marker, marker + entry, 1)
cl.write_text(t, encoding='utf-8')
print('  ✓ CHANGELOG.md 已插入 3.4.0 段')
