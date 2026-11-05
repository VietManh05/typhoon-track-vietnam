import {
  ActiveTyphoonItem,
  StormTrackResponse,
  ProvinceImpact,
  SystemHealth,
  Fix,
} from '../types';

const BASE_URL = ''; // Relative path leverages Vite dev proxy & FastAPI static serving

// Calculate Haversine distance in km between two lat/lon pairs
export function haversineKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const R = 6371.0088; // Earth radius in km
  const dLat = ((lat2 - lat1) * Math.PI) / 180.0;
  const dLon = ((lon2 - lon1) * Math.PI) / 180.0;
  const a =
    Math.sin(dLat / 2.0) * Math.sin(dLat / 2.0) +
    Math.cos((lat1 * Math.PI) / 180.0) *
      Math.cos((lat2 * Math.PI) / 180.0) *
      Math.sin(dLon / 2.0) *
      Math.sin(dLon / 2.0);
  const c = 2.0 * Math.atan2(Math.sqrt(a), Math.sqrt(1.0 - a));
  return Math.round(R * c * 10) / 10;
}

// Initial great-circle bearing in degrees (0 = north, clockwise)
export function bearingDeg(lat1: number, lon1: number, lat2: number, lon2: number): number {
  const toRad = Math.PI / 180;
  const dLon = (lon2 - lon1) * toRad;
  const y = Math.sin(dLon) * Math.cos(lat2 * toRad);
  const x =
    Math.cos(lat1 * toRad) * Math.sin(lat2 * toRad) -
    Math.sin(lat1 * toRad) * Math.cos(lat2 * toRad) * Math.cos(dLon);
  return Math.round(((Math.atan2(y, x) / toRad) + 360) % 360);
}

// Check if backend API is online
export async function checkBackendHealth(): Promise<{ online: boolean; info?: SystemHealth }> {
  try {
    const res = await fetch(`${BASE_URL}/health`, { signal: AbortSignal.timeout(1500) });
    if (res.ok) {
      const data = await res.json();
      return { online: true, info: data };
    }
    return { online: false };
  } catch {
    return { online: false };
  }
}

/**
 * Fetch active typhoons from the backend. Never substitutes demo data: an
 * empty list means "no active storms", and failures are reported as offline.
 */
export async function fetchActiveTyphoons(): Promise<{
  typhoons: ActiveTyphoonItem[];
  online: boolean;
}> {
  try {
    const res = await fetch(`${BASE_URL}/typhoons/active`, { signal: AbortSignal.timeout(2000) });
    if (res.ok) {
      const data = await res.json();
      return { typhoons: Array.isArray(data.typhoons) ? data.typhoons : [], online: true };
    }
    console.warn(`/typhoons/active returned HTTP ${res.status}`);
  } catch (err) {
    console.warn('Backend unavailable:', err);
  }
  return { typhoons: [], online: false };
}

// Fetch observed track and model forecast for a storm; throws on failure.
export async function fetchStormTrack(stormId: string): Promise<StormTrackResponse> {
  const res = await fetch(`${BASE_URL}/typhoons/${encodeURIComponent(stormId)}/track`, {
    signal: AbortSignal.timeout(5000),
  });
  if (!res.ok) {
    throw new Error(`/typhoons/${stormId}/track returned HTTP ${res.status}`);
  }
  return res.json();
}

// Fetch or calculate province impacts against storm track
export function calculateProvinceImpacts(
  provinces: any[],
  currentFix: Fix,
  forecastPoints: any[] = []
): ProvinceImpact[] {
  return provinces.map((p) => {
    const [pLat, pLon] = p.properties.centroid;
    const currentDist = haversineKm(currentFix.lat, currentFix.lon, pLat, pLon);

    let minDist = currentDist;
    let closestHorizon = 0;
    let closestValidTime = currentFix.timestamp;
    let withinCone = false;

    // Check against all forecast points
    for (const fp of forecastPoints) {
      const dist = haversineKm(fp.lat, fp.lon, pLat, pLon);
      if (dist < minDist) {
        minDist = dist;
        closestHorizon = fp.horizon_hours;
        closestValidTime = fp.valid_time;
      }
      if (dist <= fp.radius_km) {
        withinCone = true;
      }
    }

    // Determine impact category
    let impactLevel: 'critical' | 'high' | 'moderate' | 'low' | 'none' = 'none';
    if (minDist <= 60) {
      impactLevel = 'critical'; // Direct strike / eyewall zone
    } else if (minDist <= 150) {
      impactLevel = 'high'; // Gale force winds zone
    } else if (minDist <= 300) {
      impactLevel = 'moderate'; // Outer squalls & waves
    } else if (minDist <= 500) {
      impactLevel = 'low';
    }

    return {
      id: p.properties.id,
      name: p.properties.name,
      centroid: [pLat, pLon] as [number, number],
      current_distance_km: currentDist,
      min_forecast_distance_km: Math.round(minDist),
      closest_horizon_hours: closestHorizon,
      closest_valid_time: closestValidTime,
      eta_hours: closestHorizon,
      within_cone: withinCone,
      impact_level: impactLevel,
    };
  }).sort((a, b) => a.min_forecast_distance_km - b.min_forecast_distance_km);
}
