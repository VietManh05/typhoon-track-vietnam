import React, { useEffect, useState, useCallback } from 'react';
import { Play, Pause, SkipBack, SkipForward, Clock } from 'lucide-react';
import { Fix, ForecastPoint } from '../types';
import { Language, translations } from '../i18n';

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

  // Combined timeline: all observations, followed by forecast points
  const totalCount = observations.length + forecastPoints.length;

  const handlePrev = useCallback(() => {
    onSelectIndex(Math.max(0, currentIndex - 1));
  }, [currentIndex, onSelectIndex]);

  const handleNext = useCallback(() => {
    onSelectIndex(Math.min(totalCount - 1, currentIndex + 1));
  }, [currentIndex, totalCount, onSelectIndex]);

  useEffect(() => {
    let timer: ReturnType<typeof setInterval>;
    if (isPlaying) {
      timer = setInterval(() => {
        onSelectIndex((currentIndex + 1) % totalCount);
      }, 1500);
    }
    return () => clearInterval(timer);
  }, [isPlaying, currentIndex, totalCount, onSelectIndex]);

  // Current active frame info
  const isForecastFrame = currentIndex >= observations.length;
  let frameTime = '';
  let frameLabel = '';
  let frameCategory = '';

  if (isForecastFrame) {
    const fp = forecastPoints[currentIndex - observations.length];
    frameTime = fp.valid_time;
    frameLabel = `+${fp.horizon_hours}h (${t.forecast_label})`;
    frameCategory = String(fp.intensity);
  } else {
    const obs = observations[currentIndex];
    frameTime = obs.timestamp;
    frameLabel = t.observed_fix;
    frameCategory = obs.intensity;
  }

  const formattedDate = new Date(frameTime).toLocaleString(
    lang === 'vi' ? 'vi-VN' : 'en-US',
    {
      hour: '2-digit',
      minute: '2-digit',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    }
  );

  // Accessible value text for slider
  const sliderValueText = `${frameLabel} — ${formattedDate} [${frameCategory}]`;

  return (
    <div className="glass-panel p-3 flex flex-col gap-2 animate-fade-in-up" role="region" aria-label={t.timeline_title}>
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-cyan-400" aria-hidden="true" />
          <span className="text-xs font-bold text-slate-200 uppercase tracking-wider font-display">
            {t.timeline_title}
          </span>
        </div>

        {/* Current frame badge */}
        <div className="flex items-center gap-2 font-mono text-xs">
          <span
            className={`px-2 py-0.5 rounded font-bold border text-[11px] ${
              isForecastFrame
                ? 'bg-amber-950/70 text-amber-300 border-amber-500/40'
                : 'bg-cyan-950/70 text-cyan-300 border-cyan-500/40'
            }`}
          >
            {frameLabel}
          </span>
          <span className="text-slate-300 font-semibold hidden sm:inline">{formattedDate}</span>
          <span className="text-slate-500 hidden sm:inline">[{frameCategory}]</span>
        </div>
      </div>

      {/* Scrub Slider & Controls */}
      <div className="flex items-center gap-3 mt-1">
        {/* Playback buttons */}
        <div className="flex items-center gap-1">
          <button
            onClick={handlePrev}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition active:scale-95 focus-ring touch-target"
            aria-label={t.timeline_prev}
          >
            <SkipBack className="w-3.5 h-3.5" aria-hidden="true" />
          </button>

          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-1.5 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white font-bold transition shadow-md shadow-cyan-500/20 active:scale-95 focus-ring touch-target"
            aria-label={isPlaying ? t.timeline_pause : t.timeline_play}
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5" aria-hidden="true" /> : <Play className="w-3.5 h-3.5 ml-0.5" aria-hidden="true" />}
          </button>

          <button
            onClick={handleNext}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition active:scale-95 focus-ring touch-target"
            aria-label={t.timeline_next}
          >
            <SkipForward className="w-3.5 h-3.5" aria-hidden="true" />
          </button>
        </div>

        {/* Slider */}
        <div className="flex-1 relative flex items-center">
          <input
            type="range"
            min={0}
            max={totalCount - 1}
            value={currentIndex}
            onChange={(e) => onSelectIndex(Number(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400 focus-ring"
            aria-label={t.aria_timeline_slider}
            aria-valuemin={0}
            aria-valuemax={totalCount - 1}
            aria-valuenow={currentIndex}
            aria-valuetext={sliderValueText}
          />
        </div>

        {/* Step counter */}
        <div className="text-xs font-mono text-slate-400 shrink-0" aria-hidden="true">
          {currentIndex + 1} / {totalCount}
        </div>
      </div>
    </div>
  );
};
