const WINDOW_MS = 60000;

// Per-client limiter for proxied routes: the backend only sees the proxy's
// address, so its own per-IP limit cannot tell callers apart.
// shortcut: without the Cloudflare binding this is per-isolate memory, which
// only slows an attacker down; bind `bindingName` in production.
export const createRateLimiter = (bindingName, maxRequests) => {
    const buckets = new Map();
    return async (request, env) => {
        const key = request.headers.get("CF-Connecting-IP") || "unknown";
        const binding = env?.[bindingName];
        if (binding?.limit) {
            try {
                const { success } = await binding.limit({ key });
                return !success;
            } catch {
                // Fall through to the local limiter if the binding errors.
            }
        }
        const now = Date.now();
        let bucket = buckets.get(key);
        if (!bucket || now - bucket.startedAt >= WINDOW_MS) {
            bucket = { startedAt: now, count: 0 };
            buckets.set(key, bucket);
        }
        bucket.count += 1;
        if (buckets.size > 1000) {
            for (const [bucketKey, candidate] of buckets) {
                if (now - candidate.startedAt >= WINDOW_MS) buckets.delete(bucketKey);
            }
        }
        return bucket.count > maxRequests;
    };
};

export const tooManyRequests = () =>
    Response.json(
        { error: { code: "RATE_LIMITED", message: "Too many requests. Try again later." } },
        { status: 429, headers: { "Cache-Control": "no-store", "Retry-After": "60" } },
    );
