import { backendJson } from "./_lib/backend.js";
import { createRateLimiter, tooManyRequests } from "./_lib/rateLimit.js";

const isRateLimited = createRateLimiter("AUTH_RATE_LIMITER", 10);

export async function onRequestPost({ env, request }) {
    if (await isRateLimited(request, env)) return tooManyRequests();
    const body = await request.text();
    if (body.length > 4096) {
        return Response.json({ error: { message: "Request too large" } }, { status: 413 });
    }
    const result = await backendJson(env, request.url, "/token", {
        method: "POST",
        body,
    });
    if (result?.ok && typeof result.data?.access_token === "string") {
        return Response.json(result.data, { headers: { "Cache-Control": "no-store" } });
    }
    return Response.json(
        { error: { code: "AUTH_UNAVAILABLE", message: "Backend login failed or is unavailable." } },
        { status: result?.status === 401 ? 401 : 503, headers: { "Cache-Control": "no-store" } },
    );
}
