import React from "react";
import { CloudOff, AlertTriangle, Radar, RefreshCw } from "lucide-react";
import { Language, translations } from "../i18n";

interface LoadingProps {
    lang: Language;
}

/** Full-page skeleton shown while initial data loads */
export const DashboardSkeleton: React.FC<LoadingProps> = ({ lang }) => {
    const t = translations[lang];

    return (
        <div
            className="flex min-h-screen flex-col bg-page text-fg"
            role="status"
            aria-label={t.loading_data}
        >
            {/* Header skeleton */}
            <div className="w-full bg-slate-900/95 backdrop-blur-md border-b border-cyan-500/20 px-4 py-2.5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl skeleton" />
                    <div className="flex flex-col gap-1.5">
                        <div className="w-36 h-5 skeleton" />
                        <div className="w-52 h-3 skeleton hidden sm:block" />
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-24 h-7 rounded-full skeleton" />
                    <div className="w-8 h-8 rounded-lg skeleton" />
                    <div className="w-8 h-8 rounded-lg skeleton" />
                </div>
            </div>

            {/* Disclaimer skeleton */}
            <div className="w-full bg-amber-950/40 border-y border-amber-500/20 px-4 py-2 flex items-center justify-center">
                <div className="w-3/4 max-w-2xl h-3 skeleton" />
            </div>

            {/* Main content skeleton */}
            <main className="flex-1 p-3 md:p-4 grid grid-cols-1 lg:grid-cols-12 gap-4 max-w-[1800px] w-full mx-auto animate-fade-in">
                {/* Map placeholder */}
                <section className="lg:col-span-7 flex flex-col gap-3">
                    <div className="relative flex-1 min-h-[400px] lg:min-h-[600px] rounded-xl overflow-hidden border border-slate-800">
                        <div className="absolute inset-0 skeleton flex items-center justify-center">
                            <div className="flex flex-col items-center gap-3 text-slate-500">
                                <Radar className="h-12 w-12 animate-pulse" />
                                <span className="text-sm font-mono">
                                    {t.loading_map}
                                </span>
                            </div>
                        </div>
                    </div>
                    {/* Timeline skeleton */}
                    <div className="glass-panel p-3 flex items-center gap-3">
                        <div className="flex gap-1">
                            <div className="w-8 h-8 rounded-lg skeleton" />
                            <div className="w-8 h-8 rounded-lg skeleton" />
                            <div className="w-8 h-8 rounded-lg skeleton" />
                        </div>
                        <div className="flex-1 h-2 skeleton rounded-full" />
                        <div className="w-12 h-4 skeleton" />
                    </div>
                </section>

                {/* Right panel skeleton */}
                <section className="lg:col-span-5 flex flex-col gap-4">
                    {/* Storm overview skeleton */}
                    <div className="glass-panel p-4 flex flex-col gap-4">
                        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                            <div className="flex flex-col gap-1.5">
                                <div className="w-48 h-7 skeleton" />
                                <div className="w-32 h-3 skeleton" />
                            </div>
                            <div className="w-28 h-8 rounded-lg skeleton" />
                        </div>
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                            {[1, 2, 3, 4].map((i) => (
                                <div
                                    key={i}
                                    className="p-3 rounded-lg bg-slate-900/60 border border-slate-800"
                                >
                                    <div className="w-16 h-3 skeleton mb-2" />
                                    <div className="w-20 h-6 skeleton mb-1" />
                                    <div className="w-14 h-3 skeleton" />
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Province panel skeleton */}
                    <div className="glass-panel p-4 flex flex-col gap-3">
                        <div className="w-48 h-5 skeleton" />
                        <div className="w-full h-8 skeleton rounded-lg" />
                        <div className="flex flex-col gap-2">
                            {[1, 2, 3].map((i) => (
                                <div
                                    key={i}
                                    className="w-full h-10 skeleton rounded-lg"
                                />
                            ))}
                        </div>
                    </div>
                </section>
            </main>
        </div>
    );
};

/** Empty state when no storms are active */
export const EmptyState: React.FC<
    LoadingProps & { onLoadDemo: () => void; feedAvailable?: boolean }
> = ({ lang, onLoadDemo, feedAvailable = true }) => {
    const t = translations[lang];

    return (
        <div
            className="glass-panel p-8 flex flex-col items-center justify-center gap-4 text-center animate-fade-in-up"
            role="status"
        >
            <div className="w-16 h-16 rounded-2xl bg-cyan-950/50 border border-cyan-500/30 flex items-center justify-center">
                <CloudOff className="w-8 h-8 text-cyan-400" />
            </div>
            <div>
                <h3 className="text-lg font-bold font-display text-fg">
                    {feedAvailable
                        ? t.no_storms_found
                        : lang === "vi"
                          ? "Chưa kết nối nguồn dữ liệu bão trực tuyến"
                          : "Live tropical-cyclone feed is not connected"}
                </h3>
                <p className="text-sm text-fg-muted mt-1 max-w-md">
                    {feedAvailable
                        ? t.no_active_storms
                        : lang === "vi"
                          ? "Thời tiết địa phương đang cập nhật trực tiếp; dữ liệu bão chỉ có ở chế độ minh họa. Hãy dùng bản tin NCHMF cho quyết định vận hành."
                          : "Local weather is live; storm data is demo-only. Use official NCHMF bulletins for operational decisions."}
                </p>
            </div>
            <button
                onClick={onLoadDemo}
                className="btn-primary mt-2 px-5 font-semibold"
            >
                {t.view_demo_data}
            </button>
        </div>
    );
};

/** Inline error banner for API failures */
export const ErrorBanner: React.FC<LoadingProps & { onRetry?: () => void }> = ({
    lang,
    onRetry,
}) => {
    const t = translations[lang];

    return (
        <div
            className="flex w-full items-center justify-between gap-3 rounded-card border border-warning/35 bg-warning/10 px-3 py-2.5 text-xs animate-fade-in"
            role="status"
            aria-live="polite"
        >
            <div className="flex min-w-0 items-center gap-2 text-warning">
                <AlertTriangle
                    className="h-4 w-4 shrink-0"
                    aria-hidden="true"
                />
                <span className="font-medium text-fg" title={t.error_api_offline}>
                    <span className="hidden sm:inline">{t.error_api_offline}</span>
                    <span className="sm:hidden">{lang === "vi" ? "API chưa kết nối · dữ liệu mẫu" : "API offline · sample data"}</span>
                </span>
            </div>
            {onRetry && (
                <button
                    onClick={onRetry}
                    className="btn min-h-8 shrink-0 border-warning/35 bg-warning/10 px-2.5 text-warning hover:bg-warning/20"
                    aria-label={t.aria_refresh}
                >
                    <RefreshCw className="w-3 h-3" />
                    <span className="hidden sm:inline">
                        {t.error_reconnecting}
                    </span>
                </button>
            )}
        </div>
    );
};

/** Track loading indicator (inline within right panel) */
export const TrackLoadingIndicator: React.FC<LoadingProps> = ({ lang }) => {
    const t = translations[lang];

    return (
        <div
            className="glass-panel p-6 flex flex-col items-center justify-center gap-3 animate-fade-in"
            role="status"
        >
            <div className="relative w-10 h-10">
                <div className="absolute inset-0 rounded-full border-2 border-slate-700" />
                <div className="absolute inset-0 rounded-full border-2 border-cyan-400 border-t-transparent animate-spin" />
            </div>
            <span className="text-xs font-mono text-slate-400">
                {t.loading_track}
            </span>
        </div>
    );
};
