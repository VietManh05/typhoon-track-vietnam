import { backendJson } from "./_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const result = await backendJson(env, request.url, "/alerts", {
        clientRequest: request,
    });
    if (result?.ok && Array.isArray(result.data?.alerts)) {
        return Response.json(result.data, { headers: { "Cache-Control": "no-store" } });
    }
    return Response.json(
        { error: { code: "ALERTS_UNAVAILABLE", message: "Alert drafts require backend authentication." } },
        { status: result?.status === 401 ? 401 : 503, headers: { "Cache-Control": "no-store" } },
    );
}
