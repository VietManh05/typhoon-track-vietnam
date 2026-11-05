const MAX_RESPONSE_BYTES = 1_000_000;

function originFor(env, pageUrl) {
    const value = env?.TYPHOON_BACKEND_URL?.trim();
    if (!value) return null;
    let origin;
    try {
        origin = new URL(value);
    } catch {
        return null;
    }
    const local = ["127.0.0.1", "localhost", "[::1]"].includes(origin.hostname);
    if (origin.protocol !== "https:" && !(origin.protocol === "http:" && local)) {
        return null;
    }
    if (origin.username || origin.password || origin.search || origin.hash || origin.pathname !== "/") {
        return null;
    }
    if (origin.host === new URL(pageUrl).host) return null;
    return origin;
}

export function backendConfigured(env, pageUrl) {
    return originFor(env, pageUrl) !== null;
}

export async function backendJson(env, pageUrl, path, options = {}) {
    const origin = originFor(env, pageUrl);
    if (!origin || !/^\/[a-zA-Z0-9/_-]+$/.test(path)) return null;
    const headers = new Headers({ Accept: "application/json" });
    if (options.serviceKey && env?.TYPHOON_BACKEND_API_KEY?.trim()) {
        headers.set("X-API-Key", env.TYPHOON_BACKEND_API_KEY.trim());
        // Backend rate-limits keyed calls per viewer, not per Cloudflare egress IP.
        if (options.clientIp) headers.set("X-Client-IP", options.clientIp);
    }
    if (options.clientRequest) {
        for (const name of ["Authorization", "X-API-Key"]) {
            const value = options.clientRequest.headers.get(name);
            if (value) headers.set(name, value);
        }
    }
    if (options.body !== undefined) headers.set("Content-Type", "application/json");
    try {
        const response = await fetch(new URL(path, origin), {
            method: options.method || "GET",
            headers,
            body: options.body,
            redirect: "error",
            signal: AbortSignal.timeout(options.timeoutMs || 6000),
        });
        const text = await response.text();
        if (text.length > MAX_RESPONSE_BYTES) return null;
        return { ok: response.ok, status: response.status, data: JSON.parse(text) };
    } catch {
        return null;
    }
}

export async function approvedBackend(env, pageUrl) {
    const approvedVersion = env?.TYPHOON_APPROVED_MODEL_VERSION?.trim();
    const approvedRevision = env?.TYPHOON_APPROVED_MODEL_REVISION?.trim();
    if (!approvedVersion || !/^[a-f0-9]{64}$/.test(approvedRevision || "")) return null;
    const [ready, version] = await Promise.all([
        backendJson(env, pageUrl, "/ready", { timeoutMs: 5000 }),
        backendJson(env, pageUrl, "/version", { timeoutMs: 5000 }),
    ]);
    if (
        ready?.ok !== true || ready.data?.status !== "ready" ||
        version?.ok !== true || version.data?.model_kind !== "trained-model" ||
        version.data?.model_version !== approvedVersion ||
        version.data?.model_revision !== approvedRevision ||
        typeof version.data?.dataset_version !== "string" ||
        version.data.dataset_version.toLowerCase().startsWith("synthetic")
    ) return null;
    return version.data;
}

export function freshBackendStorm(item) {
    if (!item || typeof item.id !== "string" || !/^[A-Za-z0-9_-]{2,40}$/.test(item.id)) {
        return false;
    }
    const latest = item.latest;
    const issue = Date.parse(latest?.timestamp);
    const age = Date.now() - issue;
    return typeof item.name === "string" && item.name.length > 0 &&
        typeof latest?.source === "string" && latest.source.length > 0 &&
        Number.isFinite(issue) && age >= -30 * 60_000 && age <= 24 * 60 * 60_000 &&
        Number.isFinite(latest?.lat) && latest.lat >= -90 && latest.lat <= 90 &&
        Number.isFinite(latest?.lon) && latest.lon >= -180 && latest.lon <= 180;
}

export async function approvedActiveFeed(env, pageUrl, clientIp) {
    const work = (async () => {
        const version = await approvedBackend(env, pageUrl);
        if (!version) return null;
        const response = await backendJson(env, pageUrl, "/typhoons/active", {
            serviceKey: true,
            clientIp,
        });
        const items = response?.data?.typhoons;
        if (!response?.ok || !Array.isArray(items) || items.length === 0 ||
            items.length > 20 || !items.every(freshBackendStorm)) return null;
        return { version, items, disclaimer: response.data.disclaimer };
    })();
    return Promise.race([
        work,
        new Promise((resolve) => setTimeout(() => resolve(null), 6000)),
    ]);
}

export async function activeAlertDelivery(env, pageUrl) {
    const result = await backendJson(env, pageUrl, "/subscriptions");
    return result?.ok === true && result.data?.available === true &&
        result.data?.delivery === "active";
}

export function freshBackendForecast(forecast, approvedVersion) {
    const issue = Date.parse(forecast?.issue_time);
    const age = Date.now() - issue;
    return forecast?.model_kind === "trained-model" &&
        forecast.model_version === approvedVersion &&
        Number.isFinite(issue) && age >= -30 * 60_000 && age <= 24 * 60 * 60_000 &&
        Array.isArray(forecast.points) && forecast.points.length > 0 &&
        forecast.points.length <= 20 && forecast.points.every((point) =>
            Number.isFinite(point?.lat) && point.lat >= -90 && point.lat <= 90 &&
            Number.isFinite(point?.lon) && point.lon >= -180 && point.lon <= 180 &&
            Number.isFinite(point?.horizon_hours) && point.horizon_hours > 0 &&
            point.horizon_hours <= 120,
        );
}
