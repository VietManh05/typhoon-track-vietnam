import React, { useEffect, useState } from "react";
import { Language, translations } from "../../i18n";
import { ChevronDown, ChevronUp, Layers } from "lucide-react";
import { getIntensityToken } from "../../lib/storm";

interface MapLegendProps {
    lang: Language;
    showActualComparison?: boolean;
    showSuggestion?: boolean;
}

export const MapLegend: React.FC<MapLegendProps> = ({
    lang,
    showActualComparison = false,
    showSuggestion = false,
}) => {
    const compactLegendQuery = "(max-width: 1599px), (max-height: 1100px)";
    const [collapsed, setCollapsed] = useState(
        () => window.matchMedia(compactLegendQuery).matches,
    );
    useEffect(() => {
        const compactViewport = window.matchMedia(compactLegendQuery);
        const onViewportChange = (event: MediaQueryListEvent) => {
            setCollapsed(event.matches);
        };
        compactViewport.addEventListener("change", onViewportChange);
        return () => compactViewport.removeEventListener("change", onViewportChange);
    }, []);
    const t = translations[lang];

    const intensityItems: Array<{ key: string; color: string; label: string }> =
        [
            ...["TD", "TS", "STS", "TY", "STY", "SUPERTY"].map((key) => ({
                key,
                color: getIntensityToken(key).dot,
                label: t.categories[key] || key,
            })),
        ];

    return (
        <div
            className={`map-legend map-overlay absolute bottom-3 right-3 z-[1000] w-[min(280px,calc(100%-1.5rem))] p-2.5 font-mono text-xs text-fg transition-[width] duration-base ${collapsed ? "max-w-[150px]" : "max-w-[280px]"}`}
            data-collapsed={collapsed}
            role="region"
            aria-label={t.legend_title}
        >
            <button
                onClick={() => setCollapsed(!collapsed)}
                className={`flex min-h-8 w-full items-center justify-between gap-3 rounded-control font-sans focus-ring ${collapsed ? "" : "mb-2 border-b border-line pb-2"}`}
                aria-expanded={!collapsed}
                aria-label={t.legend_title}
            >
                <div className="flex items-center gap-1.5 text-xs font-semibold text-fg">
                    <Layers
                        className="h-3.5 w-3.5 text-primary"
                        aria-hidden="true"
                    />
                    <span className="map-legend-label">{t.legend_title}</span>
                </div>
                {collapsed ? (
                    <ChevronUp
                        className="h-4 w-4 text-fg-muted"
                        aria-hidden="true"
                    />
                ) : (
                    <ChevronDown
                        className="h-4 w-4 text-fg-muted"
                        aria-hidden="true"
                    />
                )}
            </button>

            {!collapsed && (
                <div className="flex flex-col gap-2.5 animate-fade-in">
                    {/* Tracks & Cone */}
                    <div className="flex flex-col gap-1.5">
                        <div className="flex items-center gap-2">
                            <div
                                className="h-0.5 w-4 border border-success bg-success"
                                aria-hidden="true"
                            />
                            <div
                                className="h-2 w-2 rounded-full bg-success"
                                aria-hidden="true"
                            />
                            <span className="text-xs text-fg-muted">
                                {t.legend_actual}
                            </span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div
                                className="h-0.5 w-4 border-t-2 border-dashed border-warning"
                                aria-hidden="true"
                            />
                            <div
                                className="h-2 w-2 rounded-full bg-warning"
                                aria-hidden="true"
                            />
                            <span className="text-xs text-fg-muted">
                                {showActualComparison
                                    ? lang === "vi"
                                        ? "Dự đoán từ mô hình training"
                                        : "Prediction from trained model"
                                    : t.legend_forecast}
                            </span>
                        </div>

                        <div className="flex items-center gap-2">
                            <div
                                className="h-3 w-4 rounded-badge border border-dashed border-[#ea580c] bg-[#fb923c]/20"
                                aria-hidden="true"
                            />
                            <span className="text-xs text-fg-muted">
                                {t.legend_cone}
                            </span>
                        </div>

                        {showActualComparison && (
                            <div className="flex items-center gap-2">
                                <div
                                    className="h-0.5 w-4 border-t-2 border-secondary"
                                    aria-hidden="true"
                                />
                                <div
                                    className="h-2 w-2 rounded-full bg-secondary"
                                    aria-hidden="true"
                                />
                                <span className="text-xs text-fg-muted">
                                    {t.legend_compare}
                                </span>
                            </div>
                        )}

                        {showSuggestion && (
                            <div className="flex items-center gap-2">
                                <div
                                    className="h-0.5 w-4 border-t-2 border-dotted border-pink-400"
                                    aria-hidden="true"
                                />
                                <div
                                    className="h-2 w-2 rounded-full bg-pink-400"
                                    aria-hidden="true"
                                />
                                <span className="text-xs text-fg-muted">
                                    {t.legend_suggestion}
                                </span>
                            </div>
                        )}
                    </div>

                    {/* Intensity Colors */}
                    <div className="flex flex-col gap-1 border-t border-line pt-2">
                        <span className="text-2xs font-semibold text-fg-faint">
                            {t.legend_intensity_scale}
                        </span>
                        <div className="grid grid-cols-2 gap-x-2 gap-y-1 text-2xs">
                            {intensityItems.map((item) => (
                                <div
                                    key={item.key}
                                    className="flex items-center gap-1.5"
                                >
                                    <span
                                        className={`w-2.5 h-2.5 rounded-full ${item.color}`}
                                        aria-hidden="true"
                                    />
                                    <span>{item.label}</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    {/* Vietnam Sovereignty Note */}
                    <div className="flex items-center gap-1.5 border-t border-line pt-1.5 text-2xs text-primary">
                        <span
                            className="h-1.5 w-1.5 rounded-full bg-primary"
                            aria-hidden="true"
                        />
                        <span>{t.legend_vietnam}</span>
                    </div>
                </div>
            )}
        </div>
    );
};
