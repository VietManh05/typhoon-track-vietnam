import React, { useEffect, useRef, useState, useMemo } from "react";
import L from "leaflet";
import leafletStylesheetUrl from "leaflet/dist/leaflet.css?url";
import {
    CurrentWeather,
    Fix,
    ForecastResponse,
    VerificationPoint,
    WeatherLocation,
} from "../../types";
import { Language, translations } from "../../i18n";
import { VIETNAM_WEATHER_LOCATIONS, fold } from "../../data/vietnamLocations";
import { sweptCone } from "../../lib/cone";

// Label-free basemaps: OSM/OpenTopoMap print neighbours in Thai/Chinese and name
// Hoàng Sa in Chinese, so the map carries only our own Vietnamese labels.
const ESRI = "https://server.arcgisonline.com/ArcGIS/rest/services";
const BASEMAPS = {
    dark: { url: `${ESRI}/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}`, attr: "&copy; Esri, GEBCO, NOAA", native: 13 },
    osm: { url: `${ESRI}/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}`, attr: "&copy; Esri", native: 13 },
    sat: { url: `${ESRI}/World_Imagery/MapServer/tile/{z}/{y}/{x}`, attr: "&copy; Esri World Imagery", native: 18 },
} as const;

// Vietnamese names for the region; sea name per Vietnamese usage.
const REGION_LABELS: Array<[number, number, string, string, "country" | "sea"]> = [
    [19.6, 102.6, "Lào", "Laos", "country"],
    [12.8, 104.9, "Campuchia", "Cambodia", "country"],
    [15.6, 100.9, "Thái Lan", "Thailand", "country"],
    [24.3, 108.8, "Trung Quốc", "China", "country"],
    [13.2, 122.6, "Philippines", "Philippines", "country"],
    [12.6, 113.2, "Biển Đông", "East Sea", "sea"],
    [18.8, 107.3, "Vịnh Bắc Bộ", "Gulf of Tonkin", "sea"],
    [11.2, 101.5, "Vịnh Thái Lan", "Gulf of Thailand", "sea"],
];
import {
    ChevronDown,
    Eye,
    Layers3,
    LocateFixed,
    Maximize2,
    Minus,
    Plus,
} from "lucide-react";
import {
    initializeWindyMap,
    WindyApi,
    WindyOverlay,
} from "../../services/windyMap";

const WINDY_API_KEY = import.meta.env.VITE_WINDY_MAP_API_KEY?.trim() ?? "";
const LEAFLET_STYLESHEET_ID = "leaflet-fallback-stylesheet";

function ensureLeafletStylesheet() {
    if (document.getElementById(LEAFLET_STYLESHEET_ID)) return;
    const link = document.createElement("link");
    link.id = LEAFLET_STYLESHEET_ID;
    link.rel = "stylesheet";
    link.href = leafletStylesheetUrl;
    document.head.appendChild(link);
}

interface TyphoonMapProps {
    observations: Fix[];
    currentFixIndex: number;
    forecast: ForecastResponse | null;
    actualTrack?: VerificationPoint[];
    selectedProvinceId: string | null;
    onSelectProvince: (id: string) => void;
    lang: Language;
    focusLocation?: WeatherLocation | null;
    weatherConditions?: CurrentWeather[];
    onSelectWeatherLocation?: (id: string) => void;
}

const weatherMarkerSvg = (icon: string) => {
    if (icon.includes("rain") || icon.includes("shower")) {
        return '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M9 21h14a6 6 0 0 0 0-12 8 8 0 0 0-15-1A6.5 6.5 0 0 0 9 21Z" fill="#e8f4ff" stroke="#5b7896" stroke-width="1.5"/><path d="m11 24-2 4m8-4-2 4m8-4-2 4" stroke="#2296d2" stroke-width="2" stroke-linecap="round"/></svg>';
    }
    if (icon.includes("cloud") || icon.includes("overcast")) {
        return '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="11" cy="10" r="6" fill="#ffc64b"/><path d="M8 24h16a6 6 0 0 0-1-12 8 8 0 0 0-15 2A5 5 0 0 0 8 24Z" fill="#eef6fb" stroke="#6b8297" stroke-width="1.5"/></svg>';
    }
    if (icon.includes("storm") || icon.includes("thunder")) {
        return '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M8 20h16a6 6 0 0 0-1-12 8 8 0 0 0-15 2A5 5 0 0 0 8 20Z" fill="#dfeaf2" stroke="#60778c" stroke-width="1.5"/><path d="m17 19-5 8h5l-2 5 7-9h-5l2-4Z" fill="#ffb020"/></svg>';
    }
    return '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="7" fill="#ffc43d"/><g stroke="#e99b17" stroke-width="2" stroke-linecap="round"><path d="M16 3v4m0 18v4M3 16h4m18 0h4M7 7l3 3m12 12 3 3M25 7l-3 3M10 22l-3 3"/></g></svg>';
};

export const TyphoonMap: React.FC<TyphoonMapProps> = ({
    observations,
    currentFixIndex,
    forecast,
    actualTrack = [],
    selectedProvinceId,
    onSelectProvince,
    lang,
    focusLocation,
    weatherConditions = [],
    onSelectWeatherLocation,
}) => {
    const mapContainerRef = useRef<HTMLDivElement>(null);
    const mapShellRef = useRef<HTMLDivElement>(null);
    const mapInstanceRef = useRef<L.Map | null>(null);
    const leafletApiRef = useRef<typeof L>(L);
    const windyApiRef = useRef<WindyApi | null>(null);

    // Layer groups refs
    const baseTileRef = useRef<L.TileLayer | null>(null);
    const provincesLayerRef = useRef<L.GeoJSON | null>(null);
    const islandsLayerRef = useRef<L.LayerGroup | null>(null);
    const trackLayerRef = useRef<L.LayerGroup | null>(null);
    const coneLayerRef = useRef<L.LayerGroup | null>(null);
    const compareLayerRef = useRef<L.LayerGroup | null>(null);
    const weatherLayerRef = useRef<L.LayerGroup | null>(null);
    const placeLabelsRef = useRef<L.LayerGroup | null>(null);
    // Province click handlers are bound once at map init; read the latest callback.
    const onSelectProvinceRef = useRef(onSelectProvince);
    onSelectProvinceRef.current = onSelectProvince;

    // WS6: Separate ref for the active cyclone marker — avoids full layer rebuild on scrub
    const cycloneMarkerRef = useRef<L.Marker | null>(null);

    // State for toggles
    const [basemapType, setBasemapType] = useState<"dark" | "osm" | "sat">(
        "dark",
    );
    const [showCone, setShowCone] = useState(true);
    const [controlsOpen, setControlsOpen] = useState(false);
    const [zoomLevel, setZoomLevel] = useState(6);
    const [islandsData, setIslandsData] = useState<any[]>([]);
    // Province polygon centroids keyed by folded name, for label placement.
    const [provinceCentroids, setProvinceCentroids] = useState<Record<string, [number, number]>>({});
    const [mapReady, setMapReady] = useState(false);
    const [mapProvider, setMapProvider] = useState<"loading" | "windy" | "leaflet">(
        WINDY_API_KEY ? "loading" : "leaflet",
    );
    const [windyOverlay, setWindyOverlay] = useState<WindyOverlay>("wind");
    const [windyError, setWindyError] = useState<string | null>(null);

    const t = translations[lang];
    const closeMapControls = () => setControlsOpen(false);
    const activeLayerLabel = mapProvider === "windy"
        ? ({ wind: lang === "vi" ? "Gió" : "Wind", temp: lang === "vi" ? "Nhiệt độ" : "Temperature", pressure: lang === "vi" ? "Áp suất" : "Pressure" }[windyOverlay])
        : mapProvider === "loading"
            ? (lang === "vi" ? "Đang tải" : "Loading")
            : ({ dark: lang === "vi" ? "Bản đồ" : "Map", osm: lang === "vi" ? "Địa hình" : "Terrain", sat: lang === "vi" ? "Vệ tinh" : "Satellite" }[basemapType]);

    // Memoize observation/forecast identity to avoid unnecessary rebuilds
    const observationsKey = useMemo(() => {
        if (!observations || observations.length === 0) return "";
        return observations.map((o) => `${o.lat},${o.lon}`).join("|");
    }, [observations]);

    const forecastKey = useMemo(() => {
        if (!forecast || !forecast.points) return "";
        return forecast.forecast_id + forecast.points.length;
    }, [forecast]);

    const actualTrackKey = useMemo(
        () => actualTrack.map((point) => `${point.lat},${point.lon},${point.valid_time}`).join("|"),
        [actualTrack],
    );

    // 1. Load Islands metadata
    useEffect(() => {
        fetch("/data/vietnam_islands.json")
            .then((res) => res.json())
            .then((data) => setIslandsData(data))
            .catch((err) => console.warn("Failed to load islands data:", err));
    }, []);

    useEffect(() => {
        const desktop = window.matchMedia("(min-width: 768px)");
        const syncControls = (event: MediaQueryListEvent) =>
            setControlsOpen(event.matches);
        desktop.addEventListener("change", syncControls);
        return () => desktop.removeEventListener("change", syncControls);
    }, []);

    // 2. Initialize Windy Map Forecast when configured, with Leaflet fallback.
    useEffect(() => {
        if (!mapContainerRef.current || mapInstanceRef.current) return;
        let cancelled = false;

        const finishInitialization = (
            map: L.Map,
            leaflet: typeof L,
            provider: "windy" | "leaflet",
        ) => {
            if (cancelled) {
                map.remove();
                return;
            }

            leafletApiRef.current = leaflet;
            mapInstanceRef.current = map;
            map.setMinZoom(4);
            map.setMaxZoom(15);
            map.on("zoomend", () => setZoomLevel(map.getZoom()));

            provincesLayerRef.current = leaflet.geoJSON(undefined, {
                style: {
                    color: "#7c8ea3",
                    weight: 0.8,
                    opacity: 0.86,
                    fillColor: "#ffffff",
                    fillOpacity: 0.06,
                },
            }).addTo(map);
            placeLabelsRef.current = leaflet.layerGroup().addTo(map);
            islandsLayerRef.current = leaflet.layerGroup().addTo(map);
            coneLayerRef.current = leaflet.layerGroup().addTo(map);
            compareLayerRef.current = leaflet.layerGroup().addTo(map);
            trackLayerRef.current = leaflet.layerGroup().addTo(map);
            weatherLayerRef.current = leaflet.layerGroup().addTo(map);

            setMapProvider(provider);
            setMapReady(true);

            fetch("/data/vietnam_provinces.geojson")
                .then((response) => response.json())
                .then((geojson) => {
                    if (cancelled || !mapInstanceRef.current) return;
                    provincesLayerRef.current?.clearLayers();
                    provincesLayerRef.current?.addData(geojson);
                    setProvinceCentroids(Object.fromEntries(
                        (geojson.features ?? []).map((f: any) => [fold(String(f.properties?.name ?? "")), f.properties?.centroid]),
                    ));
                    provincesLayerRef.current?.eachLayer((layer: any) => {
                        const props = layer.feature?.properties;
                        if (!props) return;
                        layer.bindTooltip(String(props.name).replace(/(\p{Ll})(\p{Lu})/gu, "$1 $2"), {
                            permanent: false,
                            direction: "center",
                            className: "tvn-tooltip",
                        });
                        layer.on("click", () => onSelectProvinceRef.current(props.id));
                    });
                })
                .catch((error) =>
                    console.warn("Could not load provinces GeoJSON:", error),
                );
        };

        const initializeFallback = () => {
            if (!mapContainerRef.current || cancelled) return;
            ensureLeafletStylesheet();
            mapContainerRef.current.replaceChildren();
            delete (mapContainerRef.current as HTMLDivElement & { _leaflet_id?: number })
                ._leaflet_id;
            const map = L.map(mapContainerRef.current, {
                center: [16.5, 110.0],
                zoom: 6,
                minZoom: 4,
                maxZoom: 15,
                zoomControl: false,
            });
            baseTileRef.current = L.tileLayer(BASEMAPS.dark.url, {
                attribution: BASEMAPS.dark.attr,
                maxNativeZoom: BASEMAPS.dark.native,
                maxZoom: 19,
            }).addTo(map);
            finishInitialization(map, L, "leaflet");
        };

        const initialize = async () => {
            if (!WINDY_API_KEY) {
                initializeFallback();
                return;
            }

            try {
                const { api, leaflet } = await initializeWindyMap(WINDY_API_KEY, {
                    lat: 16.5,
                    lon: 110,
                    zoom: 6,
                    overlay: "wind",
                    level: "surface",
                    particlesAnim: "on",
                    hourFormat: "24h",
                    lang,
                    verbose: false,
                });
                if (cancelled) {
                    api.map.remove();
                    return;
                }
                windyApiRef.current = api;
                finishInitialization(api.map, leaflet, "windy");
            } catch (error) {
                console.warn("Windy Map Forecast unavailable; using Leaflet:", error);
                setWindyError(error instanceof Error ? error.message : "Windy unavailable");
                initializeFallback();
            }
        };

        // Avoid a duplicate third-party initialization during StrictMode's
        // development-only effect probe.
        const timer = window.setTimeout(() => void initialize(), 0);

        return () => {
            cancelled = true;
            window.clearTimeout(timer);
            mapInstanceRef.current?.remove();
            mapInstanceRef.current = null;
            windyApiRef.current = null;
            baseTileRef.current = null;
            provincesLayerRef.current = null;
            islandsLayerRef.current = null;
            coneLayerRef.current = null;
            compareLayerRef.current = null;
            trackLayerRef.current = null;
            weatherLayerRef.current = null;
            cycloneMarkerRef.current = null;
        };
    }, []);

    // Vietnamese place labels drawn by us (the basemap has none).
    const showProvinceNames = zoomLevel >= 7;
    useEffect(() => {
        const leaflet = leafletApiRef.current;
        const layer = placeLabelsRef.current;
        if (!mapReady || !leaflet || !layer) return;
        layer.clearLayers();
        const label = (lat: number, lon: number, text: string, kind: string, anchorY = 10) =>
            leaflet.marker([lat, lon], {
                interactive: false,
                keyboard: false,
                icon: leaflet.divIcon({
                    className: `place-label place-label-${kind}`,
                    html: `<span>${text}</span>`,
                    iconSize: [160, 22],
                    iconAnchor: [80, anchorY],
                }),
            }).addTo(layer);
        for (const [lat, lon, vi, en, kind] of REGION_LABELS) label(lat, lon, lang === "vi" ? vi : en, kind);
        if (showProvinceNames) {
            // Sit below the weather bubble that shares the same point.
            for (const place of VIETNAM_WEATHER_LOCATIONS) {
                // Label at the province's area centre, not its capital: capitals
                // such as Vinh sit on a border and read as the neighbour's name.
                const centre = provinceCentroids[fold(place.name)];
                // Near the capital the weather bubble would cover it: sit below the bubble.
                const nearBubble = !centre || Math.hypot(centre[0] - place.latitude, centre[1] - place.longitude) < 0.35;
                if (nearBubble) label(place.latitude, place.longitude, place.name, "province", -24);
                else label(centre[0], centre[1], place.name, "province");
            }
        }
    }, [mapReady, lang, showProvinceNames, provinceCentroids]);

    useEffect(() => {
        if (!focusLocation || !mapInstanceRef.current) return;
        const map = mapInstanceRef.current;
        map.setView([focusLocation.latitude, focusLocation.longitude], 7, { animate: !window.matchMedia("(prefers-reduced-motion: reduce)").matches });
    }, [focusLocation, mapReady]);

    // Picking a storm brings it into view (track + forecast); scrubbing the
    // timeline keeps the same track, so the view does not jump.
    useEffect(() => {
        const map = mapInstanceRef.current;
        if (!map || !mapReady || !observationsKey) return;
        const points: L.LatLngTuple[] = [
            ...observations.map((o) => [o.lat, o.lon] as L.LatLngTuple),
            ...(forecast?.points ?? []).map((p) => [p.lat, p.lon] as L.LatLngTuple),
        ];
        map.fitBounds(L.latLngBounds(points), {
            // Keep the storm clear of the header (top) and timeline (bottom).
            paddingTopLeft: [80, 180],
            paddingBottomRight: [100, 170],
            maxZoom: 7,
            animate: !window.matchMedia("(prefers-reduced-motion: reduce)").matches,
        });
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [observationsKey, forecastKey, mapReady]);

    useEffect(() => {
        if (!mapReady || !weatherLayerRef.current) return;
        const leaflet = leafletApiRef.current;
        const layer = weatherLayerRef.current;
        const map = mapInstanceRef.current;
        if (!map) return;
        layer.clearLayers();

        // Keep nearby weather chips from covering each other at regional zooms.
        const placed: Array<{ x: number; y: number }> = [];
        const prioritized = [...weatherConditions].sort((a, b) =>
            Number(b.location.id === focusLocation?.id) - Number(a.location.id === focusLocation?.id),
        );
        prioritized.forEach((weather) => {
            const selected = weather.location.id === focusLocation?.id;
            const point = map.latLngToContainerPoint([weather.location.latitude, weather.location.longitude]);
            if (!selected && placed.some((other) =>
                Math.abs(other.x - point.x) < 70 && Math.abs(other.y - point.y) < 48,
            )) return;
            placed.push(point);
            const label = `${weather.location.name}: ${Math.round(weather.temperatureC)}°, ${weather.condition.label}`;
            const marker = leaflet.marker(
                [weather.location.latitude, weather.location.longitude],
                {
                    title: label,
                    alt: label,
                    icon: leaflet.divIcon({
                        className: "weather-map-marker",
                        html: `<div class="weather-marker-card${selected ? " is-selected" : ""}">${weatherMarkerSvg(weather.condition.icon)}<strong>${Math.round(weather.temperatureC)}°</strong></div>`,
                        iconSize: [58, 38],
                        iconAnchor: [29, 19],
                    }),
                    keyboard: true,
                },
            ).addTo(layer);
            marker.bindTooltip(label, {
                direction: "top",
                offset: [0, -18],
                className: "tvn-tooltip weather-tooltip",
            });
            marker.on("click", () => onSelectWeatherLocation?.(weather.location.id));
        });
    }, [focusLocation?.id, mapReady, onSelectWeatherLocation, weatherConditions, zoomLevel]);

    useEffect(() => {
        if (!mapContainerRef.current) return;
        const observer = new ResizeObserver(() => mapInstanceRef.current?.invalidateSize());
        observer.observe(mapContainerRef.current);
        return () => observer.disconnect();
    }, []);

    useEffect(() => {
        const resizeMap = () =>
            window.setTimeout(
                () => mapInstanceRef.current?.invalidateSize(),
                80,
            );
        document.addEventListener("fullscreenchange", resizeMap);
        window.addEventListener("resize", resizeMap, { passive: true });
        return () => {
            document.removeEventListener("fullscreenchange", resizeMap);
            window.removeEventListener("resize", resizeMap);
        };
    }, []);

    // 3. Update Basemap Tile
    useEffect(() => {
        if (mapProvider !== "leaflet" || !mapInstanceRef.current || !baseTileRef.current) return;

        mapInstanceRef.current.removeLayer(baseTileRef.current);

        const base = BASEMAPS[basemapType];
        baseTileRef.current = L.tileLayer(base.url, {
            attribution: base.attr,
            maxNativeZoom: base.native,
            maxZoom: 19,
        }).addTo(mapInstanceRef.current);
        baseTileRef.current.bringToBack();
    }, [basemapType, mapProvider, mapReady]);

    useEffect(() => {
        if (mapProvider !== "windy" || !windyApiRef.current) return;
        windyApiRef.current.store.set("overlay", windyOverlay);
        windyApiRef.current.store.set(
            "particlesAnim",
            windyOverlay === "wind" ? "on" : "off",
        );
    }, [mapProvider, windyOverlay]);

    useEffect(() => {
        if (mapProvider !== "windy" || !windyApiRef.current) return;
        windyApiRef.current.store.set("lang", lang);
    }, [lang, mapProvider]);

    // 4. Update Sovereign Islands (Hoàng Sa & Trường Sa)
    useEffect(() => {
        if (!mapInstanceRef.current || !islandsLayerRef.current) return;
        const leaflet = leafletApiRef.current;
        const group = islandsLayerRef.current;
        group.clearLayers();

        islandsData.forEach((island) => {
            const isArchipelago = island.id === "hoang_sa" || island.id === "truong_sa";
            const markerColor = isArchipelago ? "#f43f5e" : "#f59e0b";
            // Create territorial zone circle
            const circle = leaflet.circle([island.lat, island.lon], {
                radius: island.radius_km * 1000,
                color: markerColor,
                weight: isArchipelago ? 2 : 1,
                dashArray: "4, 4",
                fillColor: markerColor,
                fillOpacity: isArchipelago ? 0.08 : 0.05,
            });

            // Permanent island marker & label
            const islandIcon = leaflet.divIcon({
                className: "island-label-marker",
                html: `
          <div class="flex flex-col items-center pointer-events-auto cursor-pointer">
            <div class="${isArchipelago ? "sovereign-island-symbol" : "ordinary-island-symbol"}" aria-hidden="true">${isArchipelago ? "★" : ""}</div>
            <div class="${isArchipelago ? "sovereign-island-label" : "ordinary-island-label"}">
              ${lang === "vi" ? island.name_vi : island.name_en}
            </div>
            <div class="island-owner-label">
              ${island.sovereignty}
            </div>
          </div>
        `,
                iconSize: [160, 45],
                iconAnchor: [80, 10],
            });

            const marker = leaflet.marker([island.lat, island.lon], {
                icon: islandIcon,
                title: lang === "vi" ? island.name_vi : island.name_en,
            });
            circle.addTo(group);
            marker.addTo(group);
        });
    }, [islandsData, lang, mapReady]);

    // 5. Update Province Selection Highlights
    useEffect(() => {
        if (!provincesLayerRef.current) return;

        provincesLayerRef.current.setStyle((feature: any) => {
            const isSelected = feature.properties.id === selectedProvinceId;
            return {
                color: isSelected ? "#0063cc" : "#7c8ea3",
                weight: isSelected ? 3 : 0.8,
                opacity: isSelected ? 0.9 : 0.6,
                fillColor: isSelected ? "#3b8fe8" : "#ffffff",
                fillOpacity: isSelected ? 0.22 : 0.06,
            };
        });
    }, [selectedProvinceId, mapReady]);

    // 6. WS6 OPTIMIZED: Rebuild tracks + forecast ONLY when data changes (not on scrub)
    useEffect(() => {
        if (
            !mapInstanceRef.current ||
            !trackLayerRef.current ||
            !coneLayerRef.current
        )
            return;
        const trackGroup = trackLayerRef.current;
        const coneGroup = coneLayerRef.current;
        const compareGroup = compareLayerRef.current;
        const leaflet = leafletApiRef.current;

        trackGroup.clearLayers();
        coneGroup.clearLayers();
        compareGroup?.clearLayers();

        if (!observations || observations.length === 0) return;

        // A. Actual Track Polyline & Fix Markers
        const obsCoords: L.LatLngExpression[] = observations.map((o) => [
            o.lat,
            o.lon,
        ]);
        const actualPolyline = leaflet.polyline(obsCoords, {
            color: "#10b981",
            weight: 3.5,
            opacity: 0.9,
        });
        actualPolyline.addTo(trackGroup);

        // Add observation point markers (all same size — active highlight handled in effect #7)
        observations.forEach((obs) => {
            const marker = leaflet.circleMarker([obs.lat, obs.lon], {
                radius: 4.5,
                color: "#047857",
                weight: 1.5,
                fillColor: "#34d399",
                fillOpacity: 0.9,
            });

            marker.bindPopup(`
        <div class="text-xs font-mono p-1">
          <div class="font-bold text-emerald-400 font-display text-sm">${t.legend_actual}</div>
          <div><strong>${t.popup_time}:</strong> ${new Date(obs.timestamp).toLocaleString()}</div>
          <div><strong>${t.popup_coords}:</strong> ${obs.lat}°${lang === "vi" ? "B" : "N"}, ${obs.lon}°${lang === "vi" ? "Đ" : "E"}</div>
          <div><strong>${t.popup_pressure}:</strong> ${obs.pressure_hpa || "N/A"} hPa</div>
          <div><strong>${t.popup_wind}:</strong> ${obs.wind_kmh || (obs.wind_ms ? Math.round(obs.wind_ms * 3.6) : "N/A")} km/h</div>
          <div><strong>${t.popup_category}:</strong> ${obs.intensity}</div>
        </div>
      `);

            marker.addTo(trackGroup);
        });

        // B. Forecast Track & Points
        if (forecast && forecast.points && forecast.points.length > 0) {
            const lastObs = observations[observations.length - 1];
            const fcCoords: L.LatLngExpression[] = [
                [lastObs.lat, lastObs.lon],
                ...forecast.points.map(
                    (p) => [p.lat, p.lon] as L.LatLngExpression,
                ),
            ];

            const forecastPolyline = leaflet.polyline(fcCoords, {
                color: "#f59e0b",
                weight: 3,
                dashArray: "6, 6",
                opacity: 0.9,
            });
            forecastPolyline.addTo(trackGroup);

            // Forecast point markers
            forecast.points.forEach((p) => {
                const pMarker = leaflet.circleMarker([p.lat, p.lon], {
                    radius: 5,
                    color: "#b45309",
                    weight: 1.5,
                    fillColor: "#f59e0b",
                    fillOpacity: 0.9,
                });

                pMarker.bindPopup(`
          <div class="text-xs font-mono p-1">
            <div class="font-bold text-amber-400 font-display text-sm">${t.popup_forecast_prefix} +${p.horizon_hours} ${t.eta_hours_suffix}</div>
            <div><strong>${t.popup_valid_time}:</strong> ${new Date(p.valid_time).toLocaleString()}</div>
            <div><strong>${t.popup_coords}:</strong> ${p.lat}°${lang === "vi" ? "B" : "N"}, ${p.lon}°${lang === "vi" ? "Đ" : "E"}</div>
            <div><strong>${t.popup_wind}:</strong> ${p.wind_ms ? Math.round(p.wind_ms * 3.6) : "N/A"} km/h</div>
            <div><strong>${t.popup_cone_radius}:</strong> ±${p.radius_km} km</div>
          </div>
        `);
                pMarker.addTo(trackGroup);
            });

            // C. One swept cone along the track (NHC/Windy style), starting
            // narrow at the current centre and widening with lead time.
            if (showCone) {
                const firstRadius = forecast.points[0].radius_km;
                const { rings, outline } = sweptCone([
                    { lat: lastObs.lat, lon: lastObs.lon, radiusKm: Math.max(10, firstRadius / 3) },
                    ...forecast.points.map((p) => ({ lat: p.lat, lon: p.lon, radiusKm: p.radius_km })),
                ]);
                if (rings.length) {
                    leaflet.polygon(rings, {
                        stroke: false,
                        fillColor: "#fb923c",
                        fillOpacity: 0.16,
                        fillRule: "nonzero",
                        interactive: false,
                    }).addTo(coneGroup);
                    leaflet.polyline(outline, {
                        color: "#ea580c",
                        weight: 2,
                        opacity: 0.9,
                        dashArray: "6, 6",
                        interactive: false,
                    }).addTo(coneGroup);
                }
            }
        }

        // C. Demo/backtest verification track. It is kept separate from the
        // pre-issue observations so users can compare forecast vs outcome.
        if (compareGroup && actualTrack.length > 0) {
            const lastObs = observations[observations.length - 1];
            const actualCoords: L.LatLngExpression[] = [
                [lastObs.lat, lastObs.lon],
                ...actualTrack.map(
                    (point) => [point.lat, point.lon] as L.LatLngExpression,
                ),
            ];
            leaflet.polyline(actualCoords, {
                color: "#8b5cf6",
                weight: 3.5,
                opacity: 0.95,
            }).addTo(compareGroup);

            actualTrack.forEach((point) => {
                const marker = leaflet.circleMarker([point.lat, point.lon], {
                    radius: 4.5,
                    color: "#6d28d9",
                    weight: 1.5,
                    fillColor: "#a78bfa",
                    fillOpacity: 0.95,
                });
                marker.bindPopup(`
          <div class="text-xs font-mono p-1">
            <div class="font-bold text-violet-400 font-display text-sm">${lang === "vi" ? "Thực tế kiểm chứng" : "Verified actual track"} +${point.horizon_hours} ${t.eta_hours_suffix}</div>
            <div><strong>${t.popup_valid_time}:</strong> ${new Date(point.valid_time).toLocaleString()}</div>
            <div><strong>${t.popup_coords}:</strong> ${point.lat}°${lang === "vi" ? "B" : "N"}, ${point.lon}°${lang === "vi" ? "Đ" : "E"}</div>
            <div><strong>${lang === "vi" ? "Nguồn" : "Source"}:</strong> ${point.source}</div>
          </div>
        `);
                marker.addTo(compareGroup);
            });
        }

        // D. Explainable k-NN analog suggestion (what similar past storms did next).
        const suggestion = forecast?.suggestion;
        if (compareGroup && suggestion && suggestion.points.length > 0 && observations.length > 0) {
            const lastObs = observations[observations.length - 1];
            const analogNames = suggestion.analogs.map((a) => `${a.name} ${a.year}`).join(", ");
            leaflet.polyline(
                [
                    [lastObs.lat, lastObs.lon] as L.LatLngExpression,
                    ...suggestion.points.map((p) => [p.lat, p.lon] as L.LatLngExpression),
                ],
                { color: "#f472b6", weight: 3, dashArray: "2, 7", opacity: 0.95 },
            ).addTo(compareGroup);
            suggestion.points.forEach((p) => {
                leaflet.circleMarker([p.lat, p.lon], {
                    radius: 4,
                    color: "#be185d",
                    weight: 1.5,
                    fillColor: "#f9a8d4",
                    fillOpacity: 0.95,
                })
                    .bindPopup(`
          <div class="text-xs font-mono p-1">
            <div class="font-bold text-pink-400 font-display text-sm">${t.suggestion_title} +${p.horizon_hours} ${t.eta_hours_suffix}</div>
            <div><strong>${t.popup_coords}:</strong> ${p.lat.toFixed(1)}°${lang === "vi" ? "B" : "N"}, ${p.lon.toFixed(1)}°${lang === "vi" ? "Đ" : "E"}</div>
            <div><strong>${lang === "vi" ? "Bão tương tự" : "Similar storms"}:</strong> ${analogNames}</div>
          </div>
        `)
                    .addTo(compareGroup);
            });
        }

        // Demo verification coordinates are explicitly labelled sample/best-track.
        // WS6: Only rebuild when data/toggles change — NOT on currentFixIndex
    }, [observationsKey, forecastKey, actualTrackKey, showCone, lang, mapReady]);

    // 7. WS6 OPTIMIZED: Update ONLY the active cyclone marker position on scrub
    useEffect(() => {
        if (!mapInstanceRef.current) return;
        if (!observations || observations.length === 0) {
            cycloneMarkerRef.current?.remove();
            cycloneMarkerRef.current = null;
            return;
        }

        const isForecast = currentFixIndex >= observations.length;
        let lat = 0;
        let lon = 0;

        if (isForecast && forecast?.points) {
            const fp = forecast.points[currentFixIndex - observations.length];
            if (fp) {
                lat = fp.lat;
                lon = fp.lon;
            }
        } else if (observations[currentFixIndex]) {
            lat = observations[currentFixIndex].lat;
            lon = observations[currentFixIndex].lon;
        }

        if (!lat && !lon) {
            cycloneMarkerRef.current?.remove();
            cycloneMarkerRef.current = null;
            return;
        }
        const leaflet = leafletApiRef.current;

        // Move existing cyclone marker or create new one
        if (cycloneMarkerRef.current) {
            cycloneMarkerRef.current.setLatLng([lat, lon]);
        } else {
            const cycloneIcon = leaflet.divIcon({
                className: "cyclone-active-marker",
                html: `
          <div class="relative flex items-center justify-center w-12 h-12">
            <div class="absolute w-12 h-12 rounded-full bg-rose-500/30 pulse-ring-effect"></div>
            <div class="w-8 h-8 rounded-full bg-slate-950/80 border-2 border-rose-500 flex items-center justify-center shadow-lg shadow-rose-500/40">
              <svg class="w-5 h-5 text-rose-400 animate-spin-slow" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8 2 4 6 4 12C4 16.5 7 20 11.5 21.8C10 19.5 9.5 16 11.5 13.5C13.5 11 16.5 10.5 18 12.5C18.8 8 16 3 12 2Z"/>
                <path d="M12 22C16 22 20 18 20 12C20 7.5 17 4 12.5 2.2C14 4.5 14.5 8 12.5 10.5C10.5 13 7.5 13.5 6 11.5C5.2 16 8 21 12 22Z"/>
              </svg>
            </div>
          </div>
        `,
                iconSize: [48, 48],
                iconAnchor: [24, 24],
            });

            cycloneMarkerRef.current = leaflet.marker([lat, lon], {
                icon: cycloneIcon,
                zIndexOffset: 1000,
                // Accessible name for the focusable marker (screen readers, tooltip).
                title: lang === "vi" ? "Vị trí tâm bão hiện tại" : "Current storm centre",
            }).addTo(mapInstanceRef.current);
        }
    }, [currentFixIndex, observations, forecast, mapReady, lang]);

    return (
        <div
            ref={mapShellRef}
            data-basemap={basemapType}
            data-map-provider={mapProvider}
            className="typhoon-map-shell relative w-full overflow-hidden border border-line bg-surface"
        >
            {/* Map Container */}
            <div
                id="windy"
                ref={mapContainerRef}
                className="w-full h-full"
                style={{ backgroundColor: "rgb(var(--c-bg))" }}
                role="application"
                aria-label={t.aria_map_container}
            />

            {/* Top Map Layer Controls Toolbar */}
            <div className={`map-layer-toolbar map-overlay absolute left-3 top-3 z-[1000] flex max-w-[calc(100%-4.5rem)] flex-wrap items-center gap-1.5 p-1.5 ${controlsOpen ? "is-open" : ""}`}>
                <button
                    type="button"
                    className="map-toolbar-toggle focus-ring"
                    aria-expanded={controlsOpen}
                    aria-controls="map-toolbar-content"
                    onClick={() => setControlsOpen((open) => !open)}
                >
                    <Layers3 className="h-4 w-4" aria-hidden="true" />
                    <span>{activeLayerLabel}</span>
                    <ChevronDown
                        className={`h-4 w-4 transition-transform ${controlsOpen ? "rotate-180" : ""}`}
                        aria-hidden="true"
                    />
                </button>
                <div
                    id="map-toolbar-content"
                    className="map-toolbar-content"
                    hidden={!controlsOpen}
                >
                {mapProvider === "windy" ? (
                    <div
                        className="segmented font-mono"
                        role="radiogroup"
                        aria-label={lang === "vi" ? "Lớp dự báo Windy" : "Windy forecast overlay"}
                    >
                        {(["wind", "temp", "pressure"] as WindyOverlay[]).map((overlay) => {
                            const labels: Record<WindyOverlay, [string, string]> = {
                                wind: ["Gió", "Wind"],
                                temp: ["Nhiệt độ", "Temperature"],
                                pressure: ["Áp suất", "Pressure"],
                            };
                            return (
                                <button
                                    key={overlay}
                                    onClick={() => {
                                        setWindyOverlay(overlay);
                                        closeMapControls();
                                    }}
                                    role="radio"
                                    aria-checked={windyOverlay === overlay}
                                    className={`segmented-item focus-ring ${windyOverlay === overlay ? "segmented-item-active" : ""}`}
                                >
                                    {labels[overlay][lang === "vi" ? 0 : 1]}
                                </button>
                            );
                        })}
                    </div>
                ) : mapProvider === "loading" ? (
                    <span className="map-provider-badge" role="status">
                        {lang === "vi" ? "Đang tải Windy…" : "Loading Windy…"}
                    </span>
                ) : (
                    <div
                        className="segmented font-mono"
                        role="radiogroup"
                        aria-label={t.basemap}
                    >
                        <button
                            onClick={() => {
                                setBasemapType("dark");
                                closeMapControls();
                            }}
                            role="radio"
                            aria-checked={basemapType === "dark"}
                            className={`segmented-item focus-ring ${basemapType === "dark" ? "segmented-item-active" : ""}`}
                        >
                            {lang === "vi" ? "Bản đồ" : "Map"}
                        </button>
                        <button
                            onClick={() => {
                                setBasemapType("osm");
                                closeMapControls();
                            }}
                            role="radio"
                            aria-checked={basemapType === "osm"}
                            className={`segmented-item focus-ring ${basemapType === "osm" ? "segmented-item-active" : ""}`}
                        >
                            {lang === "vi" ? "Địa hình" : "Terrain"}
                        </button>
                        <button
                            onClick={() => {
                                setBasemapType("sat");
                                closeMapControls();
                            }}
                            role="radio"
                            aria-checked={basemapType === "sat"}
                            className={`segmented-item focus-ring ${basemapType === "sat" ? "segmented-item-active" : ""}`}
                        >
                            {lang === "vi" ? "Vệ tinh" : "Satellite"}
                        </button>
                    </div>
                )}

                {Boolean(forecast?.points?.length) && (
                    <button
                        onClick={() => {
                            setShowCone(!showCone);
                            closeMapControls();
                        }}
                        className={`chip min-h-8 px-2.5 font-mono focus-ring ${
                            showCone
                                ? "border-primary/50 bg-primary/10 text-primary"
                                : ""
                        }`}
                        aria-pressed={showCone}
                        aria-label={t.layer_cone}
                    >
                        <Eye className="w-3 h-3" aria-hidden="true" />
                        <span>{lang === "vi" ? "Vùng bão" : "Storm area"}</span>
                    </button>
                )}
                </div>
            </div>

            {windyError && mapProvider === "leaflet" && (
                <div
                    className="map-provider-warning map-overlay"
                    role="status"
                    title={windyError}
                >
                    {lang === "vi"
                        ? "Windy chưa khả dụng · đang dùng bản đồ dự phòng"
                        : "Windy unavailable · using fallback map"}
                </div>
            )}

            <div className="map-navigation absolute right-3 top-24 z-[1000] flex flex-col gap-1.5">
                <div className="map-zoom-group" role="group" aria-label={lang === "vi" ? "Thu phóng bản đồ" : "Map zoom"}>
                    <button type="button" className="map-zoom-button" disabled={zoomLevel >= 15} onClick={() => mapInstanceRef.current?.zoomIn()} aria-label={lang === "vi" ? "Phóng to bản đồ" : "Zoom in"} title={lang === "vi" ? "Phóng to bản đồ" : "Zoom in"}><Plus size={24} aria-hidden="true" /></button>
                    <button type="button" className="map-zoom-button" disabled={zoomLevel <= 4} onClick={() => mapInstanceRef.current?.zoomOut()} aria-label={lang === "vi" ? "Thu nhỏ bản đồ" : "Zoom out"} title={lang === "vi" ? "Thu nhỏ bản đồ" : "Zoom out"}><Minus size={24} aria-hidden="true" /></button>
                </div>
                <button
                    className="map-reset-button btn-icon bg-surface/90 shadow-overlay backdrop-blur-sm"
                    onClick={() =>
                        mapInstanceRef.current?.setView([16.5, 110], 6, {
                            animate: true,
                        })
                    }
                    aria-label={
                        lang === "vi"
                            ? "Đặt lại góc nhìn bản đồ"
                            : "Reset map view"
                    }
                    title={lang === "vi" ? "Đặt lại góc nhìn" : "Reset view"}
                >
                    <LocateFixed className="h-4 w-4" aria-hidden="true" />
                </button>
                <button
                    className="map-fullscreen-button btn-icon bg-surface/90 shadow-overlay backdrop-blur-sm"
                    onClick={() => {
                        if (document.fullscreenElement) void document.exitFullscreen().catch(() => {});
                        else void mapShellRef.current?.requestFullscreen?.().catch(() => {});
                    }}
                    aria-label={
                        lang === "vi"
                            ? "Mở bản đồ toàn màn hình"
                            : "Open fullscreen map"
                    }
                    title={lang === "vi" ? "Toàn màn hình" : "Fullscreen"}
                >
                    <Maximize2 className="h-4 w-4" aria-hidden="true" />
                </button>
            </div>
        </div>
    );
};
