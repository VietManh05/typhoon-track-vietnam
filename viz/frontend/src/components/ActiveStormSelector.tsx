import React from "react";
import { Radar, Wind } from "lucide-react";
import { Language, translations } from "../i18n";
import { getIntensityToken } from "../lib/storm";
import { windKmh } from "../lib/format";
import { ActiveTyphoonItem } from "../types";

interface ActiveStormSelectorProps {
    storms: ActiveTyphoonItem[];
    selectedStormId: string;
    onSelectStorm: (id: string) => void;
    lang: Language;
}

export const ActiveStormSelector: React.FC<ActiveStormSelectorProps> = ({
    storms,
    selectedStormId,
    onSelectStorm,
    lang,
}) => {
    const t = translations[lang];

    return (
        <section
            className="storm-strip border-b border-line bg-surface/55 px-3 py-2 sm:px-4"
            aria-labelledby="tracked-storms-title"
        >
            <div className="mx-auto flex max-w-[1920px] items-center gap-3 overflow-x-auto pb-0.5">
                <div className="flex shrink-0 items-center gap-2 pr-1">
                    <Radar
                        className="h-4 w-4 text-primary"
                        aria-hidden="true"
                    />
                    <h2
                        id="tracked-storms-title"
                        className="whitespace-nowrap text-sm font-semibold text-fg-muted"
                    >
                        {t.active_storms}
                    </h2>
                    <span className="badge border-line bg-surface-2 text-fg-faint">
                        {storms.length}
                    </span>
                    {storms.some((storm) => storm.latest.source.startsWith("JMA")) && (
                        <a
                            href="https://www.jma.go.jp/bosai/typhoon/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="whitespace-nowrap text-xs text-primary underline underline-offset-2"
                            title={lang === "vi" ? "Dữ liệu JMA được Typhoon VN xử lý; cảnh báo chính thức tại Việt Nam theo NCHMF" : "JMA data processed by Typhoon VN; follow NCHMF for official Vietnam warnings"}
                        >
                            {lang === "vi" ? "Nguồn JMA · đã xử lý" : "JMA source · processed"}
                        </a>
                    )}
                </div>

                <div
                    className="flex items-center gap-2"
                    role="tablist"
                    aria-label={t.active_storms}
                >
                    {storms.map((storm) => {
                        const active = storm.id === selectedStormId;
                        const token = getIntensityToken(storm.latest.intensity);
                        const speed = windKmh(
                            storm.latest.wind_ms,
                            storm.latest.wind_kmh,
                        );

                        return (
                            <button
                                key={storm.id}
                                role="tab"
                                aria-selected={active}
                                onClick={() => onSelectStorm(storm.id)}
                                className={`chip ${active ? "chip-active" : ""}`}
                            >
                                <span
                                    className={`h-2 w-2 rounded-full ${token.dot}`}
                                    aria-hidden="true"
                                />
                                <span className="font-semibold text-fg">
                                    {lang === "vi" && storm.name_vi
                                        ? storm.name_vi
                                        : storm.name}
                                </span>
                                <span className="font-mono text-xs text-fg-faint">
                                    {storm.id}
                                </span>
                                <span
                                    className={`badge ${token.bg} ${token.border} ${token.text}`}
                                >
                                    {storm.latest.intensity}
                                </span>
                                {speed !== null ? (
                                    <span className="flex items-center gap-1 font-mono text-xs text-fg-muted">
                                        <Wind
                                            className="h-3 w-3"
                                            aria-hidden="true"
                                        />
                                        {speed}&nbsp;km/h
                                    </span>
                                ) : null}
                            </button>
                        );
                    })}
                </div>
            </div>
        </section>
    );
};
