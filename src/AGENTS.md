# Source Tree Guide

This document applies to `/src` only. Keep changes aligned with the current Vue 3 + Vite + reka-ui + Tailwind CSS v4 structure already used here. **There is no Naive UI in this project** — do not reintroduce it.

## Core architecture

- `main.ts` is bootstrap only. It creates the Vue app, installs Pinia and the router, loads global styles, sets `window.$message`, kicks off `setupIconify()`, and mounts `App.vue`. Do not move feature logic into bootstrap.
- `App.vue` is the app shell. It owns global layout, mounts `<Toaster>` (vue-sonner) and `Provider`, runs startup lifecycle wiring (`initApp()` / `destroyInitManager()` from `@/utils/api/init`), and `KeepAlive`s `HomeView`.
- `src/router/index.ts` defines exactly two lazy routes:
  - `/` → `@/views/HomeView.vue`
  - `/instance/:id` → `@/views/InstanceDetail.vue`
- The router has **no guards** today. Do not add one unless there is a real need.

## Authoring conventions

- Use the Composition API with `<script setup lang="ts">`.
- Prefer `@/` imports for source-local modules instead of long relative paths.
- Keep files typed and repo-consistent with existing imports, computed state, and helper usage.

## UI library (`src/components/ui/`)

`src/components/ui/` is the local shadcn-vue-style component library (alert, avatar, back-top, badge, button, card-x, empty, input, progress-thin, sonner, spinner, tabs, tooltip). Each component:

- Wraps a `reka-ui` primitive (or composes lower-level primitives) when applicable.
- Declares variants with `class-variance-authority` and merges classes via `cn()` from `@/lib/utils` (which combines `clsx` + `tailwind-merge`).
- Uses Tailwind utilities; design tokens are CSS variables defined in `@/styles/v2/tokens/tokens.css` (OKLCH, with `.dark` overrides via `@custom-variant dark`).

When you need a new piece of UI:

1. Compose existing primitives from `src/components/ui/` first.
2. If a primitive is missing, add it following the same pattern (reka-ui + cva + `cn()`), not by pulling in another component library.
3. Do not introduce per-component SCSS files or scoped styles for things Tailwind already covers.

## Views

- Views orchestrate data already exposed by stores and utils.
- `HomeView.vue` coordinates search, grouping, view-mode selection, scroll restore, and route navigation.
- `InstanceDetail.vue` coordinates node detail presentation and chart tabs for a selected node.
- Keep `HomeView` named with `defineOptions({ name: 'HomeView' })` so `App.vue`'s `KeepAlive :include="['HomeView']"` keeps working.
- Heavy node and chart UI must stay lazily loaded with `defineAsyncComponent`, as already done for `NodeCard`, `NodeGeneralCards`, `NodeList`, `LoadChart`, and `PingChart`.

## Stores

- Pinia stores are setup stores and are the source of truth for app state.
- `@/stores/app` owns public settings, theme-derived config, login state, layout flags, formatting preferences, theme mode, and persisted UI state.
- `@/stores/nodes` owns normalized node data, group derivation, WebSocket state, and node updates.
- Components and views should read from stores, not recreate parallel state for the same domain.
- When behavior depends on `publicSettings.theme_settings`, follow the existing defensive pattern in `@/stores/app`: `typeof` checks, guarded `JSON.parse`, valid-value filtering, and defaults. The settings schema lives in `komari-theme.json` (`configuration.data`).

## Utils

- `src/utils` owns transport, formatting, lookups, and startup orchestration.
- Keep API and RPC access in `@/utils/api/api` and `@/utils/api/rpc`.
- Keep startup, transport selection, polling, reconnects, and WebSocket fallback in `@/utils/api/init`.
- Keep formatting in helpers such as `@/utils/format/helper` and record shaping in `@/utils/recordHelper`.
- Keep region, OS, and tag lookup logic in their dedicated helper modules (`regionHelper`, `osImageHelper`, `tagHelper`).
- `@/utils/misc/message` is the wrapper exposed as `window.$message`. It calls into `vue-sonner`'s `toast`.
- Views and components must reuse these helpers instead of duplicating parsing, formatting, lookup, or transport code.

## App globals

- Only one app global exists on `window`: `$message`. It is typed in `src/types/global.d.ts`. Keep that file in sync if you add/remove a global.
- There is **no** `$dialog`, `$notification`, or `$loadingBar`. Do not assume Naive-UI-style provider APIs.
- Theming: `Provider.vue` drives `useDark()` from `@vueuse/core` (storage key `vueuse-color-scheme`) and toggles `.dark` on `<html>`. Source of truth for the user-chosen mode is `useAppStore().themeMode` (`'auto' | 'light' | 'dark'`).
- Build-time constants `__BUILD_VERSION__` and `__BUILD_GIT_HASH__` are also declared in `src/types/global.d.ts` and injected by `vite.config.ts`.

## Icons

- UI icons render through `@/components/PixelIcon.vue` (`<PixelIcon name="tabler:coin" :size="28" />`).
  It resolves the name via `@/utils/media/pixelIcons` to an AI-generated pixel sprite in `src/assets/pixel-icons/`;
  when no pixel art exists for that name it falls back to `@iconify/vue`, so nothing ever renders blank.
- Add new pixel icons by dropping a 16px-logical PNG (1px `#3e2723` outline, ≤10 colors, 4× nearest-upscaled
  to 64×64) into `src/assets/pixel-icons/` and listing it in `@/utils/media/pixelIcons.ts` plus the iconify mapping.
- Iconify remains the fallback pipeline (`<Icon icon="..." />` still works); do **not** add `lucide-vue-next`
  or any other icon-as-component package.
- Lucide icons are available via the `lucide:` prefix (e.g. `lucide:x`, `lucide:minus`). Do **not** add `lucide-vue-next` or any other icon-as-component package — the project deliberately routes everything through Iconify so there is a single icon pipeline.

## Styles

- Single global stylesheet entry: `@/styles/v2.css`（分 tokens/ base/ components/ 三层）。 It imports `tailwindcss` and `tw-animate-css`, declares the `dark` custom variant, and defines OKLCH design tokens for both modes. **No SCSS, no UnoCSS.**
- Component-level styling should be Tailwind utilities composed with `cn()`, not scoped `<style>` blocks, unless there is a genuine reason (e.g. animations or selectors Tailwind cannot express cleanly).

## Validation

- Validate source-tree changes with:
  - `bun run test`（vitest，当前 422 条用例，改动必须全绿）
  - `bunx vue-tsc --noEmit`
  - `bun run build`
