import React, { useState } from 'react';
import { Language, translations } from '../../i18n';
import { ChevronDown, ChevronUp, Layers } from 'lucide-react';

interface MapLegendProps {
  lang: Language;
}

export const MapLegend: React.FC<MapLegendProps> = ({ lang }) => {
  const [collapsed, setCollapsed] = useState(false);
  const t = translations[lang];

  const intensityItems: Array<{ key: string; color: string; label: string }> = [
    { key: 'TD', color: 'bg-cyan-400', label: t.categories['TD'] || 'TD' },
    { key: 'TS', color: 'bg-emerald-400', label: t.categories['TS'] || 'TS' },
    { key: 'STS', color: 'bg-amber-400', label: t.categories['STS'] || 'STS' },
    { key: 'TY', color: 'bg-orange-500', label: t.categories['TY'] || 'TY' },
    { key: 'STY', color: 'bg-rose-500', label: t.categories['STY'] || 'STY' },
    { key: 'SUPERTY', color: 'bg-purple-500', label: t.categories['SUPERTY'] || 'SUPERTY' },
  ];

  return (
    <div
      className="absolute bottom-6 right-6 z-[1000] max-w-xs w-full bg-slate-900/90 backdrop-blur-md border border-slate-700/60 rounded-xl shadow-2xl p-3 text-xs font-mono text-slate-200"
      role="region"
      aria-label={t.legend_title}
    >
      <button
        onClick={() => setCollapsed(!collapsed)}
        className="w-full flex items-center justify-between cursor-pointer border-b border-slate-800 pb-2 mb-2 font-display select-none focus-ring rounded"
        aria-expanded={!collapsed}
      >
        <div className="flex items-center gap-1.5 font-bold text-slate-100 text-xs">
          <Layers className="w-3.5 h-3.5 text-cyan-400" aria-hidden="true" />
          <span>{t.legend_title}</span>
        </div>
        {collapsed ? <ChevronUp className="w-4 h-4 text-slate-400" aria-hidden="true" /> : <ChevronDown className="w-4 h-4 text-slate-400" aria-hidden="true" />}
      </button>

      {!collapsed && (
        <div className="flex flex-col gap-2.5 animate-fade-in">
          {/* Tracks & Cone */}
          <div className="flex flex-col gap-1.5">
            <div className="flex items-center gap-2">
              <div className="w-4 h-0.5 bg-emerald-400 border border-emerald-400" aria-hidden="true" />
              <div className="w-2 h-2 rounded-full bg-emerald-400" aria-hidden="true" />
              <span className="text-[11px] text-slate-300">{t.legend_actual}</span>
            </div>

            <div className="flex items-center gap-2">
              <div className="w-4 h-0.5 border-t-2 border-dashed border-amber-400" aria-hidden="true" />
              <div className="w-2 h-2 rounded-full bg-amber-400" aria-hidden="true" />
              <span className="text-[11px] text-slate-300">{t.legend_forecast}</span>
            </div>

            <div className="flex items-center gap-2">
              <div className="w-4 h-3 rounded bg-cyan-500/20 border border-cyan-400/60" aria-hidden="true" />
              <span className="text-[11px] text-slate-300">{t.legend_cone}</span>
            </div>

            <div className="flex items-center gap-2">
              <div className="w-4 h-0.5 border-t-2 border-dotted border-purple-400" aria-hidden="true" />
              <div className="w-2 h-2 rounded-full bg-purple-400" aria-hidden="true" />
              <span className="text-[11px] text-slate-300">{t.legend_compare}</span>
            </div>
          </div>

          {/* Intensity Colors */}
          <div className="pt-2 border-t border-slate-800 flex flex-col gap-1">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              {t.legend_intensity_scale}
            </span>
            <div className="grid grid-cols-2 gap-x-2 gap-y-1 text-[10px]">
              {intensityItems.map((item) => (
                <div key={item.key} className="flex items-center gap-1.5">
                  <span className={`w-2.5 h-2.5 rounded-full ${item.color}`} aria-hidden="true" />
                  <span>{item.label}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Vietnam Sovereignty Note */}
          <div className="pt-1.5 border-t border-slate-800 text-[10px] text-cyan-300 flex items-center gap-1">
            <span aria-hidden="true">🇻🇳</span>
            <span>{t.legend_vietnam}</span>
          </div>
        </div>
      )}
    </div>
  );
};
