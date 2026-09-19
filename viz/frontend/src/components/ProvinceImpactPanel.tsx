import React, { useState, useMemo } from 'react';
import { ProvinceImpact } from '../types';
import { Language, translations } from '../i18n';
import { MapPin, Search, AlertCircle, ArrowRight } from 'lucide-react';

interface ProvinceImpactPanelProps {
  impacts: ProvinceImpact[];
  selectedProvinceId: string | null;
  onSelectProvince: (id: string) => void;
  lang: Language;
}

const getImpactBadge = (level: ProvinceImpact['impact_level'], lang: Language) => {
  const t = translations[lang];
  switch (level) {
    case 'critical':
      return {
        label: t.impact_critical,
        className: 'bg-purple-950/80 text-purple-300 border-purple-600/60 shadow-sm shadow-purple-500/20',
      };
    case 'high':
      return {
        label: t.impact_high,
        className: 'bg-rose-950/80 text-rose-300 border-rose-600/60 shadow-sm shadow-rose-500/20',
      };
    case 'moderate':
      return {
        label: t.impact_moderate,
        className: 'bg-amber-950/80 text-amber-300 border-amber-600/60',
      };
    case 'low':
      return {
        label: t.impact_low,
        className: 'bg-emerald-950/80 text-emerald-300 border-emerald-600/60',
      };
    default:
      return {
        label: t.impact_none,
        className: 'bg-slate-900/60 text-slate-400 border-slate-800',
      };
  }
};

export const ProvinceImpactPanel: React.FC<ProvinceImpactPanelProps> = ({
  impacts,
  selectedProvinceId,
  onSelectProvince,
  lang,
}) => {
  const [search, setSearch] = useState('');
  const t = translations[lang];

  const filteredProvinces = useMemo(() => {
    return impacts.filter((p) =>
      p.name.toLowerCase().includes(search.toLowerCase())
    );
  }, [impacts, search]);

  const selectedProvince = useMemo(() => {
    return impacts.find((p) => p.id === selectedProvinceId) || impacts[0];
  }, [impacts, selectedProvinceId]);

  return (
    <div className="glass-panel p-4 flex flex-col gap-3 animate-fade-in-up" role="region" aria-label={t.province_impact_title}>
      {/* Title */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-cyan-400" aria-hidden="true" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider font-display">
            {t.province_impact_title}
          </h3>
        </div>
      </div>

      {/* Search Input */}
      <div className="relative" role="search">
        <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" aria-hidden="true" />
        <input
          type="text"
          placeholder={t.select_province}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-slate-900/90 border border-slate-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition focus-ring"
          aria-label={t.select_province}
        />
      </div>

      {/* Selected Province Highlights */}
      {selectedProvince && (
        <div className="p-3 rounded-lg bg-slate-950/80 border border-slate-800 flex flex-col gap-2.5">
          <div className="flex items-center justify-between">
            <h4 className="text-base font-bold font-display text-white flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-rose-400" aria-hidden="true" />
              {selectedProvince.name}
            </h4>
            <span className="text-[11px] font-mono text-slate-400">
              {selectedProvince.centroid[0].toFixed(2)}°{lang === 'vi' ? 'B' : 'N'}, {selectedProvince.centroid[1].toFixed(2)}°{lang === 'vi' ? 'Đ' : 'E'}
            </span>
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs font-mono">
            <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
              <div className="text-[11px] text-slate-400">{t.distance_to_center}</div>
              <div className="text-base font-bold text-cyan-300 mt-0.5">
                {selectedProvince.current_distance_km} km
              </div>
            </div>

            <div className="p-2 rounded bg-slate-900/60 border border-slate-800">
              <div className="text-[11px] text-slate-400">{t.closest_forecast_dist}</div>
              <div className="text-base font-bold text-amber-300 mt-0.5">
                {selectedProvince.min_forecast_distance_km} km
              </div>
            </div>
          </div>

          {/* ETA & Impact Level */}
          <div className="flex flex-col gap-1.5 pt-1 border-t border-slate-850">
            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400 font-medium">{t.eta_label}:</span>
              <span className="font-mono font-bold text-slate-200">
                {selectedProvince.closest_horizon_hours === 0
                  ? t.eta_now
                  : `+${selectedProvince.closest_horizon_hours} ${t.eta_hours_suffix} (${new Date(
                      selectedProvince.closest_valid_time
                    ).toLocaleString(lang === 'vi' ? 'vi-VN' : 'en-US', {
                      hour: '2-digit',
                      minute: '2-digit',
                      day: '2-digit',
                      month: '2-digit',
                    })})`}
              </span>
            </div>

            <div className="flex items-center justify-between text-xs">
              <span className="text-slate-400 font-medium">{t.impact_level_label}:</span>
              <span
                className={`px-2 py-0.5 rounded text-[11px] font-bold border ${
                  getImpactBadge(selectedProvince.impact_level, lang).className
                }`}
              >
                {getImpactBadge(selectedProvince.impact_level, lang).label}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Top 5 Most Threatened Provinces Quick List */}
      <div className="flex flex-col gap-1.5 mt-1">
        <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider font-mono">
          {t.top_provinces_label}
        </span>
        <div className="flex flex-col gap-1" role="listbox" aria-label={t.top_provinces_label}>
          {impacts.slice(0, 5).map((p) => {
            const isSel = p.id === (selectedProvince?.id || '');
            return (
              <button
                key={p.id}
                onClick={() => onSelectProvince(p.id)}
                role="option"
                aria-selected={isSel}
                className={`flex items-center justify-between p-2 rounded-lg text-xs font-mono border transition focus-ring ${
                  isSel
                    ? 'bg-slate-800 text-cyan-300 border-cyan-500'
                    : 'bg-slate-900/50 text-slate-300 border-slate-800 hover:bg-slate-850'
                }`}
              >
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-slate-200">{p.name}</span>
                  {p.within_cone && (
                    <span className="text-[10px] px-1 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800">
                      {t.in_cone}
                    </span>
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-slate-400">{p.min_forecast_distance_km} km</span>
                  <ArrowRight className="w-3 h-3 text-slate-500" aria-hidden="true" />
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Caveat note */}
      <div className="flex items-start gap-1.5 text-[11px] text-slate-500 italic mt-1">
        <AlertCircle className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" aria-hidden="true" />
        <p>{t.impact_note}</p>
      </div>
    </div>
  );
};
