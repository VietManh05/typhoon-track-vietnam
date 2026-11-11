import { backendJson } from "../_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const result = await backendJson(env, request.url, "/auth/session", {
        clientRequest: request,
    });
    if (result?.ok && result.data?.authenticated === true) {
        return Response.json(
            { authenticated: true },
            { headers: { "Cache-Control": "no-store" } },
        );
    }
    return Response.json(
        { authenticated: false, error: "Backend authentication failed or is unavailable." },
        { status: result?.status === 401 ? 401 : 503, headers: { "Cache-Control": "no-store" } },
    );
}
