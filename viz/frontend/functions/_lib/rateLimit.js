const WINDOW_MS = 60000;

// Per-client limiter for proxied routes: the backend only sees the proxy's
// address, so its own per-IP limit cannot tell callers apart.
// shortcut: unless `bindingName` is bound this is per-isolate memory, which only
// slows an attacker down, and Cloudflare's docs do not list a rate-limit binding
// for Pages Functions; the backend's own limiter stays the hard cap. Move the
// counter to KV or a Durable Object if that cap is not enough.
// One IPv6 customer usually owns a whole /64, so rotating the low bits must
// not buy a fresh budget. IPv4 (and IPv4-mapped) addresses are kept whole.
export const clientKey = (ip) => {
    if (!ip.includes(":") || ip.includes(".")) return ip;
    const [head, tail = ""] = ip.toLowerCase().split("::");
    const left = head ? head.split(":") : [];
    const right = tail ? tail.split(":") : [];
    const missing = ip.includes("::") ? Math.max(0, 8 - left.length - right.length) : 0;
    const groups = [...left, ...Array(missing).fill("0"), ...right]
        .map((group) => group.replace(/^0+(?=.)/, ""));
    // Hex-form IPv4-mapped (::ffff:cb00:7107) is still one IPv4 host, not a /64.
    if (groups.slice(0, 6).join(":") === "0:0:0:0:0:ffff") return groups.join(":");
    return `${groups.slice(0, 4).join(":")}::/64`;
};

export const createRateLimiter = (bindingName, maxRequests) => {
    const buckets = new Map();
    return async (request, env) => {
        const key = clientKey(request.headers.get("CF-Connecting-IP") || "unknown");
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
