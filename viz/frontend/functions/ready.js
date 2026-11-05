import { activeAlertDelivery, approvedActiveFeed } from "./_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const [backend, alertDeliveryReady] = await Promise.all([
        approvedActiveFeed(env, request.url),
        activeAlertDelivery(env, request.url),
    ]);
    const ready = Boolean(backend) && alertDeliveryReady;
    return Response.json(
        {
            status: ready ? "ready" : "not_ready",
            environment: "cloudflare-pages",
            modelBackendReady: Boolean(backend),
            alertDeliveryReady,
            reason: ready
                ? null
                : backend
                ? "The approved model backend is connected, but alert delivery is not active."
                : "An approved model backend and alert delivery are not connected. The JMA storm feed has separate availability checks.",
        },
        { status: ready ? 200 : 503, headers: { "Cache-Control": "no-store" } },
    );
}
