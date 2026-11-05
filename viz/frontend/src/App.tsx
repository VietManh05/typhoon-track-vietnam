import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Header } from './components/Header';
import { DisclaimerBanner } from './components/DisclaimerBanner';
import { ActiveStormSelector } from './components/ActiveStormSelector';
import { TyphoonMap } from './components/Map/TyphoonMap';
import { MapLegend } from './components/Map/MapLegend';
import { StormOverviewCard } from './components/StormOverviewCard';
import { TimelinePlayer } from './components/TimelinePlayer';
import { ForecastTable } from './components/ForecastTable';
import { ProvinceImpactPanel } from './components/ProvinceImpactPanel';
import { AlertModal } from './components/AlertModal';
import { DashboardSkeleton, EmptyState, ErrorBanner, TrackLoadingIndicator } from './components/LoadingStates';
import { CollapsibleSection } from './components/CollapsibleSection';
import { Language, translations } from './i18n';
import { ActiveTyphoonItem, Fix, StormTrackResponse, ProvinceImpact } from './types';
import {
  fetchActiveTyphoons,
  fetchStormTrack,
  calculateProvinceImpacts,
  bearingDeg,
  haversineKm,
} from './services/api';
import { MOCK_STORMS_LIST, MOCK_TRACKS } from './services/mockData';

export const App: React.FC = () => {
  const [lang, setLang] = useState<Language>('vi');
  const [isDark, setIsDark] = useState<boolean>(true);
  const [isLive, setIsLive] = useState<boolean>(false);
  // Demo data is shown only after an explicit user action, and always labelled.
  const [isDemo, setIsDemo] = useState<boolean>(false);
  const [trackError, setTrackError] = useState<string | null>(null);
  const [isAlertModalOpen, setIsAlertModalOpen] = useState<boolean>(false);

  // WS1: Loading & Error states
  const [isInitialLoading, setIsInitialLoading] = useState<boolean>(true);
  const [isTrackLoading, setIsTrackLoading] = useState<boolean>(false);
  const [loadError, setLoadError] = useState<boolean>(false);

  // Data states
  const [storms, setStorms] = useState<ActiveTyphoonItem[]>([]);
  const [selectedStormId, setSelectedStormId] = useState<string>('');
  const [stormTrack, setStormTrack] = useState<StormTrackResponse | null>(null);
  const [currentFixIndex, setCurrentFixIndex] = useState<number>(0);

  // Geographic provinces data
  const [provincesGeoJson, setProvincesGeoJson] = useState<any[]>([]);
  const [selectedProvinceId, setSelectedProvinceId] = useState<string | null>(null);

  const t = translations[lang];

  // 1. Initial Load: Check Health & Fetch Active Typhoons & Provinces GeoJSON
  useEffect(() => {
    const loadInitialData = async () => {
      setIsInitialLoading(true);
      setLoadError(false);

      try {
        // Load active storms; an empty list from a reachable backend is valid.
        const { typhoons, online } = await fetchActiveTyphoons();
        setStorms(typhoons);
        setIsLive(online);
        if (typhoons.length > 0) {
          setSelectedStormId(typhoons[0].id);
        }

        if (!online) {
          setLoadError(true);
        }
      } catch (err) {
        console.warn('Initial load error:', err);
        setLoadError(true);
      } finally {
        setIsInitialLoading(false);
      }

      // Load provinces GeoJSON for impact calculation
      try {
        const res = await fetch('/data/vietnam_provinces.geojson');
        const data = await res.json();
        if (data.features) {
          setProvincesGeoJson(data.features);
        }
      } catch (err) {
        console.warn('Could not load provinces:', err);
      }
    };

    loadInitialData();
  }, []);

  // 2. Load Track when selectedStormId changes
  useEffect(() => {
    if (!selectedStormId) return;

    let cancelled = false;
    setIsTrackLoading(true);
    setTrackError(null);
    const load = isDemo
      ? Promise.resolve(MOCK_TRACKS[selectedStormId])
      : fetchStormTrack(selectedStormId);
    load
      .then((data) => {
        if (cancelled) return;
        setStormTrack(data);
        // Set initial index to latest observation
        if (data.observations && data.observations.length > 0) {
          setCurrentFixIndex(data.observations.length - 1);
        }
      })
      .catch((err: unknown) => {
        if (cancelled) return;
        console.warn('Track load failed:', err);
        setStormTrack(null);
        setTrackError(err instanceof Error ? err.message : String(err));
      })
      .finally(() => {
        if (!cancelled) setIsTrackLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [selectedStormId, isDemo]);

  // 3. Sync Theme Class with <html> tag
  useEffect(() => {
    const root = document.documentElement;
    if (isDark) {
      root.classList.add('dark');
      root.classList.remove('light');
    } else {
      root.classList.add('light');
      root.classList.remove('dark');
    }
  }, [isDark]);

  // Selected storm object
  const currentStorm = useMemo(() => {
    return storms.find((s) => s.id === selectedStormId) || storms[0];
  }, [storms, selectedStormId]);

  // Active observation / forecast point according to scrubber
  const rawFix = useMemo((): Fix | undefined => {
    if (!stormTrack || !stormTrack.observations || stormTrack.observations.length === 0) {
      return currentStorm?.latest;
    }
    if (currentFixIndex < stormTrack.observations.length) {
      return stormTrack.observations[currentFixIndex];
    }
    // If in forecast frame
    const forecastIdx = currentFixIndex - stormTrack.observations.length;
    if (stormTrack.forecast && stormTrack.forecast.points[forecastIdx]) {
      const p = stormTrack.forecast.points[forecastIdx];
      // The model forecasts position and class only; never invent wind/pressure.
      return {
        timestamp: p.valid_time,
        lat: p.lat,
        lon: p.lon,
        wind_ms: p.wind_ms ?? null,
        pressure_hpa: p.pressure_hpa ?? null,
        intensity: (p.intensity as any) || 'UNK',
        source: stormTrack.forecast.model_kind,
        wind_kmh: p.wind_ms ? Math.round(p.wind_ms * 3.6) : undefined,
      };
    }
    return stormTrack.observations[stormTrack.observations.length - 1];
  }, [stormTrack, currentFixIndex, currentStorm]);

  // Movement (bearing/speed) from the previous point on the same timeline.
  const currentFix = useMemo(() => {
    if (!rawFix || !stormTrack) return rawFix;
    if (rawFix.bearing_deg != null && rawFix.speed_kmh != null) return rawFix;
    const timeline = [
      ...stormTrack.observations.map((o) => ({ t: o.timestamp, lat: o.lat, lon: o.lon })),
      ...(stormTrack.forecast?.points ?? []).map((p) => ({ t: p.valid_time, lat: p.lat, lon: p.lon })),
    ];
    const index = timeline.findIndex((p) => p.t === rawFix.timestamp);
    if (index < 1) return rawFix;
    const prev = timeline[index - 1];
    const hours = (Date.parse(rawFix.timestamp) - Date.parse(prev.t)) / 3.6e6;
    if (!(hours > 0)) return rawFix;
    return {
      ...rawFix,
      bearing_deg: rawFix.bearing_deg ?? bearingDeg(prev.lat, prev.lon, rawFix.lat, rawFix.lon),
      speed_kmh:
        rawFix.speed_kmh ??
        Math.round(haversineKm(prev.lat, prev.lon, rawFix.lat, rawFix.lon) / hours),
    };
  }, [rawFix, stormTrack]);

  // Calculate real-time province impacts
  const provinceImpacts: ProvinceImpact[] = useMemo(() => {
    if (!currentFix || provincesGeoJson.length === 0) return [];
    return calculateProvinceImpacts(
      provincesGeoJson,
      currentFix,
      stormTrack?.forecast?.points || []
    );
  }, [provincesGeoJson, currentFix, stormTrack]);

  const handleRefresh = useCallback(async () => {
    setLoadError(false);
    setTrackError(null);
    const { typhoons, online } = await fetchActiveTyphoons();
    setIsLive(online);
    setLoadError(!online);
    if (!online) return;
    setIsDemo(false);
    setStorms(typhoons);
    const keep = typhoons.some((s) => s.id === selectedStormId);
    const nextId = keep ? selectedStormId : typhoons[0]?.id ?? '';
    if (keep && nextId) {
      setIsTrackLoading(true);
      try {
        setStormTrack(await fetchStormTrack(nextId));
      } catch (err) {
        setStormTrack(null);
        setTrackError(err instanceof Error ? err.message : String(err));
      } finally {
        setIsTrackLoading(false);
      }
    } else {
      setStormTrack(null);
      setSelectedStormId(nextId);
    }
  }, [selectedStormId]);

  // WS1: Load clearly-labelled synthetic demo data on explicit user request
  const handleLoadDemo = useCallback(() => {
    setIsDemo(true);
    setStorms(MOCK_STORMS_LIST);
    setSelectedStormId(MOCK_STORMS_LIST[0].id);
  }, []);

  // WS1: Show full-page skeleton during initial load
  if (isInitialLoading) {
    return <DashboardSkeleton lang={lang} />;
  }

  return (
    <div className="flex flex-col min-h-screen bg-slate-950 text-slate-100">
      {/* 1. Top Navigation Bar */}
      <Header
        lang={lang}
        onToggleLang={() => setLang(lang === 'vi' ? 'en' : 'vi')}
        isDark={isDark}
        onToggleTheme={() => setIsDark(!isDark)}
        isLive={isLive}
        onRefresh={handleRefresh}
        onOpenAlerts={() => setIsAlertModalOpen(true)}
      />

      {/* 2. Permanent Legal & Meteorological Disclaimer Banner */}
      <DisclaimerBanner lang={lang} />

      {isDemo && (
        <div className="px-3 md:px-4 pt-2" role="status">
          <div className="rounded-lg border border-amber-500/60 bg-amber-950/60 px-3 py-2 text-xs font-mono text-amber-200">
            {lang === 'vi'
              ? 'DỮ LIỆU DEMO MÔ PHỎNG — không phải cơn bão thật, quan trắc hay dự báo thật.'
              : 'SYNTHETIC DEMO DATA — not a real storm, observation or forecast.'}
          </div>
        </div>
      )}

      {trackError && !isTrackLoading && (
        <div className="px-3 md:px-4 pt-2" role="alert">
          <div className="rounded-lg border border-red-500/60 bg-red-950/60 px-3 py-2 text-xs font-mono text-red-200">
            {lang === 'vi' ? 'Không tải được quỹ đạo/dự báo: ' : 'Could not load track/forecast: '}
            {trackError}
          </div>
        </div>
      )}

      {/* WS1: Error Banner when API is offline */}
      {loadError && (
        <div className="px-3 md:px-4 pt-2">
          <ErrorBanner lang={lang} onRetry={handleRefresh} />
        </div>
      )}

      {/* 3. Tracked Cyclones Strip */}
      {storms.length > 0 && (
        <ActiveStormSelector
          storms={storms}
          selectedStormId={selectedStormId}
          onSelectStorm={(id) => {
            setSelectedStormId(id);
          }}
          lang={lang}
        />
      )}

      {/* WS1: Empty State when no storms */}
      {storms.length === 0 && !isInitialLoading && (
        <div className="flex-1 flex items-center justify-center p-6">
          <EmptyState lang={lang} onLoadDemo={handleLoadDemo} />
        </div>
      )}

      {/* 4. Main Dashboard Layout */}
      {storms.length > 0 && (
        <main className="flex-1 p-3 md:p-4 grid grid-cols-1 lg:grid-cols-12 gap-4 max-w-[1800px] w-full mx-auto">
          {/* Left Column (7 cols): Map & Timeline Player */}
          <section className="lg:col-span-7 flex flex-col gap-3 min-h-[400px] lg:min-h-[750px]" aria-label={t.aria_map_container}>
            <div className="relative flex-1 rounded-xl overflow-hidden shadow-2xl border border-slate-800">
              <TyphoonMap
                observations={stormTrack?.observations || []}
                currentFixIndex={currentFixIndex}
                forecast={stormTrack?.forecast || null}
                selectedProvinceId={selectedProvinceId}
                onSelectProvince={(id) => setSelectedProvinceId(id)}
                lang={lang}
              />
              {/* Interactive Map Legend */}
              <MapLegend lang={lang} />
            </div>

            {/* Interactive Scrubbing Timeline Player */}
            {stormTrack && stormTrack.observations && (
              <TimelinePlayer
                observations={stormTrack.observations}
                forecastPoints={stormTrack.forecast?.points || []}
                currentIndex={currentFixIndex}
                onSelectIndex={(idx) => setCurrentFixIndex(idx)}
                lang={lang}
              />
            )}
          </section>

          {/* Right Column (5 cols): Metrics, Province Impact, and Forecast Table */}
          <aside className="lg:col-span-5 flex flex-col gap-4 overflow-y-auto lg:max-h-[calc(100vh-10rem)] pr-1" aria-label={lang === 'vi' ? 'Bảng điều khiển thông số bão' : 'Storm parameters panel'}>
            {/* WS1: Track loading indicator */}
            {isTrackLoading && <TrackLoadingIndicator lang={lang} />}

            {/* A. Storm Core Metrics Overview Card */}
            {!isTrackLoading && currentStorm && currentFix && (
              <CollapsibleSection
                id="storm-overview"
                title={t.storm_overview}
                defaultOpen={true}
                lang={lang}
              >
                <StormOverviewCard
                  storm={currentStorm}
                  currentFix={currentFix}
                  forecast={stormTrack?.forecast || null}
                  lang={lang}
                />
              </CollapsibleSection>
            )}

            {/* B. Province Impact & Proximity Vulnerability Assessment */}
            {!isTrackLoading && provinceImpacts.length > 0 && (
              <CollapsibleSection
                id="province-impact"
                title={t.province_impact_title}
                defaultOpen={true}
                lang={lang}
              >
                <ProvinceImpactPanel
                  impacts={provinceImpacts}
                  selectedProvinceId={selectedProvinceId}
                  onSelectProvince={(id) => setSelectedProvinceId(id)}
                  lang={lang}
                />
              </CollapsibleSection>
            )}

            {/* C. Multi-Horizon Numerical Forecast Table */}
            {!isTrackLoading && stormTrack && stormTrack.forecast && (
              <CollapsibleSection
                id="forecast-table"
                title={t.forecast_table}
                defaultOpen={false}
                lang={lang}
              >
                <ForecastTable forecast={stormTrack.forecast} lang={lang} />
              </CollapsibleSection>
            )}
          </aside>
        </main>
      )}

      {/* 5. Alert & Webhook Subscription Modal */}
      <AlertModal
        isOpen={isAlertModalOpen}
        onClose={() => setIsAlertModalOpen(false)}
        lang={lang}
      />
    </div>
  );
};
