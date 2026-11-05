import React from "react";
import {
    Crosshair,
    Gauge,
    Info,
    Layers3,
    Navigation,
    Radio,
    ShieldAlert,
    Wind,
} from "lucide-react";
import { Language, TranslationStrings, translations } from "../i18n";
import {
    beaufortFromKmh,
    formatCoordinate,
    formatDateTime,
    windKmh,
} from "../lib/format";
import { getIntensityToken } from "../lib/storm";
import { ActiveTyphoonItem, Fix, ForecastResponse } from "../types";

interface StormOverviewCardProps {
    storm: ActiveTyphoonItem;
    currentFix: Fix;
    forecast: ForecastResponse | null;
    lang: Language;
}

interface MetricCardProps {
    icon: React.ReactNode;
    label: string;
    value: React.ReactNode;
    secondary: React.ReactNode;
    accent: string;
}

const MetricCard: React.FC<MetricCardProps> = ({
    icon,
    label,
    value,
    secondary,
    accent,
}) => (
    <article className="metric-tile min-h-[132px]">
        <div className={`mb-2 flex items-center gap-2 ${accent}`}>
            {icon}
            <h3 className="text-xs font-semibold text-fg-muted">
                {label}
            </h3>
        </div>
        <div className="num text-[28px] font-bold leading-tight tracking-tight text-fg">
            {value}
        </div>
        <div className="num mt-2 text-xs leading-5 text-fg-muted">
            {secondary}
        </div>
    </article>
);

const getBearingCompass = (deg: number, t: TranslationStrings): string => {
    const keys: Array<keyof TranslationStrings> = [
        "bearing_N",
        "bearing_NNE",
        "bearing_NE",
        "bearing_ENE",
        "bearing_E",
        "bearing_ESE",
        "bearing_SE",
        "bearing_SSE",
        "bearing_S",
        "bearing_SSW",
        "bearing_SW",
        "bearing_WSW",
        "bearing_W",
        "bearing_WNW",
        "bearing_NW",
        "bearing_NNW",
    ];
    return t[keys[Math.round(deg / 22.5) % 16]] as string;
};

export const StormOverviewCard: React.FC<StormOverviewCardProps> = ({
    storm,
    currentFix,
    forecast,
    lang,
}) => {
    const t = translations[lang];
    const category = currentFix.intensity || "UNK";
    const categoryToken = getIntensityToken(category);
    const speed = windKmh(currentFix.wind_ms, currentFix.wind_kmh);
    const beaufort = currentFix.beaufort_level ?? beaufortFromKmh(speed);
    // Movement must come from the track; never substitute a default.
    const bearing = currentFix.bearing_deg ?? null;
    const movementSpeed = currentFix.speed_kmh ?? null;
    const warnings = forecast?.warnings ?? [];

    return (
        <section
            className="panel overflow-hidden"
            aria-label={t.storm_overview}
        >
            <div className="panel-head items-start">
                <div className="min-w-0">
                    <div className="mb-1 flex flex-wrap items-center gap-2">
                        <span className="section-label">
                            {t.storm_overview}
                        </span>
                        <span className="badge border-line bg-surface-2 font-mono text-fg-faint">
                            {storm.id}
                        </span>
                    </div>
                    <h2 className="truncate text-xl font-bold tracking-tight text-fg sm:text-2xl">
                        {lang === "vi" && storm.name_vi
                            ? storm.name_vi
                            : storm.name}
                    </h2>
                    <div className="mt-1 flex items-center gap-1.5 text-xs text-fg-muted">
                        <Radio
                            className="h-3 w-3 text-success"
                            aria-hidden="true"
                        />
                        <span>{t.last_observation}</span>
                        <time className="font-mono text-fg">
                            {formatDateTime(currentFix.timestamp, lang)}
                        </time>
                    </div>
                </div>
                <span
                    className={`badge shrink-0 px-2.5 py-1 ${categoryToken.bg} ${categoryToken.border} ${categoryToken.text}`}
                >
                    <ShieldAlert className="h-3.5 w-3.5" aria-hidden="true" />
                    {t.categories[category] || category}
                </span>
            </div>

            <div className="panel-body space-y-3">
                <div className="grid grid-cols-2 gap-2.5">
                    <MetricCard
                        icon={<Wind className="h-4 w-4" aria-hidden="true" />}
                        label={t.wind_speed}
                        accent="text-primary"
                        value={
                            <>
                                {speed ?? "—"}{" "}
                                <span className="text-sm font-medium text-fg-muted">
                                    km/h
                                </span>
                            </>
                        }
                        secondary={
                            <>
                                {currentFix.wind_ms ?? "—"}&nbsp;m/s ·{" "}
                                {t.beaufort_prefix}&nbsp;{beaufort}
                            </>
                        }
                    />
                    <MetricCard
                        icon={<Gauge className="h-4 w-4" aria-hidden="true" />}
                        label={t.central_pressure}
                        accent="text-warning"
                        value={
                            <>
                                {currentFix.pressure_hpa ?? "—"}{" "}
                                <span className="text-sm font-medium text-fg-muted">
                                    hPa
                                </span>
                            </>
                        }
                        secondary={
                            currentFix.pressure_hpa &&
                            currentFix.pressure_hpa < 980
                                ? t.pressure_deep
                                : t.pressure_normal
                        }
                    />
                    <MetricCard
                        icon={
                            <Crosshair className="h-4 w-4" aria-hidden="true" />
                        }
                        label={t.position}
                        accent="text-success"
                        value={
                            <span className="text-2xl">
                                {formatCoordinate(currentFix.lat, "lat", lang)}
                            </span>
                        }
                        secondary={
                            <span className="text-lg font-semibold text-fg">
                                {formatCoordinate(currentFix.lon, "lon", lang)}
                            </span>
                        }
                    />
                    <MetricCard
                        icon={
                            <Navigation
                                className="h-4 w-4"
                                style={{ transform: `rotate(${bearing ?? 0}deg)` }}
                                aria-hidden="true"
                            />
                        }
                        label={t.movement}
                        accent="text-secondary"
                        value={
                            <>
                                {movementSpeed ?? "—"}{" "}
                                {movementSpeed != null && (
                                    <span className="text-sm font-medium text-fg-muted">
                                        km/h
                                    </span>
                                )}
                            </>
                        }
                        secondary={
                            <>
                                {bearing != null ? `${getBearingCompass(bearing, t)} · ${bearing}°` : "—"}
                            </>
                        }
                    />
                </div>

                {warnings.length > 0 ? (
                    <div
                        className="rounded-card border border-warning/35 bg-warning/[0.07] p-3"
                        role="alert"
                    >
                        <div className="mb-2 flex items-center gap-2 text-warning">
                            <ShieldAlert
                                className="h-4 w-4"
                                aria-hidden="true"
                            />
                            <strong className="text-xs">
                                {lang === "vi"
                                    ? "Cảnh báo tác động"
                                    : "Impact warning"}
                            </strong>
                        </div>
                        <ul className="space-y-2 text-sm leading-6 text-fg-muted">
                            {warnings.map((warning) => (
                                <li key={warning}>{warning}</li>
                            ))}
                        </ul>
                    </div>
                ) : null}

                {forecast ? (
                    <div className="flex flex-wrap items-center justify-between gap-3 border-t border-line pt-3 text-xs text-fg-faint">
                        <span className="flex items-center gap-1.5">
                            <Info
                                className="h-3 w-3 text-primary"
                                aria-hidden="true"
                            />
                            {t.model_version}:{" "}
                            <b className="font-mono text-fg-muted">
                                {forecast.model_version}
                            </b>
                        </span>
                        <span className="flex items-center gap-1.5">
                            <Layers3
                                className="h-3 w-3 text-primary"
                                aria-hidden="true"
                            />
                            {t.data_source}:{" "}
                            <b className="text-fg-muted">
                                {forecast.sources.join(", ")}
                            </b>
                        </span>
                    </div>
                ) : null}
            </div>
        </section>
    );
};
