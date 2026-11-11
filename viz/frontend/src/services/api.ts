import {
    ActiveTyphoonItem,
    StormTrackResponse,
    ProvinceImpact,
    SystemHealth,
    SystemVersion,
    Fix,
    ForecastPoint,
    ProvinceGeoFeature,
} from "../types";
const BASE_URL = ""; // Relative path leverages Vite dev proxy & FastAPI static serving

// Session credentials stay in memory, never in localStorage or the built bundle.
let credential: { kind: "key" | "bearer"; value: string } | null = null;

export function clearCredentials(): void { credential = null; }

// One shared request: the map layer and the impact panel both need this large file.
let provincesRequest: Promise<{ type: string; features: ProvinceGeoFeature[] }> | null = null;
export function loadProvincesGeoJson() {
    provincesRequest ??= fetch("/data/vietnam_provinces.geojson").then((response) => {
        if (!response.ok) throw new Error(`Provinces GeoJSON HTTP ${response.status}`);
        return response.json();
    });
    provincesRequest.catch(() => { provincesRequest = null; }); // allow a retry after failure
    return provincesRequest;
}

export function authHeaders(): Record<string, string> {
    if (!credential) return {};
    return credential.kind === "key"
        ? { "X-API-Key": credential.value }
        : { Authorization: `Bearer ${credential.value}` };
}

export async function loginWithKey(key: string): Promise<void> {
    clearCredentials();
    if (!key.trim()) throw new Error("API key không được để trống / API key is required");
    const response = await fetch("/auth/session", {
        headers: { "X-API-Key": key.trim() }, signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) throw new Error(`Đăng nhập thất bại / Login failed (HTTP ${response.status})`);
    const payload = await response.json().catch(() => null);
    if (payload?.authenticated !== true) {
        throw new Error("Máy chủ chưa xác nhận đăng nhập / Authentication was not verified");
    }
    credential = { kind: "key", value: key.trim() };
}

export async function loginWithPassword(username: string, password: string): Promise<void> {
    clearCredentials();
    const response = await fetch("/token", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }), signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) throw new Error(`Đăng nhập thất bại / Login failed (HTTP ${response.status})`);
    const payload = await response.json();
    if (typeof payload.access_token !== "string" || !payload.access_token) {
        throw new Error("Phản hồi đăng nhập không hợp lệ / Invalid login response");
    }
    credential = { kind: "bearer", value: payload.access_token };
}

export interface OllamaChatMessage {
    role: "user" | "assistant";
    content: string;
}

export class DashboardApiError extends Error {
    readonly status?: number;
    readonly cause?: unknown;

    constructor(message: string, status?: number, cause?: unknown) {
        super(message);
        this.name = "DashboardApiError";
        this.status = status;
        this.cause = cause;
    }
}

async function fetchJson(
    path: string,
    label: string,
    timeoutMs: number,
): Promise<unknown> {
    let response: Response;
    try {
        response = await fetch(`${BASE_URL}${path}`, {
            headers: authHeaders(),
            signal: AbortSignal.timeout(timeoutMs),
        });
    } catch (cause) {
        throw new DashboardApiError(
            `Unable to load ${label}: backend is unreachable`,
            undefined,
            cause,
        );
    }

    if (!response.ok) {
        if (response.status === 401) {
            clearCredentials();
            throw new DashboardApiError("Vui lòng đăng nhập bằng nút Đăng nhập / Please sign in", 401);
        }
        throw new DashboardApiError(
            `Unable to load ${label}: API returned HTTP ${response.status}`,
            response.status,
        );
    }

    try {
        return await response.json();
    } catch (cause) {
        throw new DashboardApiError(
            `Unable to load ${label}: API returned invalid JSON`,
            response.status,
            cause,
        );
    }
}

// Calculate Haversine distance in km between two lat/lon pairs
export function haversineKm(
    lat1: number,
    lon1: number,
    lat2: number,
    lon2: number,
): number {
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


export async function fetchWeatherLocations(query=""):Promise<import("../types").WeatherLocation[]> { const res=await fetch(`/api/weather/locations/search?q=${encodeURIComponent(query)}`,{signal:AbortSignal.timeout(4000)}); if(!res.ok) throw new Error(res.status===503?"Nhà cung cấp thời tiết chưa được cấu hình":"Không tải được địa điểm"); return (await res.json()).locations; }
export async function fetchCurrentWeather(locationId:string):Promise<import("../types").CurrentWeather> { const res=await fetch(`/api/weather/current?location_id=${encodeURIComponent(locationId)}`,{signal:AbortSignal.timeout(7000)}); if(!res.ok) throw new Error("Không tải được thời tiết hiện tại"); return res.json(); }
export async function fetchLocalWeather(locationId:string){ const response=await fetch(`/api/weather/bundle?location_id=${encodeURIComponent(locationId)}`,{signal:AbortSignal.timeout(25000)}); if(!response.ok) throw new Error(response.status===429?"Đã vượt hạn mức nhà cung cấp":response.status===503?"Dữ liệu thời tiết tạm thời không khả dụng":"Không tìm thấy dữ liệu thời tiết"); return response.json(); }

export async function askOllama(
    question: string,
    history: OllamaChatMessage[],
    language: "vi" | "en",
): Promise<{ answer: string; model: string }> {
    const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, history, language }),
        signal: AbortSignal.timeout(60000),
    });
    const payload = await response.json().catch(() => null) as {
        answer?: unknown;
        model?: unknown;
        error?: { message?: unknown };
    } | null;
    if (!response.ok) {
        throw new Error(
            typeof payload?.error?.message === "string"
                ? payload.error.message
                : "Trợ lý AI tạm thời không khả dụng.",
        );
    }
    if (typeof payload?.answer !== "string" || typeof payload.model !== "string") {
        throw new Error("Ollama trả về dữ liệu không hợp lệ.");
    }
    return { answer: payload.answer, model: payload.model };
}

// Check if backend API is online
export async function checkBackendHealth(): Promise<{
    online: boolean;
    info?: SystemHealth;
}> {
    try {
        const res = await fetch(`${BASE_URL}/health`, {
            signal: AbortSignal.timeout(12000),
        });
        if (res.ok) {
            const data = await res.json();
            return { online: true, info: data };
        }
        return { online: false };
    } catch {
        return { online: false };
    }
}

// Fetch active typhoons. Demo data is only enabled by an explicit UI action.
export async function fetchActiveTyphoons(): Promise<{
    typhoons: ActiveTyphoonItem[];
    isLive: boolean;
    feedAvailable: boolean;
}> {
    const data = await fetchJson(
        "/typhoons/active?source=jma",
        "active storms",
        15000,
    );
    if (
        typeof data !== "object" ||
        data === null ||
        !("typhoons" in data) ||
        !Array.isArray(data.typhoons)
    ) {
        throw new DashboardApiError(
            "Unable to load active storms: API response is malformed",
        );
    }
    return {
        typhoons: data.typhoons as ActiveTyphoonItem[],
        isLive: true,
        feedAvailable: "feedAvailable" in data && data.feedAvailable === true,
    };
}

// Fetch track and forecast for a given storm. Never substitute another storm.
export async function fetchStormTrack(
    stormId: string,
): Promise<StormTrackResponse> {
    const payload = await fetchJson(
        `/typhoons/${encodeURIComponent(stormId)}/track?source=jma`,
        `track for ${stormId}`,
        20000,
    );
    const data = payload as Partial<StormTrackResponse> | null;
    if (
        typeof data !== "object" ||
        data === null ||
        data.storm_id !== stormId ||
        !Array.isArray(data.observations) ||
        !(data.forecast === null || typeof data.forecast === "object")
    ) {
        throw new DashboardApiError(
            `Unable to load track for ${stormId}: API response is malformed`,
        );
    }
    return data as StormTrackResponse;
}

// Fetch or calculate province impacts against storm track
export function calculateProvinceImpacts(
    provinces: ProvinceGeoFeature[],
    currentFix: Fix,
    forecastPoints: ForecastPoint[] = [],
): ProvinceImpact[] {
    return provinces
        .map((p) => {
            const [pLat, pLon] = p.properties.centroid;
            const currentDist = haversineKm(
                currentFix.lat,
                currentFix.lon,
                pLat,
                pLon,
            );

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
            let impactLevel: "critical" | "high" | "moderate" | "low" | "none" =
                "none";
            if (minDist <= 60) {
                impactLevel = "critical"; // Direct strike / eyewall zone
            } else if (minDist <= 150) {
                impactLevel = "high"; // Gale force winds zone
            } else if (minDist <= 300) {
                impactLevel = "moderate"; // Outer squalls & waves
            } else if (minDist <= 500) {
                impactLevel = "low";
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
        })
        .sort(
            (a, b) => a.min_forecast_distance_km - b.min_forecast_distance_km,
        );
}
