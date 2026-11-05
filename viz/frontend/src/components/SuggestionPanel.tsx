import React from 'react';
import { History } from 'lucide-react';
import { Suggestion } from '../types';
import { Language, translations } from '../i18n';

interface SuggestionPanelProps {
  suggestion: Suggestion;
  lang: Language;
}

/** Lists the historical analog storms behind the k-NN track suggestion. */
export const SuggestionPanel: React.FC<SuggestionPanelProps> = ({ suggestion, lang }) => {
  const t = translations[lang];
  return (
    <div className="glass-panel p-4 flex flex-col gap-3" role="region" aria-label={t.suggestion_title}>
      <div className="flex items-center gap-2 text-sm font-bold text-purple-300">
        <History className="w-4 h-4" aria-hidden="true" />
        {t.suggestion_title}
      </div>
      <p className="text-xs text-slate-300">{t.suggestion_intro}</p>
      <ol className="flex flex-col gap-1.5">
        {suggestion.analogs.map((analog) => (
          <li
            key={analog.storm_id}
            className="flex items-center justify-between rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-1.5 text-xs font-mono"
          >
            <span className="text-slate-400">
              {t.suggestion_rank} {analog.rank}
            </span>
            <span className="font-bold text-purple-200">
              {analog.name} ({analog.year})
            </span>
            <span className="text-slate-500">{analog.storm_id}</span>
          </li>
        ))}
      </ol>
      <p className="text-[11px] text-slate-400 italic">
        {t.suggestion_caveat} <span className="not-italic text-slate-500">{suggestion.method}</span>
      </p>
    </div>
  );
};
