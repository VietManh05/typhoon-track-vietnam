# Typhoon VN — Weather Intelligence Design System

This file documents the frontend visual contract. Runtime values live in `src/index.css`; Tailwind aliases live in `tailwind.config.js`.

## Direction

- Product: real-time tropical cyclone monitoring and decision support.
- Visual language: dark scientific command center, calm density, map-first hierarchy.
- Principles: clarity before decoration, status never conveyed by color alone, restrained motion, compact controls, tabular numerical data.
- Avoid: pervasive glass, heavy shadows, animated gradients, oversized pills, decorative glow, mixed icon families.

## Color tokens

| Semantic role | Value |
| --- | --- |
| Background | `#07101F` |
| Surface 1 | `#0B1526` |
| Surface 2 | `#101C2F` |
| Elevated | `#142238` |
| Border source | `#94A3B8` at 12–22% |
| Primary | `#22D3EE` |
| Primary deep | `#38BDF8` |
| Secondary | `#8B5CF6` |
| Success | `#10B981` |
| Warning | `#F59E0B` |
| Danger | `#F43F5E` |
| Text primary | `#F8FAFC` |
| Text secondary | `#94A3B8` |
| Text muted | `#64748B` |

Storm classes use the same semantic palette: TD cyan, TS emerald, STS amber, TY orange, STY rose, SUPERTY violet.

## Typography

- UI: self-hosted Be Vietnam Pro, weights 400/500/600/700.
- Data: self-hosted JetBrains Mono, weights 400/500.
- Metadata 10–12px; secondary UI 12–13px; standard UI 14px; card title 16–18px; primary values 22–28px.
- All measurements use tabular figures and a non-breaking gap before units.

## Shape, spacing, elevation

- Spacing follows a 4/8px rhythm.
- Badge radius 6px, control radius 9px, card radius 12px, panel radius 14px.
- Panels use a 1px low-opacity border and one restrained shadow level.
- Touch targets are at least 40px in the dense web UI; primary mobile actions target 44px when space permits.

## Component rules

- `panel`: stable content surface; never clickable as a whole unless explicitly designed as a selector.
- `metric-tile`: icon, muted label, dominant value, compact secondary value.
- `btn-icon`: Lucide icon only, accessible name and native button semantics required.
- `badge`: reserved for category/state/risk; text label required in addition to color.
- `segmented`: mutually exclusive map modes. Toggle layers use `aria-pressed` chips.
- Warning cards keep a dark surface with warning border/icon; the whole card is never solid red.

## Layout

- Desktop ≥1280px: map/details grid approximately 62/38.
- Tablet <1280px: map first, details below.
- Mobile: horizontally scrollable storm selector, map height around 58vh, two-column metrics, collapsible legend.
- No page-level horizontal overflow. Internal tables and storm tabs may scroll in their own labeled region.

## Motion and accessibility

- Motion duration 150–250ms. Only state transitions and a subtle active-storm pulse may repeat.
- Respect `prefers-reduced-motion` globally.
- WCAG 2.2 AA text contrast, visible focus, semantic landmarks, keyboard-operable timeline/chart, labeled icon buttons, and focus-contained modal.
- Chart series differ by color and line pattern; a keyboard path and data table fallback are mandatory.

## Performance

- Leaflet remains isolated in its own vendor chunk.
- Heavy/secondary visualization code is lazy-loaded.
- Offscreen province rows use `content-visibility`.
- Timers, event listeners, map instances, and modal focus state must clean up on unmount.
