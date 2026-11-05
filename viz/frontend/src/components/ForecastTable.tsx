import React from "react";
import { CalendarClock } from "lucide-react";
import { Language, translations } from "../i18n";
import { formatCoordinate, formatShortDateTime, windKmh } from "../lib/format";
import { getIntensityToken } from "../lib/storm";
import { ForecastResponse } from "../types";

interface ForecastTableProps {
    forecast: ForecastResponse | null;
    lang: Language;
}

export const ForecastTable: React.FC<ForecastTableProps> = ({
    forecast,
    lang,
}) => {
    const t = translations[lang];
    if (!forecast?.points.length) return null;

    return (
        <section
            className="panel overflow-hidden"
            aria-labelledby="forecast-table-title"
        >
            <div className="panel-head">
                <div className="flex items-center gap-2">
                    <CalendarClock
                        className="h-4 w-4 text-primary"
                        aria-hidden="true"
                    />
                    <h2
                        id="forecast-table-title"
                        className="text-sm font-semibold text-fg"
                    >
                        {t.forecast_table}
                    </h2>
                </div>
                <time className="font-mono text-[10px] text-fg-muted">
                    {formatShortDateTime(forecast.issue_time, lang)}
                </time>
            </div>
            <div className="forecast-table-wrap p-2 pt-1">
                <table
                    className="forecast-table w-full table-fixed border-collapse text-left font-mono text-[10px]"
                    aria-label={t.aria_forecast_table}
                >
                    <colgroup>
                        <col className="w-[10%]" />
                        <col className="w-[19%]" />
                        <col className="w-[24%]" />
                        <col className="w-[19%]" />
                        <col className="w-[14%]" />
                        <col className="w-[14%]" />
                    </colgroup>
                    <thead>
                        <tr className="border-b border-line text-fg-faint">
                            {[
                                t.horizon,
                                `${t.valid_time} (VN)`,
                                t.coordinates,
                                t.category,
                                t.wind,
                                t.cone_radius,
                            ].map((heading) => (
                                <th
                                    key={heading}
                                    className="break-words px-1.5 py-2 align-bottom font-medium leading-tight"
                                    scope="col"
                                >
                                    {heading}
                                </th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {forecast.points.map((point) => {
                            const token = getIntensityToken(
                                String(point.intensity),
                            );
                            return (
                                <tr
                                    key={point.horizon_hours}
                                    className="border-b border-line/60 text-fg-muted transition-colors hover:bg-surface-2/70"
                                >
                                    <td className="break-words px-1.5 py-2.5 align-top font-semibold text-primary">
                                        +{point.horizon_hours}h
                                    </td>
                                    <td className="break-words px-1.5 py-2.5 align-top">
                                        {formatShortDateTime(
                                            point.valid_time,
                                            lang,
                                        )}
                                    </td>
                                    <td className="break-words px-1.5 py-2.5 align-top text-fg">
                                        {formatCoordinate(
                                            point.lat,
                                            "lat",
                                            lang,
                                        )}{" "}
                                        ·{" "}
                                        {formatCoordinate(
                                            point.lon,
                                            "lon",
                                            lang,
                                        )}
                                    </td>
                                    <td className="break-words px-1.5 py-2.5 align-top">
                                        <span
                                            className={`badge ${token.bg} ${token.border} ${token.text}`}
                                        >
                                            {String(point.intensity)}
                                        </span>
                                    </td>
                                    <td className="break-words px-1.5 py-2.5 align-top">
                                        {windKmh(point.wind_ms) ?? "—"}
                                        &nbsp;km/h
                                    </td>
                                    <td className="break-words px-1.5 py-2.5 align-top">
                                        ±{point.radius_km}&nbsp;km
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
            <p className="border-t border-line px-4 py-2 font-mono text-[10px] italic text-fg-faint">
                * {forecast.uncertainty_method}
            </p>
        </section>
    );
};
