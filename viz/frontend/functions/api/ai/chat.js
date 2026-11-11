const DEFAULT_MODEL = "gemma4:31b";
const MAX_QUESTION_LENGTH = 2000;
const MAX_HISTORY_MESSAGES = 6;
const MAX_BODY_BYTES = 20000;
const RATE_LIMIT_WINDOW_MS = 60000;
const RATE_LIMIT_REQUESTS = 10;
const rateLimitBuckets = new Map();

const json = (body, status = 200, headers = {}) =>
    Response.json(body, {
        status,
        headers: { "Cache-Control": "no-store", ...headers },
    });

// Prefer the Cloudflare rate-limit binding (shared across isolates). The
// in-memory map is only a per-isolate fallback when the binding is absent.
const isRateLimited = async (request, env) => {
    const key = request.headers.get("CF-Connecting-IP") || "unknown";
    if (env?.AI_RATE_LIMITER?.limit) {
        try {
            const { success } = await env.AI_RATE_LIMITER.limit({ key });
            return !success;
        } catch {
            // Fall through to the local limiter if the binding errors.
        }
    }
    const now = Date.now();
    let bucket = rateLimitBuckets.get(key);
    if (!bucket || now - bucket.startedAt >= RATE_LIMIT_WINDOW_MS) {
        bucket = { startedAt: now, count: 0 };
        rateLimitBuckets.set(key, bucket);
    }
    bucket.count += 1;

    if (rateLimitBuckets.size > 1000) {
        for (const [bucketKey, candidate] of rateLimitBuckets) {
            if (now - candidate.startedAt >= RATE_LIMIT_WINDOW_MS) {
                rateLimitBuckets.delete(bucketKey);
            }
        }
    }
    return bucket.count > RATE_LIMIT_REQUESTS;
};

const cleanHistory = (history) => {
    if (!Array.isArray(history)) return [];
    return history
        .slice(-MAX_HISTORY_MESSAGES)
        .filter(
            (item) =>
                item &&
                (item.role === "user" || item.role === "assistant") &&
                typeof item.content === "string",
        )
        .map((item) => ({
            role: item.role,
            content: item.content.trim().slice(0, MAX_QUESTION_LENGTH),
        }))
        .filter((item) => item.content.length > 0);
};

export async function onRequestPost({ request, env }) {
    const requestOrigin = request.headers.get("Origin");
    // Browsers always send Origin on POST; a missing one means a scripted client.
    if (requestOrigin !== new URL(request.url).origin) {
        return json({ error: { code: "FORBIDDEN", message: "Origin not allowed" } }, 403);
    }

    const apiKey = typeof env.OLLAMA_API_KEY === "string" ? env.OLLAMA_API_KEY.trim() : "";
    if (!apiKey) {
        return json(
            {
                error: {
                    code: "AI_NOT_CONFIGURED",
                    message: "Ollama Cloud chưa được cấu hình.",
                },
            },
            503,
        );
    }

    if (await isRateLimited(request, env)) {
        return json(
            {
                error: {
                    code: "RATE_LIMITED",
                    message: "Bạn đang gửi câu hỏi quá nhanh. Vui lòng thử lại sau một phút.",
                },
            },
            429,
            { "Retry-After": "60" },
        );
    }

    const contentLength = Number(request.headers.get("Content-Length") || 0);
    if (contentLength > MAX_BODY_BYTES) {
        return json({ error: { code: "PAYLOAD_TOO_LARGE", message: "Yêu cầu quá lớn." } }, 413);
    }

    let rawBody;
    try {
        rawBody = await request.text();
    } catch {
        return json({ error: { code: "INVALID_BODY", message: "Không thể đọc yêu cầu." } }, 400);
    }
    if (new TextEncoder().encode(rawBody).byteLength > MAX_BODY_BYTES) {
        return json({ error: { code: "PAYLOAD_TOO_LARGE", message: "Yêu cầu quá lớn." } }, 413);
    }

    let body;
    try {
        body = JSON.parse(rawBody);
    } catch {
        return json({ error: { code: "INVALID_JSON", message: "JSON không hợp lệ." } }, 400);
    }

    const question = typeof body?.question === "string" ? body.question.trim() : "";
    if (!question || question.length > MAX_QUESTION_LENGTH) {
        return json(
            {
                error: {
                    code: "INVALID_QUESTION",
                    message: `Câu hỏi phải có từ 1 đến ${MAX_QUESTION_LENGTH} ký tự.`,
                },
            },
            400,
        );
    }

    const language = body?.language === "en" ? "English" : "Vietnamese";
    const systemPrompt = [
        `Reply in ${language}.`,
        "You are the AI assistant for Typhoon VN, an experimental weather decision-support dashboard.",
        "Explain weather and tropical-cyclone concepts clearly and concisely.",
        "Never invent current observations, storm tracks, forecasts, alerts, or source attribution.",
        "If live data is absent from the user's message, state that you cannot verify current conditions.",
        "For safety-critical decisions, direct the user to official NCHMF and local authority bulletins.",
        "Do not claim to replace professional meteorologists or official warnings.",
    ].join(" ");

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 45000);
    try {
        const upstream = await fetch("https://ollama.com/api/chat", {
            method: "POST",
            headers: {
                Authorization: `Bearer ${apiKey}`,
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                model: env.OLLAMA_MODEL || DEFAULT_MODEL,
                stream: false,
                think: false,
                messages: [
                    { role: "system", content: systemPrompt },
                    ...cleanHistory(body.history),
                    { role: "user", content: question },
                ],
                options: { temperature: 0.2, num_predict: 500 },
            }),
            signal: controller.signal,
        });

        if (!upstream.ok) {
            return json(
                {
                    error: {
                        code: "OLLAMA_UPSTREAM_ERROR",
                        message:
                            upstream.status === 401
                                ? "Ollama API key không hợp lệ."
                                : "Ollama Cloud tạm thời không khả dụng.",
                    },
                },
                upstream.status === 401 ? 502 : 503,
            );
        }

        const payload = await upstream.json();
        const answer = payload?.message?.content;
        if (typeof answer !== "string" || !answer.trim()) {
            return json(
                { error: { code: "INVALID_AI_RESPONSE", message: "Ollama trả về dữ liệu không hợp lệ." } },
                502,
            );
        }

        return json({
            answer: answer.trim(),
            model: payload.model || env.OLLAMA_MODEL || DEFAULT_MODEL,
        });
    } catch (error) {
        return json(
            {
                error: {
                    code: error instanceof Error && error.name === "AbortError" ? "AI_TIMEOUT" : "AI_UNAVAILABLE",
                    message:
                        error instanceof Error && error.name === "AbortError"
                            ? "Ollama phản hồi quá thời gian cho phép."
                            : "Không thể kết nối Ollama Cloud.",
                },
            },
            503,
        );
    } finally {
        clearTimeout(timeout);
    }
}
