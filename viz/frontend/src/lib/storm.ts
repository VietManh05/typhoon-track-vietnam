import { IntensityClass, ProvinceImpact } from '../types';
import { TranslationStrings } from '../i18n';

/**
 * Domain mappings for the storm intensity scale (WMO / NCHMF) and the province
 * risk model. Keeping them here removes colour/copy duplication from
 * components and guarantees one visual language for every badge in the UI.
 *
 * Tailwind needs literal class strings to detect them at build time — that is
 * why these maps are plain objects and not computed at runtime.
 */

export interface TokenClasses {
  /** hex value for canvas/map consumers (Leaflet, Recharts) */
  hex: string;
  text: string;
  bg: string;
  border: string;
  dot: string;
}

const NEUTRAL: TokenClasses = {
  hex: '#94a3b8',
  text: 'text-fg-muted',
  bg: 'bg-surface-3',
  border: 'border-line-strong',
  dot: 'bg-fg-faint',
};

export const INTENSITY_TOKENS: Record<string, TokenClasses> = {
  TD: { hex: '#22d3ee', text: 'text-storm-td', bg: 'bg-storm-td/10', border: 'border-storm-td/40', dot: 'bg-storm-td' },
  TS: { hex: '#10b981', text: 'text-storm-ts', bg: 'bg-storm-ts/10', border: 'border-storm-ts/40', dot: 'bg-storm-ts' },
  STS: { hex: '#f59e0b', text: 'text-storm-sts', bg: 'bg-storm-sts/10', border: 'border-storm-sts/40', dot: 'bg-storm-sts' },
  TY: { hex: '#fb923c', text: 'text-storm-ty', bg: 'bg-storm-ty/10', border: 'border-storm-ty/40', dot: 'bg-storm-ty' },
  STY: { hex: '#f43f5e', text: 'text-storm-sty', bg: 'bg-storm-sty/10', border: 'border-storm-sty/40', dot: 'bg-storm-sty' },
  SUPERTY: { hex: '#8b5cf6', text: 'text-storm-superty', bg: 'bg-storm-superty/10', border: 'border-storm-superty/40', dot: 'bg-storm-superty' },
  UNK: NEUTRAL,
};

export function getIntensityToken(intensity?: string | null): TokenClasses {
  if (!intensity) return NEUTRAL;
  return INTENSITY_TOKENS[intensity] ?? INTENSITY_TOKENS[String(intensity).toUpperCase()] ?? NEUTRAL;
}

/* -------------------------------------------------------------------------- */
/* Province risk model                                                         */
/* -------------------------------------------------------------------------- */

export type RiskLevel = 'severe' | 'veryHigh' | 'high' | 'moderate' | 'low';

/** Distance bands (km) — identical to the ones used by the impact API. */
export const IMPACT_DISTANCE_BANDS = {
  critical: 60,
  high: 150,
  moderate: 300,
  low: 500,
} as const;

export const RISK_ORDER: RiskLevel[] = ['severe', 'veryHigh', 'high', 'moderate', 'low'];

const RISK_FROM_IMPACT: Record<ProvinceImpact['impact_level'], RiskLevel> = {
  critical: 'severe',
  high: 'veryHigh',
  moderate: 'high',
  low: 'moderate',
  none: 'low',
};

export function getRiskLevel(impact: ProvinceImpact['impact_level']): RiskLevel {
  return RISK_FROM_IMPACT[impact] ?? 'low';
}

export const RISK_TOKENS: Record<RiskLevel, TokenClasses> = {
  severe: { hex: '#8b5cf6', text: 'text-secondary', bg: 'bg-secondary/10', border: 'border-secondary/45', dot: 'bg-secondary' },
  veryHigh: { hex: '#f43f5e', text: 'text-danger', bg: 'bg-danger/10', border: 'border-danger/45', dot: 'bg-danger' },
  high: { hex: '#f59e0b', text: 'text-warning', bg: 'bg-warning/10', border: 'border-warning/45', dot: 'bg-warning' },
  moderate: { hex: '#22d3ee', text: 'text-primary', bg: 'bg-primary/10', border: 'border-primary/45', dot: 'bg-primary' },
  low: { hex: '#10b981', text: 'text-success', bg: 'bg-success/10', border: 'border-success/45', dot: 'bg-success' },
};

/** i18n key suffix for each risk level, e.g. `risk_severe`. */
export const RISK_LABEL_KEYS: Record<RiskLevel, keyof TranslationStrings> = {
  severe: 'risk_severe',
  veryHigh: 'risk_very_high',
  high: 'risk_high',
  moderate: 'risk_moderate',
  low: 'risk_low',
};
