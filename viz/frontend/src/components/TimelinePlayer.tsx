import React, { useCallback, useEffect, useMemo, useState } from "react";
import { Clock3, Pause, Play, SkipBack, SkipForward } from "lucide-react";
import { Language, translations } from "../i18n";
import { formatDateTime } from "../lib/format";
import { Fix, ForecastPoint } from "../types";

interface TimelinePlayerProps {
    observations: Fix[];
    forecastPoints: ForecastPoint[];
    currentIndex: number;
    onSelectIndex: (index: number) => void;
    lang: Language;
}

export const TimelinePlayer: React.FC<TimelinePlayerProps> = ({
    observations,
    forecastPoints,
    currentIndex,
    onSelectIndex,
    lang,
}) => {
    const [isPlaying, setIsPlaying] = useState(false);
    const t = translations[lang];
    const totalCount = observations.length + forecastPoints.length;

    const frame = useMemo(() => {
        const forecastIndex = currentIndex - observations.length;
        if (forecastIndex >= 0 && forecastPoints[forecastIndex]) {
            const item = forecastPoints[forecastIndex];
            return {
                time: item.valid_time,
                label: `+${item.horizon_hours}h · ${t.forecast_label}`,
                category: String(item.intensity),
                forecast: true,
            };
        }
        const item =
            observations[currentIndex] ?? observations[observations.length - 1];
        return item
            ? {
                  time: item.timestamp,
                  label: t.observed_fix,
                  category: item.intensity,
                  forecast: false,
              }
            : null;
    }, [
        currentIndex,
        forecastPoints,
        observations,
        t.forecast_label,
        t.observed_fix,
    ]);

    const previous = useCallback(
        () => onSelectIndex(Math.max(0, currentIndex - 1)),
        [currentIndex, onSelectIndex],
    );
    const next = useCallback(
        () => onSelectIndex(Math.min(totalCount - 1, currentIndex + 1)),
        [currentIndex, onSelectIndex, totalCount],
    );

    useEffect(() => {
        if (!isPlaying || totalCount < 2) return;
        const timer = window.setInterval(
            () => onSelectIndex((currentIndex + 1) % totalCount),
            1400,
        );
        return () => window.clearInterval(timer);
    }, [currentIndex, isPlaying, onSelectIndex, totalCount]);

    useEffect(() => {
        const pauseWhenHidden = () => {
            if (document.visibilityState === "hidden") setIsPlaying(false);
        };
        document.addEventListener("visibilitychange", pauseWhenHidden);
        return () =>
            document.removeEventListener("visibilitychange", pauseWhenHidden);
    }, []);

    if (!frame || totalCount === 0) return null;

    const formatted = formatDateTime(frame.time, lang);
    return (
        <section className="timeline-player panel p-3" aria-labelledby="timeline-title">
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2">
                    <Clock3
                        className="h-4 w-4 text-primary"
                        aria-hidden="true"
                    />
                    <h2
                        id="timeline-title"
                        className="section-label text-fg-muted"
                    >
                        <span className="hidden sm:inline">{t.timeline_title}</span>
                        <span className="sm:hidden">{lang === "vi" ? "Quỹ đạo bão" : "Storm track"}</span>
                    </h2>
                </div>
                <div className="flex items-center gap-2 text-[10px]">
                    <span
                        className={`badge ${frame.forecast ? "border-secondary/40 bg-secondary/10 text-secondary" : "border-primary/40 bg-primary/10 text-primary"}`}
                    >
                        {frame.label}
                    </span>
                    <time className="num hidden font-mono text-fg-muted sm:inline">
                        {formatted}
                    </time>
                    <span className="font-mono text-fg-faint">
                        {currentIndex + 1} / {totalCount}
                    </span>
                </div>
            </div>

            <div className="flex items-center gap-2.5">
                <button
                    className="btn-icon h-9 w-9"
                    onClick={previous}
                    disabled={currentIndex === 0}
                    aria-label={t.timeline_prev}
                    title={t.timeline_prev}
                >
                    <SkipBack className="h-4 w-4" aria-hidden="true" />
                </button>
                <button
                    className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-control border border-primary/50 bg-primary text-page transition-colors hover:bg-primary-deep"
                    onClick={() => setIsPlaying((value) => !value)}
                    aria-label={isPlaying ? t.timeline_pause : t.timeline_play}
                    title={isPlaying ? t.timeline_pause : t.timeline_play}
                >
                    {isPlaying ? (
                        <Pause className="h-4 w-4" aria-hidden="true" />
                    ) : (
                        <Play className="ml-0.5 h-4 w-4" aria-hidden="true" />
                    )}
                </button>
                <button
                    className="btn-icon h-9 w-9"
                    onClick={next}
                    disabled={currentIndex >= totalCount - 1}
                    aria-label={t.timeline_next}
                    title={t.timeline_next}
                >
                    <SkipForward className="h-4 w-4" aria-hidden="true" />
                </button>
                <input
                    type="range"
                    min={0}
                    max={totalCount - 1}
                    value={currentIndex}
                    onChange={(event) =>
                        onSelectIndex(Number(event.target.value))
                    }
                    className="min-w-0 flex-1 focus-ring"
                    aria-label={t.aria_timeline_slider}
                    aria-valuetext={`${frame.label} — ${formatted} — ${frame.category}`}
                />
            </div>
            <time className="mt-1 block text-center font-mono text-[10px] text-fg-faint sm:hidden">
                {formatted}
            </time>
        </section>
    );
};
