import React, { useMemo, useState } from "react";
import { Activity, Gauge, Wind } from "lucide-react";
import { Language, translations } from "../i18n";
import { Fix, ForecastPoint } from "../types";

interface WindPressureChartProps {
    observations: Fix[];
    forecastPoints: ForecastPoint[];
    currentIndex: number;
    lang: Language;
}

interface ChartPoint {
    label: string;
    wind: number | null;
    pressure: number | null;
    forecast: boolean;
}

const WIDTH = 720;
const HEIGHT = 240;
const PLOT = { left: 52, right: 52, top: 28, bottom: 42 };

const xFor = (index: number, count: number) =>
    PLOT.left +
    (index / Math.max(1, count - 1)) * (WIDTH - PLOT.left - PLOT.right);

const pathFor = (
    points: ChartPoint[],
    value: "wind" | "pressure",
    scaleY: (value: number) => number,
    from: number,
    to: number,
) =>
    points
        .map((point, index) => ({ point, index }))
        .filter(
            ({ point, index }) =>
                index >= from && index <= to && point[value] !== null,
        )
        .map(
            ({ point, index }, pathIndex) =>
                (pathIndex === 0 ? "M" : "L") +
                " " +
                xFor(index, points.length).toFixed(1) +
                " " +
                scaleY(point[value] as number).toFixed(1),
        )
        .join(" ");

export const WindPressureChart: React.FC<WindPressureChartProps> = ({
    observations,
    forecastPoints,
    currentIndex,
    lang,
}) => {
    const [hoverIndex, setHoverIndex] = useState<number | null>(null);
    const t = translations[lang];
    const isVietnamese = lang === "vi";

    const points = useMemo<ChartPoint[]>(
        () => [
            ...observations.map((item) => ({
                label: new Date(item.timestamp).toLocaleString(
                    lang === "vi" ? "vi-VN" : "en-US",
                    {
                        day: "2-digit",
                        month: "2-digit",
                        hour: "2-digit",
                        minute: "2-digit",
                    },
                ),
                wind:
                    item.wind_kmh ??
                    (item.wind_ms ? Math.round(item.wind_ms * 3.6) : null),
                pressure: item.pressure_hpa,
                forecast: false,
            })),
            ...forecastPoints.map((item) => ({
                label: "+" + item.horizon_hours + "h",
                wind: item.wind_ms ? Math.round(item.wind_ms * 3.6) : null,
                pressure: item.pressure_hpa ?? null,
                forecast: true,
            })),
        ],
        [forecastPoints, lang, observations],
    );

    if (points.length < 2) return null;

    const winds = points.flatMap((point) =>
        point.wind === null ? [] : [point.wind],
    );
    const pressures = points.flatMap((point) =>
        point.pressure === null ? [] : [point.pressure],
    );
    const windMax = Math.ceil(Math.max(...winds, 1) / 20) * 20;
    const windMin = Math.max(0, Math.floor(Math.min(...winds, 0) / 20) * 20);
    const pressureMin = Math.floor((Math.min(...pressures, 980) - 8) / 10) * 10;
    const pressureMax = Math.ceil((Math.max(...pressures, 1010) + 8) / 10) * 10;
    const plotHeight = HEIGHT - PLOT.top - PLOT.bottom;
    const windY = (value: number) =>
        PLOT.top +
        (1 - (value - windMin) / Math.max(1, windMax - windMin)) * plotHeight;
    const pressureY = (value: number) =>
        PLOT.top +
        (1 - (value - pressureMin) / Math.max(1, pressureMax - pressureMin)) *
            plotHeight;
    const forecastStart = Math.max(0, observations.length - 1);
    const currentPointIndex = Math.max(
        0,
        Math.min(currentIndex, points.length - 1),
    );
    const selectedIndex = hoverIndex ?? currentPointIndex;
    const selected = points[selectedIndex];
    const selectedX = xFor(selectedIndex, points.length);
    const currentX = xFor(currentPointIndex, points.length);
    const xLabelIndexes = Array.from(
        new Set([0, Math.floor((points.length - 1) / 2), points.length - 1]),
    );
    const missingValue = "â€”";
    const selectedDescription =
        selected.label +
        ", " +
        (selected.forecast
            ? isVietnamese
                ? "dự báo"
                : "forecast"
            : isVietnamese
              ? "thực tế"
              : "actual") +
        ", " +
        t.wind_speed +
        " " +
        (selected.wind ?? missingValue) +
        " km/h, " +
        t.central_pressure +
        " " +
        (selected.pressure ?? missingValue) +
        " hPa";

    const onPointerMove = (event: React.PointerEvent<SVGSVGElement>) => {
        const bounds = event.currentTarget.getBoundingClientRect();
        const relativeX = ((event.clientX - bounds.left) / bounds.width) * WIDTH;
        const index = Math.round(
            ((relativeX - PLOT.left) / (WIDTH - PLOT.left - PLOT.right)) *
                (points.length - 1),
        );
        setHoverIndex(Math.max(0, Math.min(points.length - 1, index)));
    };

    const onKeyDown = (event: React.KeyboardEvent<SVGSVGElement>) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        event.preventDefault();
        const direction = event.key === "ArrowLeft" ? -1 : 1;
        setHoverIndex((value) =>
            Math.max(
                0,
                Math.min(points.length - 1, (value ?? currentIndex) + direction),
            ),
        );
    };

    return (
        <section
            className="panel overflow-hidden"
            aria-labelledby="wind-pressure-chart-title"
        >
            <div className="panel-head gap-4">
                <div className="min-w-0">
                    <div className="mb-1 flex items-center gap-2 text-primary">
                        <Activity className="h-4 w-4 shrink-0" aria-hidden="true" />
                        <span className="section-label">
                            {isVietnamese ? "Xu hướng cường độ" : "Intensity trend"}
                        </span>
                    </div>
                    <h2
                        id="wind-pressure-chart-title"
                        className="text-base font-semibold text-fg"
                    >
                        {t.wind_speed} &amp; {t.central_pressure}
                    </h2>
                </div>
                <div
                    className="flex flex-wrap items-center justify-end gap-x-3 gap-y-1 text-xs text-fg-muted"
                    aria-label={isVietnamese ? "Chú giải biểu đồ" : "Chart legend"}
                >
                    <span className="flex items-center gap-1.5">
                        <span className="h-0.5 w-4 rounded-full bg-fg" aria-hidden="true" />
                        {t.legend_actual}
                    </span>
                    <span className="flex items-center gap-1.5">
                        <span className="w-4 border-t-2 border-dashed border-fg" aria-hidden="true" />
                        {t.legend_forecast}
                    </span>
                </div>
            </div>

            <div className="relative px-1 pb-3 pt-2 sm:px-3">
                <div className="mb-1 flex flex-wrap items-center gap-x-4 gap-y-1 px-2 text-xs text-fg-muted">
                    <span className="flex items-center gap-1.5">
                        <span className="h-2.5 w-2.5 rounded-full bg-primary" aria-hidden="true" />
                        {t.wind_speed} <span className="text-fg-faint">(km/h)</span>
                    </span>
                    <span className="flex items-center gap-1.5">
                        <span className="h-2.5 w-2.5 rounded-full bg-warning" aria-hidden="true" />
                        {t.central_pressure} <span className="text-fg-faint">(hPa)</span>
                    </span>
                </div>

                <svg
                    viewBox={"0 0 " + WIDTH + " " + HEIGHT}
                    preserveAspectRatio="xMidYMid meet"
                    className="h-auto min-h-[190px] w-full touch-none rounded-control focus-ring sm:min-h-[220px]"
                    role="img"
                    aria-labelledby="wind-pressure-chart-svg-title wind-pressure-chart-svg-desc"
                    tabIndex={0}
                    onPointerMove={onPointerMove}
                    onPointerLeave={() => setHoverIndex(null)}
                    onKeyDown={onKeyDown}
                >
                    <title id="wind-pressure-chart-svg-title">
                        {t.wind_speed} &amp; {t.central_pressure}
                    </title>
                    <desc id="wind-pressure-chart-svg-desc">
                        {isVietnamese
                            ? "Đường liền là số liệu thực tế, đường đứt nét là dự báo. Dùng phím mũi tên trái và phải để xem từng thời điểm."
                            : "Solid lines are actual values and dashed lines are forecasts. Use the left and right arrow keys to inspect each time point."}
                    </desc>

                    {forecastPoints.length > 0 ? (
                        <rect
                            x={xFor(forecastStart, points.length)}
                            y={PLOT.top}
                            width={WIDTH - PLOT.right - xFor(forecastStart, points.length)}
                            height={plotHeight}
                            fill="rgba(139,92,246,.045)"
                        />
                    ) : null}

                    {[0, 0.25, 0.5, 0.75, 1].map((ratio) => {
                        const y = PLOT.top + ratio * plotHeight;
                        const windTick = Math.round(
                            windMax - ratio * (windMax - windMin),
                        );
                        const pressureTick = Math.round(
                            pressureMax - ratio * (pressureMax - pressureMin),
                        );
                        return (
                            <g key={ratio}>
                                <line
                                    x1={PLOT.left}
                                    x2={WIDTH - PLOT.right}
                                    y1={y}
                                    y2={y}
                                    stroke="rgba(148,163,184,.14)"
                                    strokeWidth="1"
                                />
                                <text
                                    x={PLOT.left - 9}
                                    y={y + 3}
                                    textAnchor="end"
                                    fill="#22d3ee"
                                    fontSize="9"
                                    fontFamily="JetBrains Mono, monospace"
                                >
                                    {windTick}
                                </text>
                                <text
                                    x={WIDTH - PLOT.right + 9}
                                    y={y + 3}
                                    fill="#f59e0b"
                                    fontSize="9"
                                    fontFamily="JetBrains Mono, monospace"
                                >
                                    {pressureTick}
                                </text>
                            </g>
                        );
                    })}

                    <text x={PLOT.left} y="13" fill="#22d3ee" fontSize="9" fontWeight="600">
                        km/h
                    </text>
                    <text
                        x={WIDTH - PLOT.right}
                        y="13"
                        textAnchor="end"
                        fill="#f59e0b"
                        fontSize="9"
                        fontWeight="600"
                    >
                        hPa
                    </text>

                    <path
                        d={pathFor(points, "wind", windY, 0, Math.max(0, observations.length - 1))}
                        fill="none"
                        stroke="#22d3ee"
                        strokeWidth="2.75"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                    <path
                        d={pathFor(points, "wind", windY, forecastStart, points.length - 1)}
                        fill="none"
                        stroke="#22d3ee"
                        strokeWidth="2.75"
                        strokeDasharray="7 6"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                    <path
                        d={pathFor(points, "pressure", pressureY, 0, Math.max(0, observations.length - 1))}
                        fill="none"
                        stroke="#f59e0b"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                    <path
                        d={pathFor(points, "pressure", pressureY, forecastStart, points.length - 1)}
                        fill="none"
                        stroke="#f59e0b"
                        strokeWidth="2"
                        strokeDasharray="7 6"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />

                    <line
                        x1={currentX}
                        x2={currentX}
                        y1={PLOT.top}
                        y2={HEIGHT - PLOT.bottom}
                        stroke="#f43f5e"
                        strokeWidth="1.5"
                        strokeDasharray="3 4"
                    />
                    <rect
                        x={Math.max(PLOT.left, Math.min(WIDTH - PLOT.right - 43, currentX - 21.5))}
                        y={PLOT.top + 4}
                        width="43"
                        height="14"
                        rx="7"
                        fill="#f43f5e"
                    />
                    <text
                        x={Math.max(PLOT.left + 21.5, Math.min(WIDTH - PLOT.right - 21.5, currentX))}
                        y={PLOT.top + 14}
                        textAnchor="middle"
                        fill="white"
                        fontSize="8"
                        fontWeight="700"
                    >
                        {isVietnamese ? "HIỆN TẠI" : "CURRENT"}
                    </text>

                    <line
                        x1={selectedX}
                        x2={selectedX}
                        y1={PLOT.top}
                        y2={HEIGHT - PLOT.bottom}
                        stroke="rgba(248,250,252,.38)"
                        strokeWidth="1"
                    />
                    {selected.wind !== null ? (
                        <circle
                            cx={selectedX}
                            cy={windY(selected.wind)}
                            r="4.5"
                            fill="#22d3ee"
                            stroke="#07101f"
                            strokeWidth="2.5"
                        />
                    ) : null}
                    {selected.pressure !== null ? (
                        <circle
                            cx={selectedX}
                            cy={pressureY(selected.pressure)}
                            r="4.5"
                            fill="#f59e0b"
                            stroke="#07101f"
                            strokeWidth="2.5"
                        />
                    ) : null}

                    {xLabelIndexes.map((index) => (
                        <text
                            key={index}
                            x={xFor(index, points.length)}
                            y={HEIGHT - 13}
                            textAnchor={
                                index === 0
                                    ? "start"
                                    : index === points.length - 1
                                      ? "end"
                                      : "middle"
                            }
                            fill="#94a3b8"
                            fontSize="9"
                            fontFamily="JetBrains Mono, monospace"
                        >
                            {points[index].label}
                        </text>
                    ))}
                </svg>

                <div
                    className="chart-readout mx-2 mb-2 flex flex-wrap items-center gap-x-4 gap-y-2 rounded-control border border-line bg-surface-2/70 px-3 py-2"
                    aria-hidden="true"
                >
                    <div className="flex items-center justify-between gap-3">
                        <span className="font-mono text-xs text-fg-muted">
                            {selected.label}
                        </span>
                        <span className="rounded-full bg-surface-3 px-1.5 py-0.5 text-[8px] font-semibold uppercase tracking-wide text-fg-faint">
                            {selected.forecast
                                ? isVietnamese
                                    ? "Dự báo"
                                    : "Forecast"
                                : isVietnamese
                                  ? "Thực tế"
                                  : "Actual"}
                        </span>
                    </div>
                    <div className="flex items-center justify-between gap-4 font-mono text-[10px]">
                        <span className="text-primary">{selected.wind ?? missingValue}</span>
                        <span className="text-fg-faint">km/h</span>
                    </div>
                    <div className="flex items-center justify-between gap-4 font-mono text-[10px]">
                        <span className="text-warning">{selected.pressure ?? missingValue}</span>
                        <span className="text-fg-faint">hPa</span>
                    </div>
                </div>

                <p className="sr-only" aria-live="polite">
                    {selectedDescription}
                </p>

                <div className="flex flex-wrap items-center justify-between gap-2 px-3 text-[10px] text-fg-faint">
                    <span className="flex items-center gap-1">
                        <Wind className="h-3 w-3 text-primary" aria-hidden="true" />
                        {isVietnamese ? "Gió · trục trái" : "Wind · left axis"}
                    </span>
                    <span className="flex items-center gap-1">
                        <Gauge className="h-3 w-3 text-warning" aria-hidden="true" />
                        {isVietnamese ? "Áp suất · trục phải" : "Pressure · right axis"}
                    </span>
                </div>

                <details className="mt-2 border-t border-line px-2 pt-2 text-xs text-fg-muted">
                    <summary className="cursor-pointer select-none rounded-sm focus-ring">
                        {isVietnamese ? "Xem bảng dữ liệu biểu đồ" : "View chart data table"}
                    </summary>
                    <div className="mt-2 max-h-40 overflow-auto">
                        <table className="w-full font-mono">
                            <caption className="sr-only">
                                {t.wind_speed} &amp; {t.central_pressure}
                            </caption>
                            <thead>
                                <tr className="text-left text-fg-faint">
                                    <th scope="col" className="py-1">{t.valid_time}</th>
                                    <th scope="col">{t.wind_speed} (km/h)</th>
                                    <th scope="col">{t.central_pressure} (hPa)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {points.map((point, index) => (
                                    <tr
                                        key={point.label + "-" + index}
                                        className="border-t border-line"
                                    >
                                        <td className="py-1">
                                            {point.label}
                                            <span className="sr-only">
                                                {point.forecast
                                                    ? isVietnamese
                                                        ? ", dự báo"
                                                        : ", forecast"
                                                    : isVietnamese
                                                      ? ", thực tế"
                                                      : ", actual"}
                                            </span>
                                        </td>
                                        <td>{point.wind ?? missingValue}</td>
                                        <td>{point.pressure ?? missingValue}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </details>
            </div>
        </section>
    );
};
