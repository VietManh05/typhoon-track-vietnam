import { activeItem, attribution, storm, targets } from "../_lib/jma.js";
import { approvedActiveFeed } from "../_lib/backend.js";

export async function onRequestGet({ env, request }) {
    const jma = (async () => {
        const list = await targets();
        return Promise.all(list.map(async (item) =>
            activeItem(await storm(item.tropicalCyclone)),
        ));
    })().then((typhoons) => ({ typhoons }), () => null);
    const approved = await approvedActiveFeed(
        env, request.url, request.headers.get("CF-Connecting-IP"),
    );
    if (approved) {
        return Response.json(
            { typhoons: approved.items, feedAvailable: true, source: "Typhoon VN backend", modelVersion: approved.version.model_version, disclaimer: approved.disclaimer },
            { headers: { "Cache-Control": "no-store" } },
        );
    }
    try {
        const fallback = await jma;
        if (!fallback) throw new Error("JMA feed unavailable");
        return Response.json(
            { typhoons: fallback.typhoons, feedAvailable: true, source: "JMA RSMC Tokyo", disclaimer: attribution },
            { headers: { "Cache-Control": "no-store" } },
        );
    } catch {
        return Response.json(
            { typhoons: [], feedAvailable: false, error: "JMA feed unavailable or stale", disclaimer: attribution },
            { status: 503, headers: { "Cache-Control": "no-store" } },
        );
    }
}
