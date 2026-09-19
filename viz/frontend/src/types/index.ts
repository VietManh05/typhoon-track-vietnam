export type IntensityClass = 'TD' | 'TS' | 'STS' | 'TY' | 'STY' | 'SUPERTY' | 'UNK';

export interface Fix {
  timestamp: string; // ISO-8601 UTC
  lat: number;
  lon: number;
  wind_ms: number | null;
  pressure_hpa: number | null;
  intensity: IntensityClass;
  source: string;
  source_url?: string | null;
  // Computed helpers for display
  wind_kmh?: number;
  wind_knot?: number;
  beaufort_level?: number;
  bearing_deg?: number;
  speed_kmh?: number;
}

export interface ForecastPoint {
  horizon_hours: number;
  valid_time: string; // ISO-8601 UTC
  lat: number;
  lon: number;
  intensity: IntensityClass | string;
  radius_km: number;
  cone: {
    type: 'Polygon';
    coordinates: number[][][]; // [lon, lat]
  };
  wind_ms?: number;
  pressure_hpa?: number;
}

export interface ForecastResponse {
  forecast_id: string;
  storm_id: string;
  issue_time: string;
  generated_at: string;
  model_version: string;
  model_kind: string;
  dataset_version: string;
  sources: string[];
  uncertainty_method: string;
  warnings: string[];
  disclaimer: string;
  points: ForecastPoint[];
}

export interface ActiveTyphoonItem {
  id: string;
  name: string;
  name_vi?: string;
  year?: number;
  latest: Fix;
  observation_count: number;
  status?: 'active' | 'watch' | 'dissipated';
}

export interface ActiveTyphoonsResponse {
  typhoons: ActiveTyphoonItem[];
  disclaimer: string;
}

export interface StormTrackResponse {
  storm_id: string;
  observations: Fix[];
  forecast: ForecastResponse | null;
}

export interface ProvinceImpact {
  id: string;
  name: string;
  centroid: [number, number]; // [lat, lon]
  current_distance_km: number;
  min_forecast_distance_km: number;
  closest_horizon_hours: number;
  closest_valid_time: string;
  eta_hours: number;
  within_cone: boolean;
  impact_level: 'critical' | 'high' | 'moderate' | 'low' | 'none';
  wind_threat_level?: string;
}

export interface SystemVersion {
  version: string;
  model_version: string;
  model_kind: string;
  dataset_version: string;
}

export interface SystemHealth {
  status: string;
  environment: string;
}
