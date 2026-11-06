import React, {
    lazy,
    Suspense,
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";
import { Header } from "./components/Header";
import { DisclaimerBanner } from "./components/DisclaimerBanner";
import { ActiveStormSelector } from "./components/ActiveStormSelector";
import { TyphoonMap } from "./components/Map/TyphoonMap";
import { MapLegend } from "./components/Map/MapLegend";
import { MapLocationSearch } from "./components/Map/MapLocationSearch";
import { StormOverviewCard } from "./components/StormOverviewCard";
import { TimelinePlayer } from "./components/TimelinePlayer";
import { ForecastTable } from "./components/ForecastTable";
import { ProvinceImpactPanel } from "./components/ProvinceImpactPanel";
import { AlertModal } from "./components/AlertModal";
import { WeatherPanel } from "./components/WeatherPanel";
import { DEMO_WEATHER_LOCATIONS, getDemoWeather } from "./services/demoWeather";
import { impactsByUnit, weatherLocationForProvince } from "./data/vietnamLocations";
import { OllamaAssistant } from "./components/OllamaAssistant";
import {
    DashboardSkeleton,
    ErrorBanner,
    TrackLoadingIndicator,
} from "./components/LoadingStates";
import { CollapsibleSection } from "./components/CollapsibleSection";
import { Language, translations } from "./i18n";
import {
    ActiveTyphoonItem,
    Fix,
    ProvinceImpact,
    ProvinceGeoFeature,
    StormTrackResponse,
    WeatherLocation,
    CurrentWeather,
    HourlyWeather,
    DailyWeather,
} from "./types";
import {
    checkBackendHealth,
    fetchActiveTyphoons,
    fetchStormTrack,
    calculateProvinceImpacts,
    fetchLocalWeather,
    fetchCurrentWeather,
    fetchWeatherLocations,
    fetchHindcastIndex,
    fetchHindcastTrack,
    bearingDeg,
    haversineKm,
} from "./services/api";
import { SuggestionPanel } from "./components/SuggestionPanel";
import "./styles/explorer.css";
import "./styles/fullscreen-map.css";
import "./styles/easy-read.css";
import { Bot, CloudSun, Radar, ChartNoAxesCombined, PanelRightClose, PanelRightOpen, MapPin, CloudOff } from "lucide-react";

const WindPressureChart = lazy(() =>
    import("./components/WindPressureChart").then((module) => ({
        default: module.WindPressureChart,
    })),
);

export const App: React.FC = () => {
    const [lang, setLang] = useState<Language>(() =>
        localStorage.getItem("typhoon-language") === "en" ? "en" : "vi",
    );
    const [isDark, setIsDark] = useState<boolean>(
        // Bright daylight theme by default (easiest to read for everyone); dark is opt-in.
        () => localStorage.getItem("typhoon-theme") === "dark",
    );
    const [isLive, setIsLive] = useState<boolean>(false);
    const [isAlertModalOpen, setIsAlertModalOpen] = useState<boolean>(false);
    const [alertsAvailable, setAlertsAvailable] = useState<boolean | null>(null);
    const [alertUnavailableReason, setAlertUnavailableReason] = useState<string | null>(null);
    const [weatherLocations, setWeatherLocations] = useState<WeatherLocation[]>([]);
    const [weatherLocationId, setWeatherLocationId] = useState("da-nang");
    const [currentWeather, setCurrentWeather] = useState<CurrentWeather | null>(null);
    const [hourlyWeather, setHourlyWeather] = useState<HourlyWeather[]>([]);
    const [dailyWeather, setDailyWeather] = useState<DailyWeather[]>([]);
    const [weatherLoading, setWeatherLoading] = useState(false);
    const [weatherError, setWeatherError] = useState<string | null>(null);
    const [mapWeather, setMapWeather] = useState<Record<string, CurrentWeather>>({});

    // WS1: Loading & Error states
    const [isInitialLoading, setIsInitialLoading] = useState<boolean>(true);
    const [isTrackLoading, setIsTrackLoading] = useState<boolean>(false);
    const [loadError, setLoadError] = useState<boolean>(false);

    // Data states
    const [storms, setStorms] = useState<ActiveTyphoonItem[]>([]);
    const [selectedStormId, setSelectedStormId] = useState<string>("");
    const [isDemoMode, setIsDemoMode] = useState<boolean>(false);
    const [stormFeedAvailable, setStormFeedAvailable] = useState<boolean>(true);
    const [stormTrack, setStormTrack] = useState<StormTrackResponse | null>(
        null,
    );
    const [currentFixIndex, setCurrentFixIndex] = useState<number>(0);

    // Geographic provinces data
    const [provincesGeoJson, setProvincesGeoJson] = useState<
        ProvinceGeoFeature[]
    >([]);
    const [selectedProvinceId, setSelectedProvinceId] = useState<string | null>(
        null,
    );

    const t = translations[lang];
    const [detailTab, setDetailTab] = useState<"weather" | "assistant" | "storm" | "analysis">("weather");
    // Map-first (like Windy): the detail panel opens once the user picks something.
    const [detailsOpen, setDetailsOpen] = useState(false);
    useEffect(() => {
        const compactViewport = window.matchMedia("(max-width: 767px)");
        const onViewportChange = (event: MediaQueryListEvent) => {
            if (event.matches) setDetailsOpen(false);
        };
        compactViewport.addEventListener("change", onViewportChange);
        return () => compactViewport.removeEventListener("change", onViewportChange);
    }, []);
    const chromeRef = useRef<HTMLDivElement>(null);
    const detailsRef = useRef<HTMLElement>(null);
    const selectDetailTab = (tab: "weather" | "assistant" | "storm" | "analysis") => {
        setDetailTab(tab);
        detailsRef.current?.scrollTo({ top: 0 });
    };
    useEffect(() => {
        if (!chromeRef.current) return;
        const observer = new ResizeObserver(([entry]) => {
            document.documentElement.style.setProperty("--map-chrome-height", entry.contentRect.height + "px");
        });
        observer.observe(chromeRef.current);
        return () => observer.disconnect();
    }, [isInitialLoading]);

    // 1. Initial Load: Check Health & Fetch Active Typhoons & Provinces GeoJSON
    useEffect(() => {
        const loadInitialData = async () => {
            setIsInitialLoading(true);
            setLoadError(false);

            try {
                // Check backend health
                const { online } = await checkBackendHealth();
                setIsLive(online);

                // Load active storms
                const { typhoons, isLive: liveStatus, feedAvailable } =
                    await fetchActiveTyphoons();
                setStorms(typhoons);
                setStormFeedAvailable(feedAvailable);
                setIsDemoMode(false);
                setIsLive(online && liveStatus && feedAvailable);
                // Map-first: nothing is selected until the user picks a storm.

                if (!liveStatus) {
                    setLoadError(true);
                }
            } catch (err) {
                console.warn("Initial load error:", err);
                setStorms([]);
                setSelectedStormId("");
                setStormTrack(null);
                setIsLive(false);
                setStormFeedAvailable(false);
                setLoadError(true);
            } finally {
                setIsInitialLoading(false);
            }

            // Load provinces GeoJSON for impact calculation
            try {
                const res = await fetch("/data/vietnam_provinces.geojson");
                const data = await res.json();
                if (data.features) {
                    // GADM names are run together ("QuảngNinh"): space them once for display.
                    setProvincesGeoJson(data.features.map((f: ProvinceGeoFeature) => ({
                        ...f,
                        properties: { ...f.properties, name: f.properties.name.replace(/(\p{Ll})(\p{Lu})/gu, "$1 $2") },
                    })));
                }
            } catch (err) {
                console.warn("Could not load provinces:", err);
            }
        };

        loadInitialData();
    }, []);

    useEffect(() => {
        if (isDemoMode) {
            setWeatherLocations(DEMO_WEATHER_LOCATIONS);
            setMapWeather(Object.fromEntries(
                DEMO_WEATHER_LOCATIONS.map((location) => [location.id, getDemoWeather(location.id).current]),
            ));
            if (!DEMO_WEATHER_LOCATIONS.some((location) => location.id === weatherLocationId)) {
                setWeatherLocationId(DEMO_WEATHER_LOCATIONS[0].id);
            }
            return;
        }
        let cancelled = false;
        setMapWeather({});
        fetchWeatherLocations()
            .then((locations) => {
                if (cancelled) return;
                setWeatherLocations(locations);
                // Selected-location weather is loaded by the effect below.
                // Avoid one provider call per province during initial loading.
            })
            .catch(() => {
                if (!cancelled) setWeatherLocations(DEMO_WEATHER_LOCATIONS);
            });
        return () => { cancelled = true; };
    }, [isDemoMode]);

    useEffect(() => {
        let cancelled = false;
        fetch("/subscriptions", { headers: { Accept: "application/json" } })
            .then(async (response) => {
                const payload = await response.json().catch(() => ({}));
                if (cancelled) return;
                if (response.ok && payload.available === true && payload.delivery === "active") {
                    setAlertsAvailable(true);
                    setAlertUnavailableReason(null);
                } else {
                    setAlertsAvailable(false);
                    setAlertUnavailableReason(payload.error?.message || null);
                }
            })
            .catch(() => {
                if (!cancelled) {
                    setAlertsAvailable(false);
                    setAlertUnavailableReason(null);
                }
            });
        return () => { cancelled = true; };
    }, []);

    useEffect(() => {
        let cancelled = false;
        if (isDemoMode) {
            const demo = getDemoWeather(weatherLocationId);
            setCurrentWeather(demo.current);
            setHourlyWeather(demo.hourly);
            setDailyWeather(demo.daily);
            setWeatherLoading(false);
            setWeatherError(null);
            return;
        }
        setWeatherLoading(true);
        setWeatherError(null);
        fetchLocalWeather(weatherLocationId)
            .then((data) => {
                if (cancelled) return;
                setCurrentWeather(data.current);
                setMapWeather((previous) => ({
                    ...previous,
                    [data.current.location.id]: data.current,
                }));
                setHourlyWeather(data.hourly);
                setDailyWeather(data.daily);
            })
            .catch((error: unknown) => {
                if (!cancelled) {
                    if (DEMO_WEATHER_LOCATIONS.some((location) => location.id === weatherLocationId)) {
                        const demo = getDemoWeather(weatherLocationId);
                        setCurrentWeather(demo.current);
                        setHourlyWeather(demo.hourly);
                        setDailyWeather(demo.daily);
                        setWeatherError(null);
                    } else {
                        setCurrentWeather(null);
                        setHourlyWeather([]);
                        setDailyWeather([]);
                        setWeatherError(
                            error instanceof Error
                                ? error.message
                                : "Dữ liệu thời tiết tạm thời không khả dụng",
                        );
                    }
                }
            })
            .finally(() => {
                if (!cancelled) setWeatherLoading(false);
            });
        return () => {
            cancelled = true;
        };
    }, [isDemoMode, weatherLocationId]);

    // 2. Load the selected track. Demo tracks are never an API fallback.
    useEffect(() => {
        if (!selectedStormId) {
            setStormTrack(null);
            return;
        }
        if (isDemoMode) {
            // Hindcast archive: real past storms re-forecast by the trained model.
            let cancelled = false;
            setIsTrackLoading(true);
            fetchHindcastTrack(selectedStormId)
                .then((data) => {
                    if (cancelled) return;
                    setStormTrack(data);
                    setCurrentFixIndex(Math.max(0, data.observations.length - 1));
                })
                .catch(() => {
                    if (!cancelled) setStormTrack(null);
                })
                .finally(() => {
                    if (!cancelled) setIsTrackLoading(false);
                });
            return () => {
                cancelled = true;
            };
        }

        let cancelled = false;
        setStormTrack(null);
        setIsTrackLoading(true);
        fetchStormTrack(selectedStormId)
            .then((data) => {
                if (cancelled) return;
                setStormTrack(data);
                setLoadError(false);
                setCurrentFixIndex(Math.max(0, data.observations.length - 1));
            })
            .catch(() => {
                if (!cancelled) {
                    setStormTrack(null);
                    setLoadError(true);
                }
            })
            .finally(() => {
                if (!cancelled) setIsTrackLoading(false);
            });
        return () => {
            cancelled = true;
        };
    }, [isDemoMode, selectedStormId]);

    // Keep the live bulletin and selected track current while the page is open.
    useEffect(() => {
        if (isDemoMode || isInitialLoading) return;
        let cancelled = false;
        let running = false;
        const refreshLive = async () => {
            if (cancelled || running || document.visibilityState === "hidden") return;
            running = true;
            try {
                const { online } = await checkBackendHealth();
                const active = await fetchActiveTyphoons();
                if (cancelled) return;
                setStorms(active.typhoons);
                setStormFeedAvailable(active.feedAvailable);
                setIsLive(online && active.isLive && active.feedAvailable);
                setLoadError(false);
                // Keep the user's pick; never auto-select on refresh.
                const nextId = active.typhoons.some((item) => item.id === selectedStormId)
                    ? selectedStormId
                    : "";
                if (nextId !== selectedStormId) {
                    setSelectedStormId(nextId);
                } else if (nextId) {
                    const track = await fetchStormTrack(nextId);
                    if (!cancelled) {
                        setStormTrack(track);
                        setCurrentFixIndex(Math.max(0, track.observations.length - 1));
                    }
                } else {
                    setStormTrack(null);
                }
            } catch {
                if (!cancelled) {
                    setIsLive(false);
                    setStormFeedAvailable(false);
                    setStorms([]);
                    setStormTrack(null);
                    setLoadError(true);
                }
            } finally {
                running = false;
            }
        };
        const timer = window.setInterval(() => { void refreshLive(); }, 300_000);
        const onVisible = () => {
            if (document.visibilityState === "visible") void refreshLive();
        };
        document.addEventListener("visibilitychange", onVisible);
        return () => {
            cancelled = true;
            window.clearInterval(timer);
            document.removeEventListener("visibilitychange", onVisible);
        };
    }, [isDemoMode, isInitialLoading, selectedStormId]);

    useEffect(() => {
        localStorage.setItem("typhoon-language", lang);
        document.documentElement.lang = lang;
    }, [lang]);

    // 3. Sync Theme Class with <html> tag
    useEffect(() => {
        const root = document.documentElement;
        localStorage.setItem("typhoon-theme", isDark ? "dark" : "light");
        if (isDark) {
            root.classList.add("dark");
            root.classList.remove("light");
        } else {
            root.classList.add("light");
            root.classList.remove("dark");
        }
    }, [isDark]);

    // Selected storm object
    const currentStorm = useMemo(() => {
        return storms.find((s) => s.id === selectedStormId) || storms[0];
    }, [storms, selectedStormId]);

    // Active observation / forecast point according to scrubber
    const rawFix = useMemo((): Fix | undefined => {
        if (
            !stormTrack ||
            !stormTrack.observations ||
            stormTrack.observations.length === 0
        ) {
            return currentStorm?.latest;
        }
        if (currentFixIndex < stormTrack.observations.length) {
            return stormTrack.observations[currentFixIndex];
        }
        // If in forecast frame
        const forecastIdx = currentFixIndex - stormTrack.observations.length;
        if (stormTrack.forecast && stormTrack.forecast.points[forecastIdx]) {
            const p = stormTrack.forecast.points[forecastIdx];
            return {
                timestamp: p.valid_time,
                lat: p.lat,
                lon: p.lon,
                // The model forecasts position and class only; never invent values.
                wind_ms: p.wind_ms ?? null,
                pressure_hpa: p.pressure_hpa ?? null,
                intensity: (p.intensity as Fix["intensity"]) || "UNK",
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
            speed_kmh: rawFix.speed_kmh ?? Math.round(haversineKm(prev.lat, prev.lon, rawFix.lat, rawFix.lon) / hours),
        };
    }, [rawFix, stormTrack]);

    // Calculate real-time province impacts
    const provinceImpacts: ProvinceImpact[] = useMemo(() => {
        if (!currentFix || provincesGeoJson.length === 0) return [];
        // Listed per current (2025) province, not per old map polygon.
        return impactsByUnit(calculateProvinceImpacts(
            provincesGeoJson,
            currentFix,
            stormTrack?.forecast?.points || [],
        ));
    }, [provincesGeoJson, currentFix, stormTrack]);

    const handleRefresh = useCallback(async () => {
        setLoadError(false);
        setIsDemoMode(false);
        try {
            const { online } = await checkBackendHealth();
            setIsLive(online);
            const active = await fetchActiveTyphoons();
            setStorms(active.typhoons);
            setStormFeedAvailable(active.feedAvailable);
            setIsLive(online && active.isLive && active.feedAvailable);
            const nextStormId = active.typhoons.some(
                (storm) => storm.id === selectedStormId,
            )
                ? selectedStormId
                : "";
            setSelectedStormId(nextStormId);
            setStormTrack(null);
            if (nextStormId) {
                setIsTrackLoading(true);
                const track = await fetchStormTrack(nextStormId);
                setStormTrack(track);
                setCurrentFixIndex(
                    Math.max(0, track.observations.length - 1),
                );
            }
        } catch {
            setStorms([]);
            setSelectedStormId("");
            setStormTrack(null);
            setIsLive(false);
            setStormFeedAvailable(false);
            setLoadError(true);
        } finally {
            setIsTrackLoading(false);
        }
    }, [selectedStormId]);

    // Demo data is opt-in and remains visibly offline.
    const handleLoadDemo = useCallback(async () => {
        // "Demo" now means the hindcast archive of real 2021-2024 storms.
        try {
            const archive = await fetchHindcastIndex();
            setIsDemoMode(true);
            setLoadError(false);
            setStorms(archive);
            setStormTrack(null);
            // Same rule as live mode: nothing is drawn until the user picks a storm.
            setSelectedStormId("");
            setIsLive(false);
        } catch (err) {
            console.warn("Hindcast archive unavailable:", err);
            setLoadError(true);
        }
    }, []);

    // WS1: Show full-page skeleton during initial load
    if (isInitialLoading) {
        return <DashboardSkeleton lang={lang} />;
    }

    return (
        <div className={`weather-app immersive-map ${detailsOpen ? "details-is-open" : ""} flex min-h-screen w-full min-w-0 flex-col overflow-x-hidden text-fg`}>
            <a
                href="#dashboard-main"
                className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-toast focus:rounded-control focus:bg-primary focus:px-4 focus:py-2 focus:font-semibold focus:text-page"
            >
                {lang === "vi"
                    ? "Đi đến nội dung chính"
                    : "Skip to main content"}
            </a>
            {/* 1. Top Navigation Bar */}
            <div className="map-top-chrome" ref={chromeRef}>
            <Header
                lang={lang}
                onToggleLang={() => setLang(lang === "vi" ? "en" : "vi")}
                isDark={isDark}
                onToggleTheme={() => setIsDark(!isDark)}
                isLive={isLive}
                isDemoMode={isDemoMode}
                onToggleDemo={isDemoMode ? handleRefresh : handleLoadDemo}
                onRefresh={handleRefresh}
                onOpenAlerts={() => setIsAlertModalOpen(true)}
            />

            {isDemoMode && (
                <div className="map-connection-row">
                    <div role="status" className="rounded-control border border-warning/35 bg-warning/10 px-3 py-2 text-xs font-semibold text-warning">
                        {lang === "vi"
                            ? "DỰ BÁO LẠI · Bão thật 2021–2024 ảnh hưởng Việt Nam, được mô hình dự báo lại (mô hình chưa thấy các bão này khi huấn luyện). Đường tím: quỹ đạo thực tế. Thời tiết là dữ liệu mẫu."
                            : "HINDCAST · Real 2021–2024 storms affecting Vietnam re-forecast by the model (unseen in training). Violet: actual track. Weather is sample data."}
                    </div>
                </div>
            )}

            {/* WS1: Error Banner when API is offline */}
            {loadError && !isDemoMode && (
                <div className="map-connection-row">
                    <ErrorBanner lang={lang} onRetry={handleRefresh} />
                </div>
            )}

            {/* 3. Tracked Cyclones Strip */}
            {storms.length > 0 && (
                <ActiveStormSelector
                    storms={storms}
                    selectedStormId={selectedStormId}
                    onSelectStorm={(id) => {
                        setStormTrack(null);
                        // Tapping the selected storm again clears the selection.
                        if (id === selectedStormId) {
                            setSelectedStormId("");
                            setDetailsOpen(false);
                            return;
                        }
                        setSelectedStormId(id);
                        selectDetailTab("storm");
                        // Phones: show the track on the map first; the sheet would cover it.
                        setDetailsOpen(window.innerWidth >= 768);
                    }}
                    lang={lang}
                />
            )}

            </div>
            {/* 2. Permanent Legal & Meteorological Disclaimer Banner */}
            <DisclaimerBanner lang={lang} />

            <div className="workspace-heading">
                <div><h2>{lang === "vi" ? "Việt Nam & Biển Đông" : "Vietnam & the East Sea"}<span className="region-badge">GMT+7</span></h2></div>
                <button className="btn-ghost" onClick={() => setDetailsOpen(!detailsOpen)} aria-label={lang === "vi" ? (detailsOpen ? "Ẩn chi tiết" : "Xem chi tiết") : (detailsOpen ? "Hide details" : "Show details")} title={lang === "vi" ? (detailsOpen ? "Ẩn bảng chi tiết" : "Mở bảng chi tiết") : (detailsOpen ? "Hide detail panel" : "Open detail panel")} aria-expanded={detailsOpen} aria-controls="weather-details">{detailsOpen ? <PanelRightClose size={18} aria-hidden="true" /> : <PanelRightOpen size={18} aria-hidden="true" />}<span>{lang === "vi" ? (detailsOpen ? "Ẩn chi tiết" : "Xem chi tiết") : (detailsOpen ? "Hide details" : "Show details")}</span></button>
            </div>

            {/* 4. Main Dashboard Layout */}
            {(
                <main
                    id="dashboard-main"
                    tabIndex={-1}
                    className={`weather-workspace ${detailsOpen ? "" : "details-closed"}`}
                >
                    <section
                        className="map-column"
                        aria-label={t.aria_map_container}
                    >
                        <div className="map-stage">
                            <TyphoonMap
                                observations={stormTrack?.observations || []}
                                currentFixIndex={currentFixIndex}
                                forecast={stormTrack?.forecast || null}
                                actualTrack={isDemoMode ? stormTrack?.actual_track || [] : []}
                                focusLocation={weatherLocations.find((location) => location.id === weatherLocationId) ?? null}
                                weatherConditions={Object.values(mapWeather)}
                                onSelectWeatherLocation={(id) => {
                                    setWeatherLocationId(id);
                                    selectDetailTab("weather");
                                    setDetailsOpen(true);
                                }}
                                selectedProvinceId={selectedProvinceId}
                                onSelectProvince={(id) => {
                                    setSelectedProvinceId(id);
                                    // A province click shows that place's weather (old
                                    // 63-province polygon -> current 34-unit location).
                                    const province = provincesGeoJson.find((f) => f.properties.id === id)?.properties;
                                    if (province) setWeatherLocationId(weatherLocationForProvince(province.name, province.centroid).id);
                                    selectDetailTab("weather");
                                    setDetailsOpen(true);
                                }}
                                lang={lang}
                            />
                            <MapLocationSearch
                                lang={lang}
                                locations={weatherLocations}
                                onSelect={(id) => {
                                    setWeatherLocationId(id);
                                    selectDetailTab("weather");
                                    setDetailsOpen(true);
                                }}
                            />
                            {/* Interactive Map Legend */}
                            <MapLegend
                                lang={lang}
                                showActualComparison={
                                    isDemoMode && Boolean(stormTrack?.actual_track?.length)
                                }
                                showSuggestion={Boolean(stormTrack?.forecast?.suggestion)}
                            />
                        </div>

                        {!stormTrack && <div className="map-caption"><MapPin size={16} aria-hidden="true" /><span>{lang === "vi" ? "Khám phá bản đồ · Chọn địa điểm để xem thời tiết" : "Explore the map · Choose a location for local weather"}</span></div>}
                        {/* Interactive Scrubbing Timeline Player */}
                        {stormTrack && stormTrack.observations && (
                            <TimelinePlayer
                                observations={stormTrack.observations}
                                forecastPoints={
                                    stormTrack.forecast?.points || []
                                }
                                currentIndex={currentFixIndex}
                                onSelectIndex={(idx) => setCurrentFixIndex(idx)}
                                lang={lang}
                            />
                        )}
                    </section>

                    {/* Right Column (5 cols): Metrics, Province Impact, and Forecast Table */}
                    <aside
                        id="weather-details"
                        ref={detailsRef}
                        hidden={!detailsOpen}
                        className="details-panel scroll-area"
                        data-tab={detailTab}
                        aria-label={
                            lang === "vi"
                                ? "Bảng điều khiển thông số bão"
                                : "Storm parameters panel"
                        }
                    >
                        <div className="detail-tabs" role="group" aria-label={lang === "vi" ? "Nội dung chi tiết" : "Detail views"}>
                            {([
                                ["storm", Radar, lang === "vi" ? "Cơn bão" : "Storm", lang === "vi" ? "Bão" : "Storm"],
                                ["weather", CloudSun, lang === "vi" ? "Thời tiết" : "Weather", lang === "vi" ? "Thời tiết" : "Weather"],
                                ["analysis", ChartNoAxesCombined, lang === "vi" ? "Biểu đồ" : "Charts", lang === "vi" ? "Biểu đồ" : "Charts"],
                                ["assistant", Bot, lang === "vi" ? "Hỏi đáp" : "Ask", lang === "vi" ? "Hỏi" : "Ask"],
                            ] as const).map(([id, Icon, label, compactLabel]) => <button key={id} type="button" aria-label={label} aria-pressed={detailTab === id} onClick={() => selectDetailTab(id)}><Icon size={18} aria-hidden="true" /><span className="detail-tab-label">{label}</span><span className="detail-tab-label-compact" aria-hidden="true">{compactLabel}</span></button>)}
                        </div>
                        {/* WS1: Track loading indicator */}
                        {isTrackLoading && (
                            <TrackLoadingIndicator lang={lang} />
                        )}

                        <WeatherPanel
                            lang={lang}
                            locations={weatherLocations}
                            locationId={weatherLocationId}
                            onLocationChange={setWeatherLocationId}
                            current={currentWeather}
                            hourly={hourlyWeather}
                            daily={dailyWeather}
                            loading={weatherLoading}
                            error={weatherError}
                            dataMode={isDemoMode ? "demo" : "live"}
                            stormFeedAvailable={stormFeedAvailable}
                            onLoadDemo={isDemoMode ? undefined : handleLoadDemo}
                        />

                        {detailTab === "assistant" && <OllamaAssistant lang={lang} />}
                        {detailTab === "storm" && storms.length === 0 && <div className="storm-empty-note" role="status"><CloudOff size={18} aria-hidden="true"/><span>{lang === "vi" ? (stormFeedAvailable ? "Hiện không có bão đang hoạt động." : "Chưa kết nối dữ liệu bão trực tuyến.") : (stormFeedAvailable ? "No active storms right now." : "Live storm data is not connected.")}</span><button type="button" onClick={handleLoadDemo}>{lang === "vi" ? "Xem demo" : "View demo"}</button></div>}
                        {detailTab === "analysis" && !stormTrack && <p className="storm-empty-note" role="status">{lang === "vi" ? "Chọn một cơn bão hoặc xem demo để khám phá biểu đồ phân tích." : "Select a storm or view the demo to explore analysis charts."}</p>}

                        {/* A. Storm Core Metrics Overview Card */}
                        {detailTab === "storm" && !isTrackLoading && currentStorm && currentFix && (
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

                        {/* Explainable similar-storm suggestion (k-NN analogs) */}
                        {detailTab === "storm" && !isTrackLoading && stormTrack?.forecast?.suggestion && (
                            <CollapsibleSection
                                id="similar-storms"
                                title={t.suggestion_title}
                                defaultOpen={true}
                                lang={lang}
                            >
                                <SuggestionPanel
                                    suggestion={stormTrack.forecast.suggestion}
                                    hindcast={stormTrack.hindcast}
                                    lang={lang}
                                />
                            </CollapsibleSection>
                        )}

                        {/* Wind & Pressure Chart */}
                        {detailTab === "analysis" && !isTrackLoading &&
                            stormTrack &&
                            stormTrack.observations && (
                                <CollapsibleSection
                                    id="wind-chart"
                                    title={
                                        lang === "vi"
                                            ? "Biểu đồ Gió & Áp suất"
                                            : "Wind & Pressure Chart"
                                    }
                                    defaultOpen={true}
                                    lang={lang}
                                >
                                    <Suspense
                                        fallback={
                                            <div className="panel h-72 p-4">
                                                <div className="skeleton h-full w-full" />
                                            </div>
                                        }
                                    >
                                        <WindPressureChart
                                            observations={
                                                stormTrack.observations
                                            }
                                            forecastPoints={
                                                stormTrack.forecast?.points ||
                                                []
                                            }
                                            currentIndex={currentFixIndex}
                                            lang={lang}
                                        />
                                    </Suspense>
                                </CollapsibleSection>
                            )}

                        {/* B. Province Impact & Proximity Vulnerability Assessment */}
                        {detailTab === "storm" && !isTrackLoading && provinceImpacts.length > 0 && (
                            <CollapsibleSection
                                id="province-impact"
                                title={t.province_impact_title}
                                defaultOpen={true}
                                lang={lang}
                            >
                                <ProvinceImpactPanel
                                    impacts={provinceImpacts}
                                    selectedProvinceId={selectedProvinceId}
                                    onSelectProvince={(id) =>
                                        setSelectedProvinceId(id)
                                    }
                                    lang={lang}
                                />
                            </CollapsibleSection>
                        )}

                        {/* C. Multi-Horizon Numerical Forecast Table */}
                        {detailTab === "analysis" && !isTrackLoading &&
                            stormTrack &&
                            stormTrack.forecast && (
                                <CollapsibleSection
                                    id="forecast-table"
                                    title={t.forecast_table}
                                    defaultOpen={false}
                                    lang={lang}
                                >
                                    <ForecastTable
                                        forecast={stormTrack.forecast}
                                        lang={lang}
                                    />
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
                available={alertsAvailable === true}
                loadingCapability={alertsAvailable === null}
                unavailableReason={alertUnavailableReason}
            />
        </div>
    );
};
