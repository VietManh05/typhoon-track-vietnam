import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { Language, translations } from '../i18n';

interface DisclaimerBannerProps {
  lang: Language;
}

export const DisclaimerBanner: React.FC<DisclaimerBannerProps> = ({ lang }) => {
  const t = translations[lang];

  return (
    <aside
      role="alert"
      aria-label={lang === 'vi' ? 'Cảnh báo pháp lý và khoa học' : 'Legal and scientific notice'}
      className="w-full bg-amber-950/80 border-y border-amber-500/30 px-4 py-1.5 flex items-center justify-center gap-2 text-xs text-amber-200 font-medium z-40 backdrop-blur-sm"
    >
      <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 animate-pulse" />
      <p className="text-center tracking-tight">
        {t.disclaimer}
      </p>
    </aside>
  );
};
