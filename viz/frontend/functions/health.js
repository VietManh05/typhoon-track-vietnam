import { targets, storm } from "./_lib/jma.js";
import { activeAlertDelivery, approvedActiveFeed } from "./_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const [backendResult, feedResult, alertResult] = await Promise.allSettled([
        approvedActiveFeed(env, request.url),
        (async () => {
            const items = await targets();
            await Promise.all(items.map((item) => storm(item.tropicalCyclone)));
        })(),
        activeAlertDelivery(env, request.url),
    ]);
    const backend = backendResult.status === "fulfilled" ? backendResult.value : null;
    const stormFeed = Boolean(backend) || feedResult.status === "fulfilled";
    return Response.json(
        {
            status: "ok",
            environment: "cloudflare-pages",
            service: "typhoon-vn-edge",
            capabilities: {
                weather: true,
                ai: Boolean(env?.OLLAMA_API_KEY?.trim()),
                stormFeed,
                modelForecast: Boolean(backend),
                modelVersion: backend?.version.model_version || null,
                alertDelivery: alertResult.status === "fulfilled" && alertResult.value === true,
            },
        },
        { headers: { "Cache-Control": "no-store" } },
    );
}
