import React, { useEffect, useRef, useState, useMemo } from 'react';
import L from 'leaflet';
import { Fix, ForecastResponse } from '../../types';
import { Language, translations } from '../../i18n';
import { MOCK_OFFICIAL_COMPARISON } from '../../services/mockData';
import { Eye, Compass } from 'lucide-react';

interface TyphoonMapProps {
  observations: Fix[];
  currentFixIndex: number;
  forecast: ForecastResponse | null;
  selectedProvinceId: string | null;
  onSelectProvince: (id: string) => void;
  lang: Language;
}

export const TyphoonMap: React.FC<TyphoonMapProps> = ({
  observations,
  currentFixIndex,
  forecast,
  selectedProvinceId,
  onSelectProvince,
  lang,
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  // Layer groups refs
  const baseTileRef = useRef<L.TileLayer | null>(null);
  const provincesLayerRef = useRef<L.GeoJSON | null>(null);
  const islandsLayerRef = useRef<L.LayerGroup | null>(null);
  const trackLayerRef = useRef<L.LayerGroup | null>(null);
  const coneLayerRef = useRef<L.LayerGroup | null>(null);
  const compareLayerRef = useRef<L.LayerGroup | null>(null);

  // WS6: Separate ref for the active cyclone marker — avoids full layer rebuild on scrub
  const cycloneMarkerRef = useRef<L.Marker | null>(null);
  const currentFixMarkerRef = useRef<L.CircleMarker | null>(null);
  const prevFixIndexRef = useRef<number>(-1);

  // State for toggles
  const [basemapType, setBasemapType] = useState<'dark' | 'osm' | 'sat'>('dark');
  const [showCone, setShowCone] = useState(true);
  const [showCompare, setShowCompare] = useState(true);
  const [islandsData, setIslandsData] = useState<any[]>([]);

  const t = translations[lang];

  // Memoize observation/forecast identity to avoid unnecessary rebuilds
  const observationsKey = useMemo(() => {
    if (!observations || observations.length === 0) return '';
    return observations.map((o) => `${o.lat},${o.lon}`).join('|');
  }, [observations]);

  const forecastKey = useMemo(() => {
    if (!forecast || !forecast.points) return '';
    return forecast.forecast_id + forecast.points.length;
  }, [forecast]);

  // 1. Load Islands metadata
  useEffect(() => {
    fetch('/data/vietnam_islands.json')
      .then((res) => res.json())
      .then((data) => setIslandsData(data))
      .catch((err) => console.warn('Failed to load islands data:', err));
  }, []);

  // 2. Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    // Center on Vietnam and East Sea (Biển Đông)
    const map = L.map(mapContainerRef.current, {
      center: [16.5, 110.0],
      zoom: 6,
      minZoom: 4,
      maxZoom: 15,
      zoomControl: false,
    });

    L.control.zoom({ position: 'topright' }).addTo(map);

    // Default tile: CartoDB Dark Matter
    baseTileRef.current = L.tileLayer(
      'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 19,
      }
    ).addTo(map);

    // Create layer groups
    provincesLayerRef.current = L.geoJSON(undefined, {
      style: {
        color: '#0284c7',
        weight: 1.2,
        opacity: 0.6,
        fillColor: '#0369a1',
        fillOpacity: 0.08,
      },
    }).addTo(map);

    islandsLayerRef.current = L.layerGroup().addTo(map);
    coneLayerRef.current = L.layerGroup().addTo(map);
    compareLayerRef.current = L.layerGroup().addTo(map);
    trackLayerRef.current = L.layerGroup().addTo(map);

    mapInstanceRef.current = map;

    // Load Vietnam provinces GeoJSON
    fetch('/data/vietnam_provinces.geojson')
      .then((r) => r.json())
      .then((geojson) => {
        if (!mapInstanceRef.current) return;
        provincesLayerRef.current?.clearLayers();
        provincesLayerRef.current?.addData(geojson);

        provincesLayerRef.current?.eachLayer((layer: any) => {
          const props = layer.feature?.properties;
          if (props) {
            layer.bindTooltip(props.name, {
              permanent: false,
              direction: 'center',
              className: 'bg-slate-900/90 text-cyan-200 text-xs px-2 py-1 rounded border border-cyan-500/40 font-mono',
            });
            layer.on('click', () => {
              onSelectProvince(props.id);
            });
          }
        });
      })
      .catch((e) => console.warn('Could not load provinces GeoJSON:', e));

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // 3. Update Basemap Tile
  useEffect(() => {
    if (!mapInstanceRef.current || !baseTileRef.current) return;

    mapInstanceRef.current.removeLayer(baseTileRef.current);

    let url = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
    let attr = '&copy; OpenStreetMap &copy; CARTO';

    if (basemapType === 'osm') {
      url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      attr = '&copy; OpenStreetMap contributors';
    } else if (basemapType === 'sat') {
      url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
      attr = '&copy; Esri World Imagery';
    }

    baseTileRef.current = L.tileLayer(url, { attribution: attr, maxZoom: 18 }).addTo(mapInstanceRef.current);
    baseTileRef.current.bringToBack();
  }, [basemapType]);

  // 4. Update Sovereign Islands (Hoàng Sa & Trường Sa)
  useEffect(() => {
    if (!mapInstanceRef.current || !islandsLayerRef.current) return;
    const group = islandsLayerRef.current;
    group.clearLayers();

    islandsData.forEach((island) => {
      // Create territorial zone circle
      const circle = L.circle([island.lat, island.lon], {
        radius: island.radius_km * 1000,
        color: '#f59e0b',
        weight: 1,
        dashArray: '4, 4',
        fillColor: '#f59e0b',
        fillOpacity: 0.05,
      });

      // Permanent island marker & label
      const islandIcon = L.divIcon({
        className: 'island-label-marker',
        html: `
          <div class="flex flex-col items-center pointer-events-auto cursor-pointer">
            <div class="w-3 h-3 rounded-full bg-amber-400 border-2 border-slate-900 shadow-md"></div>
            <div class="bg-slate-950/90 text-amber-300 text-[11px] font-bold px-2 py-0.5 rounded border border-amber-500/50 shadow-lg whitespace-nowrap mt-1 font-display">
              🇻🇳 ${lang === 'vi' ? island.name_vi : island.name_en}
            </div>
            <div class="text-[9px] text-slate-300 font-mono bg-slate-900/80 px-1 rounded">
              ${island.sovereignty}
            </div>
          </div>
        `,
        iconSize: [160, 45],
        iconAnchor: [80, 10],
      });

      const marker = L.marker([island.lat, island.lon], { icon: islandIcon });
      circle.addTo(group);
      marker.addTo(group);
    });
  }, [islandsData, lang]);

  // 5. Update Province Selection Highlights
  useEffect(() => {
    if (!provincesLayerRef.current) return;

    provincesLayerRef.current.setStyle((feature: any) => {
      const isSelected = feature.properties.id === selectedProvinceId;
      return {
        color: isSelected ? '#f43f5e' : '#0284c7',
        weight: isSelected ? 2.5 : 1.2,
        opacity: isSelected ? 0.9 : 0.6,
        fillColor: isSelected ? '#f43f5e' : '#0369a1',
        fillOpacity: isSelected ? 0.25 : 0.08,
      };
    });
  }, [selectedProvinceId]);

  // 6. WS6 OPTIMIZED: Rebuild tracks + forecast ONLY when data changes (not on scrub)
  useEffect(() => {
    if (!mapInstanceRef.current || !trackLayerRef.current || !coneLayerRef.current) return;
    const trackGroup = trackLayerRef.current;
    const coneGroup = coneLayerRef.current;
    const compareGroup = compareLayerRef.current;

    trackGroup.clearLayers();
    coneGroup.clearLayers();
    compareGroup?.clearLayers();

    // Clean up previous cyclone marker
    if (cycloneMarkerRef.current && mapInstanceRef.current) {
      mapInstanceRef.current.removeLayer(cycloneMarkerRef.current);
      cycloneMarkerRef.current = null;
    }
    currentFixMarkerRef.current = null;
    prevFixIndexRef.current = -1;

    if (!observations || observations.length === 0) return;

    // A. Actual Track Polyline & Fix Markers
    const obsCoords: L.LatLngExpression[] = observations.map((o) => [o.lat, o.lon]);
    const actualPolyline = L.polyline(obsCoords, {
      color: '#10b981',
      weight: 3.5,
      opacity: 0.9,
    });
    actualPolyline.addTo(trackGroup);

    // Add observation point markers (all same size — active highlight handled in effect #7)
    observations.forEach((obs) => {
      const marker = L.circleMarker([obs.lat, obs.lon], {
        radius: 4.5,
        color: '#047857',
        weight: 1.5,
        fillColor: '#34d399',
        fillOpacity: 0.9,
      });

      marker.bindPopup(`
        <div class="text-xs font-mono p-1">
          <div class="font-bold text-emerald-400 font-display text-sm">${t.legend_actual}</div>
          <div><strong>${t.popup_time}:</strong> ${new Date(obs.timestamp).toLocaleString()}</div>
          <div><strong>${t.popup_coords}:</strong> ${obs.lat}°${lang === 'vi' ? 'B' : 'N'}, ${obs.lon}°${lang === 'vi' ? 'Đ' : 'E'}</div>
          <div><strong>${t.popup_pressure}:</strong> ${obs.pressure_hpa || 'N/A'} hPa</div>
          <div><strong>${t.popup_wind}:</strong> ${obs.wind_kmh || (obs.wind_ms ? Math.round(obs.wind_ms * 3.6) : 'N/A')} km/h</div>
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
        ...forecast.points.map((p) => [p.lat, p.lon] as L.LatLngExpression),
      ];

      const forecastPolyline = L.polyline(fcCoords, {
        color: '#f59e0b',
        weight: 3,
        dashArray: '6, 6',
        opacity: 0.9,
      });
      forecastPolyline.addTo(trackGroup);

      // Forecast point markers
      forecast.points.forEach((p) => {
        const pMarker = L.circleMarker([p.lat, p.lon], {
          radius: 5,
          color: '#b45309',
          weight: 1.5,
          fillColor: '#f59e0b',
          fillOpacity: 0.9,
        });

        pMarker.bindPopup(`
          <div class="text-xs font-mono p-1">
            <div class="font-bold text-amber-400 font-display text-sm">${t.popup_forecast_prefix} +${p.horizon_hours} ${t.eta_hours_suffix}</div>
            <div><strong>${t.popup_valid_time}:</strong> ${new Date(p.valid_time).toLocaleString()}</div>
            <div><strong>${t.popup_coords}:</strong> ${p.lat}°${lang === 'vi' ? 'B' : 'N'}, ${p.lon}°${lang === 'vi' ? 'Đ' : 'E'}</div>
            <div><strong>${t.popup_wind}:</strong> ${p.wind_ms ? Math.round(p.wind_ms * 3.6) : 'N/A'} km/h</div>
            <div><strong>${t.popup_cone_radius}:</strong> ±${p.radius_km} km</div>
          </div>
        `);
        pMarker.addTo(trackGroup);

        // C. Cone of uncertainty polygons
        if (showCone && p.cone && p.cone.coordinates) {
          const coneLatLngs = p.cone.coordinates[0].map((coord) => [coord[1], coord[0]] as L.LatLngExpression);
          const conePolygon = L.polygon(coneLatLngs, {
            color: '#06b6d4',
            weight: 1.2,
            opacity: 0.7,
            fillColor: '#06b6d4',
            fillOpacity: 0.12,
            dashArray: '3, 3',
          });
          conePolygon.addTo(coneGroup);
        }
      });
    }

    // D. S10 Official Forecast Comparison
    if (showCompare && compareGroup) {
      const compareCoords: L.LatLngExpression[] = MOCK_OFFICIAL_COMPARISON.map(
        (c) => [c.lat, c.lon] as L.LatLngExpression
      );
      const compareLine = L.polyline(compareCoords, {
        color: '#c084fc',
        weight: 2.5,
        dashArray: '3, 6',
        opacity: 0.8,
      });
      compareLine.addTo(compareGroup);

      MOCK_OFFICIAL_COMPARISON.forEach((c) => {
        const marker = L.circleMarker([c.lat, c.lon], {
          radius: 4,
          color: '#a855f7',
          weight: 1,
          fillColor: '#c084fc',
          fillOpacity: 0.8,
        });
        marker.bindPopup(`
          <div class="text-xs font-mono p-1">
            <div class="font-bold text-purple-400">${t.popup_nchmf_official}</div>
            <div>${t.popup_forecast_hour} +${c.horizon_hours}h</div>
            <div>${t.popup_coords}: ${c.lat}°${lang === 'vi' ? 'B' : 'N'}, ${c.lon}°${lang === 'vi' ? 'Đ' : 'E'}</div>
          </div>
        `);
        marker.addTo(compareGroup);
      });
    }
  // WS6: Only rebuild when data/toggles change — NOT on currentFixIndex
  }, [observationsKey, forecastKey, showCone, showCompare, lang]);

  // 7. WS6 OPTIMIZED: Update ONLY the active cyclone marker position on scrub
  useEffect(() => {
    if (!mapInstanceRef.current || !observations || observations.length === 0) return;
    if (currentFixIndex === prevFixIndexRef.current) return;

    prevFixIndexRef.current = currentFixIndex;

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

    if (!lat && !lon) return;

    // Move existing cyclone marker or create new one
    if (cycloneMarkerRef.current) {
      cycloneMarkerRef.current.setLatLng([lat, lon]);
    } else {
      const cycloneIcon = L.divIcon({
        className: 'cyclone-active-marker',
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

      cycloneMarkerRef.current = L.marker([lat, lon], {
        icon: cycloneIcon,
        zIndexOffset: 1000,
      }).addTo(mapInstanceRef.current);
    }
  }, [currentFixIndex, observations, forecast]);

  return (
    <div className="relative w-full h-full min-h-[450px] rounded-xl overflow-hidden border border-slate-800 shadow-2xl">
      {/* Map Container */}
      <div
        ref={mapContainerRef}
        className="w-full h-full"
        role="application"
        aria-label={t.aria_map_container}
      />

      {/* Top Map Layer Controls Toolbar */}
      <div className="absolute top-4 left-4 z-[1000] flex flex-wrap items-center gap-2 bg-slate-900/90 backdrop-blur-md p-1.5 rounded-xl border border-slate-700/60 shadow-xl">
        {/* Basemap Switcher */}
        <div className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-lg text-xs font-mono" role="radiogroup" aria-label={t.basemap}>
          <button
            onClick={() => setBasemapType('dark')}
            role="radio"
            aria-checked={basemapType === 'dark'}
            className={`px-2 py-1 rounded transition focus-ring ${
              basemapType === 'dark' ? 'bg-cyan-600 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            {t.basemap_dark}
          </button>
          <button
            onClick={() => setBasemapType('osm')}
            role="radio"
            aria-checked={basemapType === 'osm'}
            className={`px-2 py-1 rounded transition focus-ring ${
              basemapType === 'osm' ? 'bg-cyan-600 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            OSM
          </button>
          <button
            onClick={() => setBasemapType('sat')}
            role="radio"
            aria-checked={basemapType === 'sat'}
            className={`px-2 py-1 rounded transition focus-ring ${
              basemapType === 'sat' ? 'bg-cyan-600 text-white font-bold' : 'text-slate-400 hover:text-white'
            }`}
          >
            Satellite
          </button>
        </div>

        {/* Cone Toggle */}
        <button
          onClick={() => setShowCone(!showCone)}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono border transition focus-ring ${
            showCone
              ? 'bg-cyan-950 text-cyan-300 border-cyan-500/50'
              : 'bg-slate-800/80 text-slate-400 border-slate-700'
          }`}
          aria-pressed={showCone}
          aria-label={t.layer_cone}
        >
          <Eye className="w-3 h-3" aria-hidden="true" />
          <span className="hidden sm:inline">{lang === 'vi' ? 'Nón bất định' : 'Cone'}</span>
        </button>

        {/* S10 Official Comparison Toggle */}
        <button
          onClick={() => setShowCompare(!showCompare)}
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-mono border transition focus-ring ${
            showCompare
              ? 'bg-purple-950 text-purple-300 border-purple-500/50'
              : 'bg-slate-800/80 text-slate-400 border-slate-700'
          }`}
          aria-pressed={showCompare}
          aria-label={t.layer_official_compare}
        >
          <Compass className="w-3 h-3" aria-hidden="true" />
          <span className="hidden sm:inline">{lang === 'vi' ? 'So sánh NCHMF' : 'Compare NCHMF'}</span>
        </button>
      </div>
    </div>
  );
};
