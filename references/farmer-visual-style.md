# Farmer Visual Style Schema

Version: v0.2.0
Activation: `data-theme="farmer"` on `<html>` via `useVisualStyle`

## Theme options

- `farmer`: pixel/ pastoral UI kit, pixel panoramic background, pixel font for key cards.
- `baseline`: default neon/shader background.

## Token requirements

Must declare for both light and dark appearances:

- `--bg-0`, `--surface`, `--surface-elev`, `--surface-sunken`
- `--border`, `--border-subtle`, `--border-strong`, `--hairline`
- `--text-primary`, `--text-secondary`, `--text-tertiary`, `--text-on-strong`
- `--fill-secondary`, `--fill-tertiary`, `--hover-bg`, `--progress-bg`
- `--progress-cpu`, `--progress-memory`, `--progress-swap`, `--progress-disk`, `--progress-network`, `--progress-load`
- `--status-success`, `--status-warning`, `--status-error`, `--status-info`
- `--accent-500`, `--accent-strong`
- `--speed-idle`, `--speed-low`, `--speed-high`, `--speed-max`
- `--traffic-up`, `--traffic-down`, `--status-online`, `--status-offline`
- `--ring`, `--shadow-card`

## Visual geometry tokens

- `--visual-radius-card`, `--visual-radius-panel`, `--visual-radius-control`
- `--visual-border-width`, `--visual-panel-shadow`

## Typography

- `image-rendering: pixelated` under visual style.
- Pixel font for `.server-card, .compact-node-card, .mini-node-card, .overview-card, .node-list, .instance-panel, .theme-masthead, .surface-inset`.

## Background contract

- Replace default shader with static panoramic when `data-theme="farmer"`.
- Both modes define `--bg-image-desktop|mobile` via （已移除的 v1 背景素材）.
- Provide `--bg-scrim`, `--bg-size`, `--bg-position`.

## Accessibility

- WCAG AA contrast between `--text-primary` / `--surface` and `--text-primary` / `--bg-0`.
- `:focus-visible` uses `var(--ring)`.
