import React from "react";
import { History } from "lucide-react";
import { HindcastSummary, Suggestion } from "../types";
import { Language, translations } from "../i18n";

interface SuggestionPanelProps {
    suggestion: Suggestion;
    hindcast?: HindcastSummary;
    lang: Language;
}

const HORIZONS = ["6", "12", "24", "48", "72"];

/** Historical analog storms behind the k-NN track suggestion (+ hindcast errors). */
export const SuggestionPanel: React.FC<SuggestionPanelProps> = ({ suggestion, hindcast, lang }) => {
    const t = translations[lang];
    const vi = lang === "vi";
    return (
        <section className="panel flex flex-col gap-3 p-4" aria-label={t.suggestion_title}>
            <div className="flex items-center gap-2 text-sm font-semibold text-fg">
                <History className="h-4 w-4 text-pink-400" aria-hidden="true" />
                {t.suggestion_title}
            </div>
            <p className="text-xs text-fg-muted">{t.suggestion_intro}</p>
            <ol className="flex flex-col gap-1.5">
                {suggestion.analogs.map((analog) => (
                    <li
                        key={analog.storm_id}
                        className="flex items-center justify-between gap-2 rounded-control border border-line bg-surface-2 px-3 py-1.5 text-xs"
                    >
                        <span className="text-fg-muted">#{analog.rank}</span>
                        <span className="font-semibold text-fg">
                            {analog.name} ({analog.year})
                        </span>
                        <span className="font-mono text-fg-muted">{analog.storm_id}</span>
                    </li>
                ))}
            </ol>

            {hindcast && (
                <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                        <caption className="pb-1 text-left text-fg-muted">
                            {vi
                                ? "Sai số so với quỹ đạo thực tế (km)"
                                : "Error against the actual track (km)"}
                        </caption>
                        <thead>
                            <tr className="text-fg-muted">
                                <th className="text-left font-medium">{vi ? "Phương pháp" : "Method"}</th>
                                {HORIZONS.map((h) => (
                                    <th key={h} className="text-right font-medium">{h}h</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody className="font-mono">
                            <tr>
                                <td className="text-left text-amber-400">{vi ? "Mô hình LSTM" : "LSTM model"}</td>
                                {HORIZONS.map((h) => (
                                    <td key={h} className="text-right">
                                        {Math.round(hindcast.errors_km.model[h])}
                                        {hindcast.inside_cone[h] ? "" : "*"}
                                    </td>
                                ))}
                            </tr>
                            {hindcast.errors_km.analog && (
                                <tr>
                                    <td className="text-left text-pink-400">{vi ? "Gợi ý k-NN" : "k-NN suggestion"}</td>
                                    {HORIZONS.map((h) => (
                                        <td key={h} className="text-right">
                                            {Math.round(hindcast.errors_km.analog![h])}
                                        </td>
                                    ))}
                                </tr>
                            )}
                        </tbody>
                    </table>
                    <p className="pt-1 text-xs text-fg-muted">
                        {vi
                            ? "* vị trí thực tế nằm ngoài nón bất định của mô hình."
                            : "* actual position outside the model's uncertainty cone."}
                    </p>
                </div>
            )}

            <p className="text-xs italic text-fg-muted">
                {t.suggestion_caveat} <span className="not-italic">{suggestion.method}</span>
            </p>
        </section>
    );
};
