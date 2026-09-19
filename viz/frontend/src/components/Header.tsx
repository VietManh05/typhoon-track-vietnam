import React, { useState, useEffect } from 'react';
import {
  CloudLightning,
  Clock,
  Globe2,
  Moon,
  Sun,
  Bell,
  Activity,
  RefreshCw,
} from 'lucide-react';
import { Language, translations } from '../i18n';

interface HeaderProps {
  lang: Language;
  onToggleLang: () => void;
  isDark: boolean;
  onToggleTheme: () => void;
  isLive: boolean;
  onRefresh: () => void;
  onOpenAlerts: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  lang,
  onToggleLang,
  isDark,
  onToggleTheme,
  isLive,
  onRefresh,
  onOpenAlerts,
}) => {
  const [time, setTime] = useState<Date>(new Date());
  const t = translations[lang];

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formatUtc = (d: Date) => {
    return d.toISOString().replace('T', ' ').substring(0, 19) + ' UTC';
  };

  const formatVn = (d: Date) => {
    return (
      d.toLocaleString('vi-VN', {
        timeZone: 'Asia/Ho_Chi_Minh',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      }) + ' (GMT+7)'
    );
  };

  return (
    <header role="banner" className="w-full bg-slate-900/95 backdrop-blur-md border-b border-cyan-500/20 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-lg z-50">
      {/* Brand Logo & Title */}
      <div className="flex items-center gap-3">
        <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-700 shadow-md shadow-cyan-500/20 border border-cyan-400/30">
          <CloudLightning className="w-6 h-6 text-cyan-200 animate-pulse" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-lg md:text-xl font-bold tracking-tight text-white font-display flex items-center gap-2">
              TYPHOON<span className="text-cyan-400">VN</span>
              <span className="text-xs px-2 py-0.5 rounded-full font-mono font-medium tracking-normal bg-cyan-950/80 text-cyan-300 border border-cyan-700/50">
                v1.0-STAGING
              </span>
            </h1>
          </div>
          <p className="text-xs text-slate-400 font-medium hidden sm:block">
            {t.app_title}
          </p>
        </div>
      </div>

      {/* Clocks & Connection Badge */}
      <div className="hidden lg:flex items-center gap-4 bg-slate-950/70 border border-slate-800 rounded-lg px-3 py-1.5 text-xs font-mono" aria-label={t.time_utc}>
        <div className="flex items-center gap-1.5 text-slate-300">
          <Clock className="w-3.5 h-3.5 text-cyan-400" aria-hidden="true" />
          <time>{formatUtc(time)}</time>
        </div>
        <span className="text-slate-600" aria-hidden="true">|</span>
        <div className="text-cyan-300 font-semibold">
          <time>{formatVn(time)}</time>
        </div>
      </div>

      {/* Action Controls */}
      <nav className="flex items-center gap-2" aria-label={lang === 'vi' ? 'Điều khiển hệ thống' : 'System controls'}>
        {/* Live / Mock Status Badge */}
        <div
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border ${
            isLive
              ? 'bg-emerald-950/70 text-emerald-400 border-emerald-500/40 shadow-sm shadow-emerald-500/20'
              : 'bg-amber-950/70 text-amber-300 border-amber-500/40'
          }`}
          role="status"
          aria-live="polite"
          title={isLive ? t.system_status_live : t.system_status_mock}
        >
          <Activity className={`w-3.5 h-3.5 ${isLive ? 'animate-pulse text-emerald-400' : 'text-amber-400'}`} aria-hidden="true" />
          <span className="hidden sm:inline">
            {isLive ? t.system_status_live : t.system_status_mock}
          </span>
        </div>

        {/* Subscribe Alerts Button */}
        <button
          onClick={onOpenAlerts}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-medium bg-slate-800 hover:bg-slate-750 text-slate-200 border border-slate-700 transition hover:border-cyan-500/40 focus-ring"
          aria-label={t.subscribe_alerts}
        >
          <Bell className="w-3.5 h-3.5 text-amber-400" aria-hidden="true" />
          <span className="hidden md:inline">{t.subscribe_alerts}</span>
        </button>

        {/* Refresh */}
        <button
          onClick={onRefresh}
          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition active:scale-95 focus-ring touch-target"
          aria-label={t.aria_refresh}
        >
          <RefreshCw className="w-4 h-4" aria-hidden="true" />
        </button>

        {/* Language Switcher */}
        <button
          onClick={onToggleLang}
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-cyan-300 border border-slate-700 transition focus-ring"
          aria-label={t.aria_lang_toggle}
        >
          <Globe2 className="w-3.5 h-3.5" aria-hidden="true" />
          <span>{lang === 'vi' ? '🇻🇳 VI' : '🇬🇧 EN'}</span>
        </button>

        {/* Theme Switcher */}
        <button
          onClick={onToggleTheme}
          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition focus-ring touch-target"
          aria-label={t.aria_theme_toggle}
        >
          {isDark ? <Sun className="w-4 h-4 text-amber-300" aria-hidden="true" /> : <Moon className="w-4 h-4 text-slate-600" aria-hidden="true" />}
        </button>
      </nav>
    </header>
  );
};
