import React from 'react';
import { ForecastResponse } from '../types';
import { Language, translations } from '../i18n';
import { Calendar } from 'lucide-react';

interface ForecastTableProps {
  forecast: ForecastResponse | null;
  lang: Language;
}

const getCategoryBadgeColor = (cat: string): string => {
  switch (cat) {
    case 'SUPERTY': return 'bg-purple-900/60 text-purple-300 border-purple-700';
    case 'STY': return 'bg-rose-900/60 text-rose-300 border-rose-700';
    case 'TY': return 'bg-orange-900/60 text-orange-300 border-orange-700';
    case 'STS': return 'bg-amber-900/60 text-amber-300 border-amber-700';
    case 'TS': return 'bg-emerald-900/60 text-emerald-300 border-emerald-700';
    case 'TD': return 'bg-cyan-900/60 text-cyan-300 border-cyan-700';
    default: return 'bg-slate-800 text-slate-300 border-slate-700';
  }
};

export const ForecastTable: React.FC<ForecastTableProps> = ({ forecast, lang }) => {
  const t = translations[lang];

  if (!forecast || !forecast.points || forecast.points.length === 0) {
    return null;
  }

  return (
    <div className="glass-panel p-4 flex flex-col gap-3 animate-fade-in-up" role="region" aria-label={t.forecast_table}>
      <div className="flex items-center justify-between border-b border-slate-800 pb-2">
        <div className="flex items-center gap-2">
          <Calendar className="w-4 h-4 text-cyan-400" aria-hidden="true" />
          <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider font-display">
            {t.forecast_table}
          </h3>
        </div>
        <span className="text-[11px] font-mono text-cyan-400/80">
          Issue: {new Date(forecast.issue_time).toLocaleTimeString(lang === 'vi' ? 'vi-VN' : 'en-US')}
        </span>
      </div>

      {/* Horizontal scroll indicator for mobile */}
      <div className="overflow-x-auto -mx-1 px-1">
        <table className="w-full text-left text-xs font-mono border-collapse" aria-label={t.aria_forecast_table}>
          <thead>
            <tr className="border-b border-slate-800 text-slate-400">
              <th className="py-2 px-2 font-medium" scope="col">{t.horizon}</th>
              <th className="py-2 px-2 font-medium" scope="col">{t.valid_time} (VN)</th>
              <th className="py-2 px-2 font-medium" scope="col">{t.coordinates}</th>
              <th className="py-2 px-2 font-medium" scope="col">{t.category}</th>
              <th className="py-2 px-2 font-medium" scope="col">{t.wind}</th>
              <th className="py-2 px-2 font-medium" scope="col">{t.cone_radius}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {forecast.points.map((p) => {
              const vnTime = new Date(p.valid_time).toLocaleString('vi-VN', {
                timeZone: 'Asia/Ho_Chi_Minh',
                hour: '2-digit',
                minute: '2-digit',
                day: '2-digit',
                month: '2-digit',
              });

              const catStr = String(p.intensity);

              return (
                <tr key={p.horizon_hours} className="hover:bg-slate-850/50 transition">
                  <td className="py-2 px-2 font-bold text-cyan-300">
                    +{p.horizon_hours}h
                  </td>
                  <td className="py-2 px-2 text-slate-300">
                    {vnTime}
                  </td>
                  <td className="py-2 px-2 text-slate-200">
                    {p.lat.toFixed(1)}°{lang === 'vi' ? 'B' : 'N'} · {p.lon.toFixed(1)}°{lang === 'vi' ? 'Đ' : 'E'}
                  </td>
                  <td className="py-2 px-2">
                    <span className={`px-1.5 py-0.5 rounded text-[10px] font-bold border ${getCategoryBadgeColor(catStr)}`}>
                      {catStr}
                    </span>
                  </td>
                  <td className="py-2 px-2 text-slate-300">
                    {p.wind_ms ? `${Math.round(p.wind_ms * 3.6)} km/h` : 'N/A'}
                  </td>
                  <td className="py-2 px-2 text-slate-400">
                    ±{p.radius_km} km
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <div className="text-[11px] text-slate-400 font-mono italic pt-1 border-t border-slate-850">
        * {forecast.uncertainty_method}
      </div>
    </div>
  );
};
