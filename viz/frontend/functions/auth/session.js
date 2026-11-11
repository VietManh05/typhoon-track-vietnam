import { backendJson } from "../_lib/backend.js";
import { createRateLimiter, tooManyRequests } from "../_lib/rateLimit.js";

// Each call tests one API key, so it is a guessing oracle like /token.
const isRateLimited = createRateLimiter("AUTH_RATE_LIMITER", 10);

export async function onRequestGet({ env, request }) {
    if (await isRateLimited(request, env)) return tooManyRequests();
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
