# Typhoon VN — Weather Intelligence Design System

This file documents the frontend visual contract. Runtime values live in `src/index.css`; Tailwind aliases live in `tailwind.config.js`.

## Direction

- Product: tropical-cyclone track suggestion and decision support for Vietnam, used by the general public, including older people with little app experience.
- Visual language: bright daylight weather app (white cards on a soft sky background, one clear-sky blue accent), modelled on mainstream weather apps; map-first hierarchy.
- Principles: readability before decoration, plain Vietnamese wording instead of codes, status never conveyed by colour alone, big touch targets, restrained motion.
- Avoid: navy/neon "command centre" styling, glowing effects, small letter-spaced capitals, technical codes (STS, UNK, storm IDs) as primary labels.

## Color tokens

Runtime values are RGB triplets in `src/index.css`. Daylight (`html.light`) is the default; night is opt-in.

| Semantic role | Daylight (default) | Night (opt-in) |
| --- | --- | --- |
| Background | `#EEF5FC` (sky gradient at top) | `#14161A` |
| Surface 1 / 2 / 3 | `#FFFFFF` / `#F6F9FD` / `#E2ECF7` | `#1E2126` / `#282C32` / `#343940` |
| Primary (clear-sky blue) | `#0063CC` | `#6EB4FF` |
| Success / Warning / Danger | `#15803D` / `#B45309` / `#C81E1E` | `#4ADE80` / `#FBBF24` / `#FF7878` |
| Text primary / secondary / muted | `#111827` / `#374151` / `#4B5563` | `#F6F7F9` / `#CED4DC` / `#B0B8C4` |

All daylight text colours keep at least 7:1 contrast on white (WCAG AAA). On the night accent, selected controls use dark text.

Storm classes use `--c-storm-*` tokens per theme (TD cyan-blue, TS green, STS amber, TY orange, STY red, SUPERTY violet); map lines use mid-tone hex values readable on both basemaps. Labels show the Vietnamese class name ("Bão mạnh"), never the code alone.

## Typography

- UI: self-hosted Be Vietnam Pro; data: JetBrains Mono, tabular figures.
- Minimum text 13px; secondary 14–15px; body 17px; primary values 26–56px.
- Sentence case everywhere; no uppercase letter-spaced labels.
- Easy-read overrides live in `src/styles/easy-read.css`, loaded last.

## Shape, spacing, elevation

- Spacing follows a 4/8px rhythm.
- Badge radius 6px, control radius 9px, card radius 12px, panel radius 14px.
- Panels use a 1px low-opacity border and one restrained shadow level.
- Touch targets are at least 48px (map controls, tabs, storm chips, timeline buttons).

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
