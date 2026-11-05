import React, { useEffect, useRef, useState } from "react";
import {
    Bell,
    Clock3,
    FlaskConical,
    Globe2,
    MoreHorizontal,
    Moon,
    Radio,
    RefreshCw,
    Sun,
} from "lucide-react";
import { Language, translations } from "../i18n";
import { formatClock, formatUtcStamp } from "../lib/format";
import { AuthControl } from "./AuthControl";

interface HeaderProps {
    lang: Language;
    onToggleLang: () => void;
    isDark: boolean;
    onToggleTheme: () => void;
    isLive: boolean;
    isDemoMode: boolean;
    onToggleDemo: () => void | Promise<void>;
    onRefresh: () => void | Promise<void>;
    onOpenAlerts: () => void;
}

export const Header: React.FC<HeaderProps> = ({
    lang,
    onToggleLang,
    isDark,
    onToggleTheme,
    isLive,
    isDemoMode,
    onToggleDemo,
    onRefresh,
    onOpenAlerts,
}) => {
    const [time, setTime] = useState(() => new Date());
    const [isRefreshing, setIsRefreshing] = useState(false);
    const optionsRef = useRef<HTMLDetailsElement>(null);
    const t = translations[lang];

    useEffect(() => {
        const timer = window.setInterval(() => setTime(new Date()), 1000);
        return () => window.clearInterval(timer);
    }, []);

    const refresh = async () => {
        optionsRef.current?.removeAttribute("open");
        setIsRefreshing(true);
        try {
            await onRefresh();
        } finally {
            window.setTimeout(() => setIsRefreshing(false), 300);
        }
    };

    return (
        <header
            className="sticky top-0 z-header border-b border-line bg-page/95 px-3 backdrop-blur-md sm:px-4"
            role="banner"
        >
            <div className="mx-auto flex min-h-[64px] max-w-[1920px] items-center justify-between gap-3">
                <div className="flex min-w-0 items-center gap-3">
                    <img src="/favicon.svg" className="brand-mark h-10 w-10 shrink-0" alt="" aria-hidden="true" />
                    <div className="min-w-0">
                        <div className="flex items-center gap-2">
                            <h1 className="truncate text-base font-bold tracking-[0.04em] text-fg sm:text-lg">
                                TYPHOON <span className="text-primary">VN</span>
                            </h1>
                            <span className="hidden rounded-badge border border-line bg-surface-2 px-1.5 py-0.5 font-mono text-2xs font-medium text-fg-faint sm:inline">
                                WEATHER
                            </span>
                        </div>
                    </div>
                </div>

                <div
                    className="header-clocks hidden items-center gap-5 rounded-control border border-line bg-surface/70 px-3 py-1.5 xl:flex"
                    aria-label={`${t.time_utc}; ${t.time_vn}`}
                >
                    <div className="header-utc flex items-center gap-2">
                        <Clock3
                            className="h-3.5 w-3.5 text-fg-faint"
                            aria-hidden="true"
                        />
                        <div>
                            <div className="text-2xs font-semibold text-fg-faint">
                                UTC
                            </div>
                            <time className="clock-full font-mono text-xs text-fg-muted">
                                {formatUtcStamp(time)}
                            </time>
                            <time className="clock-short hidden font-mono text-xs text-fg-muted">
                                {time.toLocaleTimeString(lang === "vi" ? "vi-VN" : "en-GB", { timeZone: "UTC", hour: "2-digit", minute: "2-digit" })}
                            </time>
                        </div>
                    </div>
                    <div className="header-clock-divider h-7 w-px bg-line" aria-hidden="true" />
                    <div>
                        <div className="text-2xs font-semibold text-fg-faint">
                            Việt Nam
                        </div>
                        <time className="clock-full font-mono text-xs font-medium text-primary">
                            {formatClock(time, "Asia/Ho_Chi_Minh", lang)} GMT+7
                        </time>
                        <time className="clock-short hidden font-mono text-xs font-medium text-primary">
                            {time.toLocaleTimeString(lang === "vi" ? "vi-VN" : "en-GB", { timeZone: "Asia/Ho_Chi_Minh", hour: "2-digit", minute: "2-digit" })} GMT+7
                        </time>
                    </div>
                </div>

                <nav
                    className="header-actions flex shrink-0 items-center gap-2"
                    aria-label={
                        lang === "vi"
                            ? "Điều khiển hệ thống"
                            : "System controls"
                    }
                >
                    <div
                        className={`desktop-control hidden min-h-9 items-center gap-2 rounded-control border px-2.5 text-xs font-semibold sm:flex ${isLive ? "border-success/35 bg-success/10 text-success" : isDemoMode ? "border-warning/35 bg-warning/10 text-warning" : "border-line bg-surface-2 text-fg-muted"}`}
                        role="status"
                        aria-live="polite"
                        title={
                            isLive
                                ? (lang === "vi" ? "Nguồn dữ liệu bão trực tuyến; dịch vụ gửi cảnh báo được kiểm tra riêng" : "Live storm feed; alert delivery has a separate status")
                                : isDemoMode ? t.system_status_mock : (lang === "vi" ? "Chưa kết nối dữ liệu bão trực tuyến" : "Live storm data is unavailable")
                        }
                    >
                        <span
                            className={`h-1.5 w-1.5 rounded-full ${isLive ? "bg-success" : isDemoMode ? "bg-warning" : "bg-fg-muted"}`}
                            aria-hidden="true"
                        />
                        {isLive ? (lang === "vi" ? "Trực tiếp" : "Live") : isDemoMode ? (lang === "vi" ? "Xem lại bão cũ" : "Past storms") : (lang === "vi" ? "Chưa có dữ liệu" : "Offline")}
                    </div>
                    <button
                        type="button"
                        className="inline-flex min-h-11 w-11 items-center justify-center gap-1.5 rounded-control border border-transparent bg-transparent text-xs font-semibold text-fg hover:border-primary hover:bg-white/10 hover:text-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-primary sm:min-h-9 sm:w-auto sm:px-2.5"
                        onClick={() => { void onToggleDemo(); }}
                        aria-pressed={isDemoMode}
                        title={isDemoMode ? (lang === "vi" ? "Tải lại dữ liệu trực tuyến" : "Reload live data") : (lang === "vi" ? "Xem dự báo lại các bão 2021–2024" : "View hindcasts of 2021–2024 storms")}
                    >
                        {isDemoMode ? <Radio size={15} aria-hidden="true" /> : <FlaskConical size={15} aria-hidden="true" />}
                        <span className="hidden sm:inline">{isDemoMode ? (lang === "vi" ? "Dữ liệu trực tuyến" : "Live data") : (lang === "vi" ? "Dự báo lại" : "Hindcasts")}</span>
                    </button>
                    <button
                        className="btn-icon header-alert-trigger"
                        onClick={onOpenAlerts}
                        aria-label={t.subscribe_alerts}
                        title={t.subscribe_alerts}
                    >
                        <Bell
                            className="h-[18px] w-[18px]"
                            aria-hidden="true"
                        />
                    </button>
                    <details ref={optionsRef} className="header-options">
                        <summary aria-label={lang === "vi" ? "Tùy chọn hiển thị" : "Display options"} title={lang === "vi" ? "Tùy chọn" : "Options"}>
                            <MoreHorizontal size={20} aria-hidden="true" />
                        </summary>
                        <div className="header-options-menu">
                            <button type="button" onClick={() => { void onToggleDemo(); optionsRef.current?.removeAttribute("open"); }} aria-pressed={isDemoMode}>
                                {isDemoMode ? <Radio size={17} aria-hidden="true" /> : <FlaskConical size={17} aria-hidden="true" />}
                                {isDemoMode ? (lang === "vi" ? "Dữ liệu trực tuyến" : "Live data") : (lang === "vi" ? "Dự báo lại" : "Hindcasts")}
                            </button>
                            <button type="button" onClick={() => { onOpenAlerts(); optionsRef.current?.removeAttribute("open"); }}>
                                <Bell size={17} aria-hidden="true" />{t.subscribe_alerts}
                            </button>
                            <button type="button" onClick={refresh} disabled={isRefreshing} title={lang === "vi" ? "Làm mới dữ liệu từ máy chủ" : "Refresh data from the server"}>
                                <RefreshCw size={17} className={isRefreshing ? "animate-spin" : ""} aria-hidden="true" />{lang === "vi" ? "Làm mới dữ liệu" : "Refresh data"}
                            </button>
                            <button type="button" onClick={() => { onToggleLang(); optionsRef.current?.removeAttribute("open"); }}>
                                <Globe2 size={17} aria-hidden="true" />{lang === "vi" ? "English" : "Tiếng Việt"}
                            </button>
                            <button type="button" onClick={() => { onToggleTheme(); optionsRef.current?.removeAttribute("open"); }}>
                                {isDark ? <Sun size={17} aria-hidden="true" /> : <Moon size={17} aria-hidden="true" />}{isDark ? (lang === "vi" ? "Giao diện sáng" : "Light theme") : (lang === "vi" ? "Giao diện tối" : "Dark theme")}
                            </button>
                        </div>
                    </details>
                    <AuthControl lang={lang} onAuthenticated={onRefresh} />
                </nav>
            </div>
        </header>
    );
};
