import React, { useEffect, useState } from "react";
import { Language } from "../i18n";

interface Snapshot {
    observedAt: string;
    observations: { id: string; name: string; temperatureC: number; sourceUrl: string }[];
    bulletins: { id: string; title: string; issuedAt: string; sourceUrl: string }[];
    metadata: { isStale: boolean; sourceUrl: string };
}

export const NchmfPanel: React.FC<{ lang: Language }> = ({ lang }) => {
    const [data, setData] = useState<Snapshot | null>(null);
    const [error, setError] = useState(false);
    const [loading, setLoading] = useState(true);
    const [query, setQuery] = useState("");
    const vi = lang === "vi";

    useEffect(() => {
        let active = true;
        let request: AbortController | undefined;
        const refresh = async () => {
            request?.abort();
            const controller = new AbortController();
            request = controller;
            const timeout = window.setTimeout(() => controller.abort(), 12000);
            try {
                const response = await fetch("/api/weather/nchmf", { signal: controller.signal });
                if (!response.ok) throw new Error("NCHMF unavailable");
                const snapshot: Snapshot = await response.json();
                if (!Array.isArray(snapshot.observations) || !Array.isArray(snapshot.bulletins)) {
                    throw new Error("NCHMF invalid response");
                }
                if (active) { setData(snapshot); setError(false); }
            } catch {
                if (active) setError(true);
            } finally {
                window.clearTimeout(timeout);
                if (active) setLoading(false);
            }
        };
        void refresh();
        const interval = window.setInterval(() => { void refresh(); }, 600000);
        return () => { active = false; request?.abort(); window.clearInterval(interval); };
    }, []);

    const normalize = (value: string) => value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").replace(/đ/gi, "d").toLocaleLowerCase();
    const filtered = data?.observations.filter(item => normalize(item.name).includes(normalize(query))) ?? [];
    const formatTime = (value: string) => new Date(value).toLocaleString(vi ? "vi-VN" : "en-GB", { timeZone: "Asia/Ho_Chi_Minh" });

    return <section className="weather-section" aria-labelledby="nchmf-title" aria-busy={loading}>
        <h3 id="nchmf-title">{vi ? "Thời tiết từ NCHMF" : "NCHMF weather"}</h3>
        <p className="weather-source"><a href="https://nchmf.gov.vn/kttvsite/" target="_blank" rel="noreferrer">{vi ? "Trung tâm Dự báo KTTV quốc gia" : "National Centre for Hydro-Meteorological Forecasting"}</a></p>
        {loading && <p role="status">{vi ? "Đang tải nguồn NCHMF…" : "Loading NCHMF…"}</p>}
        {error && <p role="status">{vi ? "Chưa cập nhật được nguồn NCHMF. Mở trang nguồn để kiểm tra bản tin mới nhất." : "NCHMF update unavailable. Check the source for the latest bulletin."}</p>}
        {data && <>
            <p className="weather-source">{vi ? "Giờ quan trắc" : "Observation time"}: <time dateTime={data.observedAt}>{formatTime(data.observedAt)} GMT+7</time></p>
            {(data.metadata.isStale || error) && <p role="status" className="text-warning">{vi ? "Dữ liệu cũ — chưa xác nhận quan trắc mới." : "Stale data — newer observations unconfirmed."}</p>}
            <label className="location-search" htmlFor="nchmf-search"><span className="sr-only">{vi ? "Tìm địa điểm NCHMF" : "Search NCHMF locations"}</span><input id="nchmf-search" type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder={vi ? "Tìm địa điểm NCHMF…" : "Search NCHMF locations…"} /></label>
            <div className="daily-list scroll-area" style={{ maxHeight: 240, overflowY: "auto" }} tabIndex={0} role="region" aria-label={vi ? "Nhiệt độ các địa điểm" : "Location temperatures"}>
                {filtered.map(item => <p key={item.id} className="flex justify-between gap-3 py-2"><a href={item.sourceUrl} target="_blank" rel="noreferrer">{item.name}</a><strong>{item.temperatureC}°C</strong></p>)}
                {!filtered.length && <p>{vi ? "Không có địa điểm phù hợp." : "No matching locations."}</p>}
            </div>
            <h4 className="mt-4">{vi ? "Bản tin từ nguồn" : "Source bulletins"}</h4>
            <ul className="space-y-3 mt-2">{data.bulletins.slice(0, 5).map(item => <li key={item.id}><a href={item.sourceUrl} target="_blank" rel="noreferrer">{item.title}</a><p className="weather-source"><time dateTime={item.issuedAt}>{formatTime(item.issuedAt)} GMT+7</time></p></li>)}</ul>
            <p className="weather-source">{vi ? "Danh sách bản tin toàn quốc; không tự suy ra cảnh báo cho địa điểm đang chọn." : "National bulletin list; not a warning inferred for the selected location."}</p>
        </>}
    </section>;
};
