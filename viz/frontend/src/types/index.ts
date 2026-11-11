export type IntensityClass =
    | "TD"
    | "TS"
    | "STS"
    | "TY"
    | "STY"
    | "SUPERTY"
    | "UNK";

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
        type: "Polygon";
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
    status?: "active" | "watch" | "dissipated";
}

export interface ActiveTyphoonsResponse {
    typhoons: ActiveTyphoonItem[];
    disclaimer: string;
}

export interface VerificationPoint {
    horizon_hours: number;
    valid_time: string;
    lat: number;
    lon: number;
    intensity?: IntensityClass | string;
    wind_ms?: number | null;
    pressure_hpa?: number | null;
    source: string;
}

export interface StormTrackResponse {
    storm_id: string;
    observations: Fix[];
    forecast: ForecastResponse | null;
    /** Demo/backtest only: observed best-track points after the forecast issue time. */
    actual_track?: VerificationPoint[];
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
    impact_level: "critical" | "high" | "moderate" | "low" | "none";
    wind_threat_level?: string;
}

export interface ProvinceGeoFeature {
    type: "Feature";
    properties: {
        id: string;
        name: string;
        centroid: [number, number];
        [key: string]: unknown;
    };
    geometry: {
        type: string;
        coordinates: unknown;
    };
}

export interface SystemVersion {
    version: string;
    model_version: string;
    model_revision?: string;
    model_kind: string;
    dataset_version: string;
}


export interface WeatherLocation { id:string; name:string; province:string; country:string; latitude:number; longitude:number; timezone:string; providerLocationId?:string|null; aliases?:string[] }
export interface WeatherMetadata { source:string; provider:string; retrievedAt:string; timezone:string; locationId:string; sourceUrl?:string|null; isStale:boolean }
export interface WeatherCondition { code:string; label:string; icon:string }
export interface WeatherWind { speedKmh:number; gustKmh?:number|null; directionDeg?:number|null; directionLabel?:string|null }
export interface WeatherPrecipitation { probabilityPercent?:number|null; rainMm?:number|null }
export interface CurrentWeather { location:WeatherLocation; observationTime:string; temperatureC:number; feelsLikeC?:number|null; condition:WeatherCondition; humidityPercent?:number|null; wind:WeatherWind; pressureHpa?:number|null; visibilityKm?:number|null; dewPointC?:number|null; cloudCoverPercent?:number|null; uvIndex?:number|null; precipitation:WeatherPrecipitation; airQualityIndex?:number|null; metadata:WeatherMetadata }
export interface HourlyWeather { forecastTime:string; temperatureC:number; feelsLikeC?:number|null; condition:WeatherCondition; precipitation:WeatherPrecipitation; humidityPercent?:number|null; wind:WeatherWind; pressureHpa?:number|null; uvIndex?:number|null; metadata:WeatherMetadata }
export interface DailyWeather { forecastDate:string; minTemperatureC:number; maxTemperatureC:number; condition:WeatherCondition; precipitation:WeatherPrecipitation; wind:WeatherWind; sunrise?:string|null; sunset?:string|null; metadata:WeatherMetadata }

export interface SystemHealth {
    status: string;
    environment: string;
}
