import React from 'react';
import { ActiveTyphoonItem } from '../types';
import { Language, translations } from '../i18n';
import { Compass, Wind } from 'lucide-react';

interface ActiveStormSelectorProps {
  storms: ActiveTyphoonItem[];
  selectedStormId: string;
  onSelectStorm: (id: string) => void;
  lang: Language;
}

const getCategoryBadgeClass = (category: string) => {
  switch (category) {
    case 'SUPERTY':
      return 'bg-purple-950 text-purple-300 border-purple-600/60 shadow-sm shadow-purple-500/20';
    case 'STY':
      return 'bg-rose-950 text-rose-300 border-rose-600/60 shadow-sm shadow-rose-500/20';
    case 'TY':
      return 'bg-orange-950 text-orange-300 border-orange-600/60';
    case 'STS':
      return 'bg-amber-950 text-amber-300 border-amber-600/60';
    case 'TS':
      return 'bg-emerald-950 text-emerald-300 border-emerald-600/60';
    default:
      return 'bg-cyan-950 text-cyan-300 border-cyan-600/60';
  }
};

export const ActiveStormSelector: React.FC<ActiveStormSelectorProps> = ({
  storms,
  selectedStormId,
  onSelectStorm,
  lang,
}) => {
  const t = translations[lang];

  return (
    <div className="w-full bg-slate-900/80 border-b border-slate-800 px-4 py-2 flex items-center gap-3 overflow-x-auto">
      <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider shrink-0">
        <Compass className="w-3.5 h-3.5 text-cyan-400" />
        <span>{t.active_storms}:</span>
      </div>

      <div className="flex items-center gap-2">
        {storms.map((storm) => {
          const isSelected = storm.id === selectedStormId;
          const cat = storm.latest.intensity;
          const catName = t.categories[cat] || cat;

          return (
            <button
              key={storm.id}
              onClick={() => onSelectStorm(storm.id)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs transition shrink-0 ${
                isSelected
                  ? 'bg-slate-800 text-white border-cyan-500 shadow-md shadow-cyan-500/10'
                  : 'bg-slate-900/60 text-slate-300 border-slate-800 hover:border-slate-700 hover:bg-slate-850'
              }`}
            >
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-slate-100 font-display">
                  {lang === 'vi' && storm.name_vi ? storm.name_vi : storm.name}
                </span>
                <span className="text-slate-400 text-[10px] font-mono">
                  ({storm.id})
                </span>
              </div>

              <span
                className={`px-1.5 py-0.5 rounded text-[10px] font-bold border font-mono ${getCategoryBadgeClass(
                  cat
                )}`}
              >
                {cat}
              </span>

              {storm.latest.wind_kmh && (
                <span className="flex items-center gap-1 text-[11px] font-mono text-cyan-300">
                  <Wind className="w-3 h-3 text-cyan-400" />
                  {storm.latest.wind_kmh} km/h
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
