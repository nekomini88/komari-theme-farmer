# Changelog

## [3.4.1] - 2026-10-14

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

## [3.4.0] - 2026-10-14

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

## [3.3.0] - 2026-10-13

主题更名：**Komari-Stardew → Komari-Farmer**（用户口径：「修改为 Komari-famer（农场，与星露谷物语没有关系）」）。

本次按用户选定的 **A 档口径**执行：只改「活的身份标识 + 文档」，不动任何业务代码与历史记录。

### Changed
- 主题清单 `komari-theme.json`：`name` / `short` 改为 `Komari-Farmer`；`description` 去掉星露谷品牌、
  改为农场主题描述；`url` 指向新仓库 `komari-theme-farmer`；设置组名 `Emerald 设置` → `Komari-Farmer 设置`；
  设置里视觉风格项的说明文案去掉品牌字样。
- 产物命名：`komari-theme-Komari-Stardew-<版本>-<hash>.zip` → `komari-theme-Komari-Farmer-<版本>-<hash>.zip`；
  package.json 的 `name` 同步为 `komari-theme-farmer`；自动发版工作流的附件 glob 同步。
- 文档：README / AGENTS / spec.yaml / CHANGELOG / docs/rollback.md 的对外名称与描述全部换新；
  `references/stardew-visual-style.md` → `references/farmer-visual-style.md`；
  `docs/adr/ADR-001-stardew-theme.md` → `docs/adr/ADR-001-farmer-theme.md`；
  `STARDew-V7-README.md` → `FARMER-V7-README.md`。
- 活代码注释里点名的参考稿说法改为中性的「参考稿」。

### Unchanged（A 档显式保留，非遗漏）
- **视觉风格内部键 `data-theme='stardew'` 与 `useVisualStyle` 的 `['stardew','baseline']` 白名单原样保留**：
  该键与 12 个 legacy 样式文件的选择器、3 个既有测试断言绑定，属内部标识符而非主题名；
  改动它需要同时动 legacy 死文件或删测试断言，超出本档范围。对外不可见（仅内部数据键）。
- v1 时代 legacy 组件与样式文件（`src/components/{Background,FloraFaunaOverlay,TopStatsGrid,…}.vue`、
  `src/styles/{main,visual-styles,matte-pixel,hard-pixel-core,…}.css`）按口径整体不动，其中仍含旧品牌字样。
- CHANGELOG 与 ADR 的历史条目保持原样（记录即记录，不回改历史）。

### 验证
- 单测全绿（含 spec.yaml 规格断言、产物命名断言）
- 发布包名、部署目录名、GitHub 仓库名三者一致

## [3.0.0] - 2026-10-13

像素风面板的正式版：卡片本体按《星露谷物语主题.pdf》逐项对齐，数据密度补到「有实际容量」为止。
（版本号说明：编号历史里有 2026-07-31 的初版 1.0.0、以及早期 2.x 线；本版按用户口径跳过这些历史，直接把「像素风面板」定为一个更大的里程碑 3.0.0。）

### Added
- **卡片实际容量明细**（此前只有百分比，看不出关键信息）：CPU 给出 1/5/15 分钟负载 + 核数
  （`0.01, 0.01, 0.00 (1c)`）；Memory / Disk 给出「已用 / 总量」（`244.7 MB / 932.3 MB`、`3.2 GB / 7.7 GB`）。
  总量或核数缺失时退化为只显示已用，不留 ` / ` 尾巴与 `(0c)` 噪声。
- **参考稿美术底板**：擦掉原图烘死的文字/数值/进度条/国旗，保留叶藤横幅、纸底、左上盆栽、右下向日葵；
  按 6 个配色槽做 HSV 色相变体（保留原始明暗与描边），卡片以底图铺装 + CSS 叠实时数据。
- **每台一色**：配色取参考稿跨 6 张设计稿的实测套色（绿 `#229900` / 蓝 `#2b8ced` / 紫 `#7a24c7`
  / 粉 `#e63e5f` / 橙 `#e68900` / 青 `#00aba7`）；稳定哈希 + 贪心避让分配，同批 ≤6 台两两不同色，
  筛选 / 排序 / 刷新均不换色。
- **像素字与像素图标**：Fusion Pixel 12px（OFL）零抗锯齿；图标走 16 的整数倍（1×/2×），
  消失的页面类样式（`.vk-overview*`、`.vk-home*`）一并补回。
- **自动审核单测**（`v2-pixel-invariants` 等）：直接解码底板 PNG 取横幅实测色、按 WCAG 实算文字对比度
  （大号文本 3:1 门槛），并做过反向验证（故意写回错误配对会失败）。

### Changed
- **服务器名称真正居中且贴顶**：`.vk-panel` 的 `padding` 归零让横幅贴卡片顶端（原先被压低 17px）；
  横幅内去掉 32px 图标，改三列网格 `1fr minmax(0, 62%) 1fr`（两翼等宽 ⇒ 名称自身精确居中），
  国旗 + 状态点收进 `.vk-panel-meta` 紧跟名称右侧（对齐参考稿「横幅内无图标、国旗紧跟名称」）。
  实测 6/6 卡片名称偏差 0.0px。
- 卡片结构改为「横幅条 + 角饰锚定 + 正文高度由内容决定」：不再锁 `aspect-ratio`
  （曾导致正文比卡片高 113px，最下两行指标被 `overflow: hidden` 静默裁掉）。
- 进度条绿由旧母板的灰绿 `#7fa851` 改为参考稿实测亮绿 `#2a9708`；等级警示选择器修正
  （原写 `alert`/`danger`，而 `usageLevel()` 返回 `ok`/`warn`/`crit`，规则从不生效）。

### Fixed
- **部署漏资源**：线上 `dist/images/` 缺 `v2-panel` 与 `v2-scene`，卡片底板与场景图并未真正发布；
  重做部署后齐全。
- **测试偶发**：两处 `mountHome` 用固定 flush 轮数等异步，全量并行时异步链更慢会早查，
  同一批用例在不同 run 里交替失败 → 改为轮询条件等待；连跑 3 次稳定全绿。
- 手机端像素发虚：根因是图标取 20px（非 16 的整数倍，每逻辑像素落 3.75 设备像素）；
  顶栏改像素纸面板、按钮加 `white-space: nowrap`（窄屏不再折成竖排）。

### Verification
- 单测 214/214（22 文件，连跑 3 次稳定）；几何审计 10/10（等宽等高、无溢出、名称居中、
  不与图标/国旗重叠、比例接近参考稿 428/394 = 1.086）。

## [0.121.0] - 2026-10-12

### Changed
- **场景世界的时间基准改为「我们的时间（UTC+8）」**：时间 / 季节 / 天气不再由访客本地时钟驱动，
  改为取服务端 HTTP `Date` 响应头建立锚点（复用启动时既有的 `/api/public` 等请求，**零额外请求**），
  并用请求往返中点抵消 RTT，访客时钟只当滴答器。访客系统时间不准或身处其他时区，看到的世界完全一致。
- 场景状态改为每 60s 重算一次，日夜与季节会自然推进（原来仅在页面加载时算一次就固定）。
- 天气判定新增按显式「年月日」取种的 `weatherFromDaySeed()`，避免 `Date` 本地 getter 按访客时区取错日期；
  `weatherFromDate()` 保留但仅作兼容。

### Added
- 新增 6 个后台配置项（`komari-theme.json` → 分组「场景世界（时间 / 季节 / 天气）」）：
  `sceneTimeMode` / `sceneFixedTime` / `sceneSeasonMode` / `sceneFixedSeason` /
  `weatherMode`（`off` / `auto` / `fixed` 三态，默认 `auto`）/ `weatherFixed`
- 新增 `utils/serverClock.ts`（世界时钟）与 `v2/theme/sceneConfig.ts`（配置解析），均带单测；
  并新增契约测试：配置项 `options` 白名单必须与代码枚举逐项一致，防止脱钩

### Removed
- **移除全部 URL 覆盖口**（`?scene=` / `?season=` / `?weather=` / `?life=`）：
  此前任何访客改 URL 即可改世界，与「场景由管理员设置」冲突。今后手动覆盖只走配置项。

## [0.114.0] - 2026-10-11

### Added
- 生态 / 天气精灵换成 AI 生成的像素 sprite（22 张 32×32）：鸟、兔子、萤火虫、云、雾缕、冰、闪电、雨滴、雪花、星星，
  以及**蝴蝶 / 花 / 叶的四季变体**（逐色单独生成，不做色相旋转改色）
- 界面图标换成像素 sprite（44 张 16×16），新增 `PixelIcon.vue` + `utils/pixelIcons.ts`：
  找不到像素图时自动回落 Iconify 矢量图标，不会空白
- 新增流量图标三件套（总量 / 上行 / 下行），解决原来三张统计卡共用一个图标、分不清上下行的问题

### Changed
- 生态层渲染改为按当前季节取图（`spriteOf()`），`lightning` 不再复用雾缕贴图
- 删除旧的矢量 sprite（`src/assets/sprites/*.svg`），全部由像素 PNG 取代

### Fixed
- 抠图管线补洞：白云、白兔这类"白主体 + 白底"的素材不再被整块抠成空白

## [0.54.0] - 2026-08-01

### Fixed
- 背景改为完整像素田园图 `bg-sky.png`（蓝天/草地/远山），对齐 PDF 与 preview
- 移除 hard-pixel-core 对场景层的 `background-image: none` / 全局 `box-shadow: none` 破坏
- 页面底色改为天空蓝，避免出现深蓝斜纹底

### Changed
- TopStatsGrid 改为木牌布局 + 像素图标（对齐 preview 木框卡片）
- NodeCard `.sd-card` 强制木纹边框与硬阴影


## [1.0.0] - 2026-07-31

### Added
- 新增 `stardew` 主题，对齐 Header 主题选择菜单
- `data-theme="farmer"` CSS 变量集合：matte cream / hard shadow / Nunito / pixel pill / dotted border
- `vitest` 单测 + 集成测试 + v8 coverage（lines >= 80%）
- `tests/unit/` + `tests/integration/` + `tests/fixtures/`
- GitHub Actions Release On Version Bump workflow
- ADR-001: Stardew 主题决策记录
- rollback docs

### Changed
- README 增加验收标准 DoD、使用说明、测试命令
- `vite.config.ts` zip 产物名改为 `komari-theme-Komari-Farmer-v-*.zip`
- `.gitignore` 修正 regex 警告，增加 `bun.lock` / `komari-theme-*.zip`

### Fixed
- CI Release 附件名从 neko 改为 stardew

### Security
- 排除未跟踪的 `README.md.orig`，避免临时文件泄露
## [0.1.1] - 2026-07-31

### Fixed
- fix release workflow zip attachment by bumping version to trigger release
