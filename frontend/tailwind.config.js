/** @type {import('tailwindcss').Config} */

/*
 * TYPHOON VN — Design tokens.
 *
 * Every colour resolves to a CSS custom property declared in `src/index.css`
 * (`:root`), so the whole theme can be retuned from a single place while
 * keeping full Tailwind opacity-modifier support (`bg-primary/10`).
 */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      /* ===== Colour system (dark weather-intelligence palette) ===== */
      colors: {
        /* Page background — deepest layer */
        page: 'rgb(var(--c-bg) / <alpha-value>)',

        /* Surface elevation scale */
        surface: {
          DEFAULT: 'rgb(var(--c-surface-1) / <alpha-value>)',
          2: 'rgb(var(--c-surface-2) / <alpha-value>)',
          3: 'rgb(var(--c-surface-3) / <alpha-value>)',
        },

        /* Hairline borders — baked alpha, use `border-line` directly */
        line: {
          DEFAULT: 'rgb(var(--c-line) / 0.12)',
          strong: 'rgb(var(--c-line) / 0.22)',
          faint: 'rgb(var(--c-line) / 0.07)',
        },

        /* Text ramp */
        fg: {
          DEFAULT: 'rgb(var(--c-fg) / <alpha-value>)',
          muted: 'rgb(var(--c-fg-2) / <alpha-value>)',
          faint: 'rgb(var(--c-fg-3) / <alpha-value>)',
        },

        /* Brand + semantic accents */
        primary: {
          DEFAULT: 'rgb(var(--c-primary) / <alpha-value>)',
          deep: 'rgb(var(--c-primary-deep) / <alpha-value>)',
        },
        secondary: 'rgb(var(--c-secondary) / <alpha-value>)',
        success: 'rgb(var(--c-success) / <alpha-value>)',
        warning: 'rgb(var(--c-warning) / <alpha-value>)',
        danger: 'rgb(var(--c-danger) / <alpha-value>)',

        /* Domain scale — WMO / NCHMF storm intensity classes.
           Mapped onto the accent palette so the UI never invents new hues. */
        storm: {
          td: 'rgb(var(--c-storm-td) / <alpha-value>)', // Tropical Depression
          ts: 'rgb(var(--c-storm-ts) / <alpha-value>)', // Tropical Storm
          sts: 'rgb(var(--c-storm-sts) / <alpha-value>)', // Severe Tropical Storm
          ty: 'rgb(var(--c-storm-ty) / <alpha-value>)', // Typhoon
          sty: 'rgb(var(--c-storm-sty) / <alpha-value>)', // Severe Typhoon
          superty: 'rgb(var(--c-storm-superty) / <alpha-value>)', // Super Typhoon
        },
      },

      /* ===== Typography ===== */
      fontFamily: {
        sans: ['"Be Vietnam Pro"', 'Inter', 'system-ui', '-apple-system', 'Segoe UI', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Consolas', 'monospace'],
      },
      fontSize: {
        // Larger floor than Tailwind defaults so older readers never see < 13px text.
        '2xs': ['0.8125rem', { lineHeight: '1.15rem', letterSpacing: '0.01em' }], // 13px
        xs: ['0.875rem', { lineHeight: '1.3rem' }], // 14px
        sm: ['0.9375rem', { lineHeight: '1.45rem' }], // 15px
        base: ['1.0625rem', { lineHeight: '1.65rem' }], // 17px
        metric: ['1.75rem', { lineHeight: '1.15', letterSpacing: '-0.02em' }], // 28px — major values
        hero: ['2rem', { lineHeight: '1.1', letterSpacing: '-0.02em' }], // 32px
      },

      /* ===== Radius (card 10–14px, control 8–10px, badge 6px) ===== */
      borderRadius: {
        badge: '6px',
        control: '9px',
        card: '12px',
        panel: '14px',
      },

      /* ===== Elevation — restrained, never glowing walls ===== */
      boxShadow: {
        panel: '0 1px 2px rgba(2, 6, 23, 0.45)',
        raised: '0 10px 30px -18px rgba(2, 6, 23, 0.9)',
        overlay: '0 18px 44px -20px rgba(2, 6, 23, 0.95)',
        'ring-primary': '0 0 0 1px rgba(34, 211, 238, 0.35)',
      },

      /* ===== Z-index ===== */
      zIndex: {
        map: '400',
        mapOverlay: '500',
        header: '600',
        dropdown: '700',
        modal: '900',
        toast: '1000',
      },

      /* ===== Motion — 150–250ms micro-interactions ===== */
      transitionDuration: {
        fast: '150ms',
        base: '200ms',
        slow: '250ms',
      },
      keyframes: {
        'pulse-ring': {
          '0%': { transform: 'scale(0.78)', opacity: '0.5' },
          '70%': { transform: 'scale(1.85)', opacity: '0' },
          '100%': { transform: 'scale(1.85)', opacity: '0' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-160% 0' },
          '100%': { backgroundPosition: '260% 0' },
        },
        'fade-in-up': {
          from: { opacity: '0', transform: 'translateY(6px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'slide-down': {
          from: { opacity: '0', transform: 'translateY(-6px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'pulse-ring': 'pulse-ring 2.4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 1.6s ease-in-out infinite',
        'fade-in-up': 'fade-in-up 0.24s ease-out both',
        'fade-in': 'fade-in 0.18s ease-out both',
        'slide-down': 'slide-down 0.18s ease-out both',
      },
    },
  },
  plugins: [],
};
