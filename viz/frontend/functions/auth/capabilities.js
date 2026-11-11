import { backendJson } from "../_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const result = await backendJson(env, request.url, "/auth/capabilities");
    return Response.json(
        { available: result?.ok === true && result.data?.available === true,
            reason: result?.ok ? null : "Authentication requires a reachable Python backend." },
        { headers: { "Cache-Control": "no-store" } },
    );
}
