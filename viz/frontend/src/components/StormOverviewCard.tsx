import React from 'react';
import { ActiveTyphoonItem, Fix, ForecastResponse } from '../types';
import { Language, TranslationStrings, translations } from '../i18n';
import {
  Wind,
  Gauge,
  Navigation,
  Crosshair,
  ShieldAlert,
  Info,
  Layers,
} from 'lucide-react';

interface StormOverviewCardProps {
  storm: ActiveTyphoonItem;
  currentFix: Fix;
  forecast: ForecastResponse | null;
  lang: Language;
}

const getCategoryColor = (cat: string) => {
  switch (cat) {
    case 'SUPERTY':
      return 'text-purple-400 border-purple-500/40 bg-purple-950/40';
    case 'STY':
      return 'text-rose-400 border-rose-500/40 bg-rose-950/40';
    case 'TY':
      return 'text-orange-400 border-orange-500/40 bg-orange-950/40';
    case 'STS':
      return 'text-amber-400 border-amber-500/40 bg-amber-950/40';
    case 'TS':
      return 'text-emerald-400 border-emerald-500/40 bg-emerald-950/40';
    default:
      return 'text-cyan-400 border-cyan-500/40 bg-cyan-950/40';
  }
};

/** Get compass direction string from bearing degrees using i18n keys */
const getBearingCompass = (deg: number = 0, t: TranslationStrings): string => {
  const keys: Array<keyof TranslationStrings> = [
    'bearing_N', 'bearing_NNE', 'bearing_NE', 'bearing_ENE',
    'bearing_E', 'bearing_ESE', 'bearing_SE', 'bearing_SSE',
    'bearing_S', 'bearing_SSW', 'bearing_SW', 'bearing_WSW',
    'bearing_W', 'bearing_WNW', 'bearing_NW', 'bearing_NNW',
  ];
  const idx = Math.round(deg / 22.5) % 16;
  return t[keys[idx]] as string;
};

/** Get pressure description using i18n */
const getPressureDesc = (hpa: number | null, t: TranslationStrings): string => {
  if (!hpa) return '';
  return hpa < 980 ? t.pressure_deep : t.pressure_normal;
};

export const StormOverviewCard: React.FC<StormOverviewCardProps> = ({
  storm,
  currentFix,
  forecast,
  lang,
}) => {
  const t = translations[lang];
  const cat = currentFix.intensity || 'TY';
  const catLabel = t.categories[cat] || cat;

  const windKmh = currentFix.wind_kmh || (currentFix.wind_ms ? Math.round(currentFix.wind_ms * 3.6) : null);
  const beaufort = currentFix.beaufort_level || (windKmh ? (windKmh >= 184 ? 16 : windKmh >= 150 ? 14 : windKmh >= 118 ? 12 : 10) : 12);
  const bearing = currentFix.bearing_deg ?? 285;
  const speedKmh = currentFix.speed_kmh ?? 20;

  return (
    <div className="glass-panel p-4 flex flex-col gap-4 animate-fade-in-up" role="region" aria-label={t.storm_overview}>
      {/* Header with Name & Category */}
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl md:text-2xl font-bold font-display text-white tracking-tight">
              {lang === 'vi' && storm.name_vi ? storm.name_vi : storm.name}
            </h2>
            <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
              {storm.id}
            </span>
          </div>
          <p className="text-xs text-slate-400 font-mono mt-0.5">
            {t.last_observation}: {new Date(currentFix.timestamp).toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US')}
          </p>
        </div>

        {/* Intensity Badge */}
        <div className={`px-3 py-1.5 rounded-lg border font-bold text-xs flex items-center gap-2 ${getCategoryColor(cat)}`}>
          <ShieldAlert className="w-4 h-4 shrink-0" aria-hidden="true" />
          <span>{catLabel}</span>
        </div>
      </div>

      {/* Primary Metrics Grid (4 columns) */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {/* Wind Speed */}
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
            <Wind className="w-3.5 h-3.5 text-cyan-400" aria-hidden="true" />
            <span>{t.wind_speed}</span>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-cyan-300">
              {windKmh ? `${windKmh} km/h` : 'N/A'}
            </div>
            <div className="text-[11px] text-slate-400 font-mono">
              {currentFix.wind_ms ? `${currentFix.wind_ms} m/s` : ''} · {t.beaufort_prefix} {beaufort}
            </div>
          </div>
        </div>

        {/* Central Pressure */}
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
            <Gauge className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
            <span>{t.central_pressure}</span>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-amber-300">
              {currentFix.pressure_hpa ? `${currentFix.pressure_hpa} hPa` : 'N/A'}
            </div>
            <div className="text-[11px] text-slate-400 font-mono">
              {getPressureDesc(currentFix.pressure_hpa, t)}
            </div>
          </div>
        </div>

        {/* Center Position */}
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
            <Crosshair className="w-3.5 h-3.5 text-emerald-400" aria-hidden="true" />
            <span>{t.position}</span>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-emerald-300">
              {currentFix.lat.toFixed(1)}°{lang === 'vi' ? 'B' : 'N'} · {currentFix.lon.toFixed(1)}°{lang === 'vi' ? 'Đ' : 'E'}
            </div>
            <div className="text-[11px] text-slate-400 font-mono">
              {t.sea_region}
            </div>
          </div>
        </div>

        {/* Movement Vector */}
        <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 flex flex-col justify-between">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium">
            <Navigation className="w-3.5 h-3.5 text-rose-400" style={{ transform: `rotate(${bearing}deg)` }} aria-hidden="true" />
            <span>{t.movement}</span>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-rose-300">
              {speedKmh} km/h
            </div>
            <div className="text-[11px] text-slate-400 font-mono truncate">
              {getBearingCompass(bearing, t)} ({bearing}°)
            </div>
          </div>
        </div>
      </div>

      {/* Warnings & Model Metadata */}
      {forecast && (
        <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 text-xs flex flex-col gap-2">
          {forecast.warnings && forecast.warnings.length > 0 && (
            <div className="flex items-start gap-2 text-amber-300" role="alert">
              <ShieldAlert className="w-4 h-4 shrink-0 text-amber-400 mt-0.5" aria-hidden="true" />
              <div className="flex flex-col gap-1">
                {forecast.warnings.map((w, idx) => (
                  <span key={idx} className="font-medium">{w}</span>
                ))}
              </div>
            </div>
          )}

          <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-850 text-slate-400 text-[11px] font-mono">
            <div className="flex items-center gap-1">
              <Info className="w-3 h-3 text-cyan-400" aria-hidden="true" />
              <span>{t.model_version}: <strong className="text-slate-200">{forecast.model_version}</strong></span>
            </div>
            <div className="flex items-center gap-1">
              <Layers className="w-3 h-3 text-cyan-400" aria-hidden="true" />
              <span>{t.data_source}: <strong className="text-slate-200">{forecast.sources.join(', ')}</strong></span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
