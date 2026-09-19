import {
  ActiveTyphoonItem,
  StormTrackResponse,
  ProvinceImpact,
  SystemHealth,
  SystemVersion,
  Fix,
} from '../types';
import {
  MOCK_STORMS_LIST,
  MOCK_TRACK_YAGI,
  MOCK_TRACK_SIM,
} from './mockData';

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

// Fetch active typhoons (with automatic mock fallback)
export async function fetchActiveTyphoons(): Promise<{
  typhoons: ActiveTyphoonItem[];
  isLive: boolean;
}> {
  try {
    const res = await fetch(`${BASE_URL}/typhoons/active`, { signal: AbortSignal.timeout(2000) });
    if (res.ok) {
      const data = await res.json();
      if (data.typhoons && data.typhoons.length > 0) {
        return { typhoons: data.typhoons, isLive: true };
      }
    }
  } catch (err) {
    console.warn('Backend unavailable, using realistic mock typhoons:', err);
  }

  // Fallback to mock active storms
  return { typhoons: MOCK_STORMS_LIST, isLive: false };
}

// Fetch track and forecast for a given storm
export async function fetchStormTrack(stormId: string): Promise<StormTrackResponse> {
  try {
    const res = await fetch(`${BASE_URL}/typhoons/${stormId}/track`, { signal: AbortSignal.timeout(2500) });
    if (res.ok) {
      const data = await res.json();
      return data;
    }
  } catch (err) {
    console.warn(`Backend /track failed for ${stormId}, returning mock track:`, err);
  }

  // Fallback mock track matching ID
  if (stormId === 'WP112024') {
    return MOCK_TRACK_YAGI;
  }
  return MOCK_TRACK_SIM;
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
