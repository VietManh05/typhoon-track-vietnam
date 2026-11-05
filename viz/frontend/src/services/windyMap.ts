import type L from "leaflet";

const LEAFLET_SCRIPT_ID = "windy-leaflet-runtime";
const WINDY_SCRIPT_ID = "windy-map-forecast-runtime";
const LEAFLET_URL = "https://unpkg.com/leaflet@1.4.0/dist/leaflet.js";
const WINDY_URL = "https://api.windy.com/assets/map-forecast/libBoot.js";

export type WindyOverlay = "wind" | "temp" | "pressure";

export interface WindyStore {
    get(key: string): unknown;
    getAllowed(key: string): unknown;
    set(key: string, value: unknown, options?: { forceChange?: boolean }): void;
    on(key: string, callback: (...args: unknown[]) => void): void;
    off(key: string, callback: (...args: unknown[]) => void): void;
}

export interface WindyPicker {
    open(location: { lat: number; lon: number }): void;
    close(): void;
}

export interface WindyApi {
    map: L.Map;
    store: WindyStore;
    picker: WindyPicker;
}

interface WindyOptions {
    key: string;
    lat: number;
    lon: number;
    zoom: number;
    overlay: WindyOverlay;
    level: "surface";
    particlesAnim: "on" | "off";
    hourFormat: "24h";
    lang: "vi" | "en";
    verbose: boolean;
}

declare global {
    interface Window {
        L?: typeof import("leaflet");
        windyInit?: (
            options: WindyOptions,
            callback: (api: WindyApi) => void,
        ) => void;
    }
}

const scriptLoads = new Map<string, Promise<void>>();

function loadScript(id: string, src: string): Promise<void> {
    const activeLoad = scriptLoads.get(id);
    if (activeLoad) return activeLoad;

    const promise = new Promise<void>((resolve, reject) => {
        const existing = document.getElementById(id) as HTMLScriptElement | null;
        const script = existing ?? document.createElement("script");

        const onLoad = () => {
            script.dataset.loaded = "true";
            resolve();
        };
        const onError = () => reject(new Error(`Unable to load ${src}`));

        if (script.dataset.loaded === "true") {
            resolve();
            return;
        }

        script.addEventListener("load", onLoad, { once: true });
        script.addEventListener("error", onError, { once: true });

        if (!existing) {
            script.id = id;
            script.src = src;
            script.async = true;
            script.crossOrigin = "anonymous";
            document.head.appendChild(script);
        }
    });

    scriptLoads.set(id, promise);
    return promise;
}

async function loadWindyRuntime(): Promise<typeof import("leaflet")> {
    if (!window.L) await loadScript(LEAFLET_SCRIPT_ID, LEAFLET_URL);
    if (!window.L) throw new Error("Windy Leaflet runtime did not initialize");

    if (!window.windyInit) await loadScript(WINDY_SCRIPT_ID, WINDY_URL);
    if (!window.windyInit) throw new Error("Windy Map Forecast runtime did not initialize");

    return window.L;
}

export async function initializeWindyMap(
    apiKey: string,
    options: Omit<WindyOptions, "key">,
): Promise<{ api: WindyApi; leaflet: typeof import("leaflet") }> {
    const leaflet = await loadWindyRuntime();

    return new Promise((resolve, reject) => {
        const timeout = window.setTimeout(
            () => reject(new Error("Windy Map Forecast initialization timed out")),
            20_000,
        );

        try {
            window.windyInit?.({ ...options, key: apiKey }, (api) => {
                window.clearTimeout(timeout);
                if (!api?.map || !api.store) {
                    reject(new Error("Windy Map Forecast returned an invalid API object"));
                    return;
                }
                resolve({ api, leaflet });
            });
        } catch (error) {
            window.clearTimeout(timeout);
            reject(error);
        }
    });
}
