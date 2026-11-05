import { backendJson } from "./_lib/backend.js";

const unavailable = () =>
    Response.json(
        {
            error: {
                code: "ALERT_DELIVERY_UNAVAILABLE",
                message:
                    "Dịch vụ gửi cảnh báo chưa được kích hoạt trên bản Cloudflare Pages. Hãy theo dõi bản tin NCHMF và cơ quan chức năng.",
            },
        },
        {
            status: 503,
            headers: { "Cache-Control": "no-store" },
        },
    );

export async function onRequestGet({ env, request }) {
    const result = await backendJson(env, request.url, "/subscriptions");
    if (result?.ok && typeof result.data?.available === "boolean") {
        return Response.json(result.data, { headers: { "Cache-Control": "no-store" } });
    }
    return unavailable();
}

export async function onRequestPost({ env, request }) {
    const capability = await backendJson(env, request.url, "/subscriptions");
    if (capability?.ok !== true || capability.data?.available !== true ||
        capability.data?.delivery !== "active") return unavailable();
    const body = await request.text();
    if (body.length > 4096) {
        return Response.json({ error: { message: "Request too large" } }, { status: 413 });
    }
    const result = await backendJson(env, request.url, "/subscriptions", {
        method: "POST",
        body,
        clientRequest: request,
    });
    if (result?.ok && result.data?.delivery === "active") {
        return Response.json(result.data, { status: 201, headers: { "Cache-Control": "no-store" } });
    }
    return unavailable();
}
