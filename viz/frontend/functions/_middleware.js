const SECURITY_HEADERS = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    // Keep in sync with CONTENT_SECURITY_POLICY in src/typhoon_vn/api/app.py.
    "Content-Security-Policy": "default-src 'self'; script-src 'self' https://api.windy.com https://*.windy.com https://unpkg.com; style-src 'self' 'unsafe-inline' https://unpkg.com https://*.windy.com; img-src 'self' data: blob: https://server.arcgisonline.com https://unpkg.com https://*.windy.com; font-src 'self' data:; connect-src 'self' https://*.windy.com; worker-src 'self' blob:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'",
};

export async function onRequest({ next }) {
    const upstream = await next();
    const response = new Response(upstream.body, upstream);
    for (const [name, value] of Object.entries(SECURITY_HEADERS)) {
        response.headers.set(name, value);
    }
    return response;
}
