import { Language } from '../i18n';

/**
 * Formatting helpers for meteorological values.
 *
 * Rules enforced across the whole dashboard:
 *  - a value and its unit are always separated by a non-breaking space
 *  - numbers use tabular figures (see `.num` utility) so columns align
 *  - dates follow the active language, times the requested time zone
 */

export const NBSP = '\u00A0';

/** Wind speed in km/h from either SI (m/s) or already converted values. */
export function windKmh(windMs?: number | null, windKmhValue?: number | null): number | null {
  if (typeof windKmhValue === 'number' && Number.isFinite(windKmhValue)) return Math.round(windKmhValue);
  if (typeof windMs === 'number' && Number.isFinite(windMs)) return Math.round(windMs * 3.6);
  return null;
}

export function windKnots(windMs?: number | null): number | null {
  if (typeof windMs !== 'number' || !Number.isFinite(windMs)) return null;
  return Math.round(windMs * 1.94384);
}

/** Beaufort level for a km/h wind speed (WMO scale, 0–17). */
export function beaufortFromKmh(kmh?: number | null): number {
  if (typeof kmh !== 'number' || !Number.isFinite(kmh)) return 0;
  const scale = [1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117, 134, 149, 166, 183, 201, 220];
  const index = scale.findIndex((upper) => kmh < upper);
  return index === -1 ? 17 : index;
}

export function formatCoordinate(value: number, axis: 'lat' | 'lon', lang: Language, digits = 1): string {
  const hemisphere = axis === 'lat' ? (lang === 'vi' ? 'B' : 'N') : lang === 'vi' ? 'Đ' : 'E';
  return `${value.toFixed(digits)}°${hemisphere}`;
}

export function formatLatLon(lat: number, lon: number, lang: Language, digits = 1): string {
  return `${formatCoordinate(lat, 'lat', lang, digits)} ${formatCoordinate(lon, 'lon', lang, digits)}`;
}

/** Minutes elapsed between `iso` and `now` (never negative). */
export function minutesSince(iso: string, now: Date = new Date()): number {
  const then = new Date(iso).getTime();
  if (!Number.isFinite(then)) return 0;
  return Math.max(0, Math.round((now.getTime() - then) / 60000));
}

export function formatDateTime(iso: string, lang: Language, timeZone = 'Asia/Ho_Chi_Minh'): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US', {
    timeZone,
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  });
}

export function formatShortDateTime(iso: string, lang: Language, timeZone = 'Asia/Ho_Chi_Minh'): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '—';
  return date.toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US', {
    timeZone,
    hour: '2-digit',
    minute: '2-digit',
    day: '2-digit',
    month: '2-digit',
  });
}

/** `HH:mm:ss dd/MM/yyyy` for a live clock in the requested time zone. */
export function formatClock(date: Date, timeZone: string, lang: Language): string {
  return date.toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US', {
    timeZone,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour12: false,
  });
}

/** Compact UTC stamp: `14:05:09 19/09/2026 UTC`. */
export function formatUtcStamp(date: Date): string {
  const iso = date.toISOString();
  return `${iso.slice(11, 19)} ${iso.slice(8, 10)}/${iso.slice(5, 7)}/${iso.slice(0, 4)} UTC`;
}

/** Distance in km with locale separators. */
export function formatKm(km?: number | null, digits = 0): string {
  if (typeof km !== 'number' || !Number.isFinite(km)) return '—';
  return km.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
}

export function formatHours(hours?: number | null): string {
  if (typeof hours !== 'number' || !Number.isFinite(hours)) return '—';
  return `+${hours}${NBSP}h`;
}
