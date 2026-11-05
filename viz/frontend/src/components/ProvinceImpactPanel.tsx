import React, { useDeferredValue, useMemo, useState } from "react";
import { Clock3, MapPin, Navigation, Search, ShieldAlert } from "lucide-react";
import { Language, translations } from "../i18n";
import { formatHours, formatKm } from "../lib/format";
import { getRiskLevel, RISK_LABEL_KEYS, RISK_TOKENS } from "../lib/storm";
import { ProvinceImpact } from "../types";

interface ProvinceImpactPanelProps {
    impacts: ProvinceImpact[];
    selectedProvinceId: string | null;
    onSelectProvince: (id: string) => void;
    lang: Language;
}

type Filter = "all" | "danger" | "near" | "cone";

export const ProvinceImpactPanel: React.FC<ProvinceImpactPanelProps> = ({
    impacts,
    selectedProvinceId,
    onSelectProvince,
    lang,
}) => {
    const [search, setSearch] = useState("");
    const [filter, setFilter] = useState<Filter>("all");
    const deferredSearch = useDeferredValue(
        search.trim().toLocaleLowerCase(lang === "vi" ? "vi" : "en"),
    );
    const t = translations[lang];

    const filtered = useMemo(
        () =>
            impacts.filter((impact) => {
                if (
                    deferredSearch &&
                    !impact.name
                        .toLocaleLowerCase(lang === "vi" ? "vi" : "en")
                        .includes(deferredSearch)
                )
                    return false;
                if (filter === "danger")
                    return (
                        impact.impact_level === "critical" ||
                        impact.impact_level === "high"
                    );
                if (filter === "near")
                    return impact.min_forecast_distance_km <= 150;
                if (filter === "cone") return impact.within_cone;
                return true;
            }),
        [deferredSearch, filter, impacts, lang],
    );

    const selected =
        impacts.find((impact) => impact.id === selectedProvinceId) ??
        impacts[0];
    const filterLabels: Record<Filter, string> = {
        all: lang === "vi" ? "Tất cả" : "All",
        danger: lang === "vi" ? "Nguy hiểm" : "Danger",
        near: lang === "vi" ? "Gần tâm bão" : "Near center",
        cone: lang === "vi" ? "Trong nón" : "In cone",
    };

    return (
        <section
            className="panel overflow-hidden"
            aria-labelledby="province-risk-title"
        >
            <div className="panel-head">
                <div>
                    <div className="mb-1 flex items-center gap-2 text-primary">
                        <MapPin className="h-4 w-4" aria-hidden="true" />
                        <span className="section-label">
                            {lang === "vi"
                                ? "Phân tích tác động"
                                : "Impact intelligence"}
                        </span>
                    </div>
                    <h2
                        id="province-risk-title"
                        className="text-sm font-semibold text-fg"
                    >
                        {t.province_impact_title}
                    </h2>
                </div>
                <span className="badge border-line bg-surface-2 font-mono text-fg-muted">
                    {impacts.length}
                </span>
            </div>

            <div className="space-y-3 p-3">
                {selected
                    ? (() => {
                          const level = getRiskLevel(selected.impact_level);
                          const token = RISK_TOKENS[level];
                          return (
                              <div
                                  className={`rounded-card border p-3 ${token.border} ${token.bg}`}
                              >
                                  <div className="flex items-start justify-between gap-3">
                                      <div>
                                          <div className="text-base font-semibold text-fg">
                                              {selected.name}
                                          </div>
                                          <div className="mt-1 flex flex-wrap gap-x-3 gap-y-1 font-mono text-2xs text-fg-muted">
                                              <span>
                                                  {formatKm(
                                                      selected.min_forecast_distance_km,
                                                  )}
                                                  &nbsp;km
                                              </span>
                                              <span>
                                                  ETA{" "}
                                                  {formatHours(
                                                      selected.eta_hours,
                                                  )}
                                              </span>
                                              {selected.within_cone ? (
                                                  <span className="text-warning">
                                                      {t.in_cone}
                                                  </span>
                                              ) : null}
                                          </div>
                                      </div>
                                      <span
                                          className={`badge ${token.border} ${token.bg} ${token.text}`}
                                      >
                                          <ShieldAlert
                                              className="h-3 w-3"
                                              aria-hidden="true"
                                          />
                                          {t[RISK_LABEL_KEYS[level]] as string}
                                      </span>
                                  </div>
                              </div>
                          );
                      })()
                    : null}

                <div className="relative" role="search">
                    <label htmlFor="province-search" className="sr-only">
                        {t.select_province}
                    </label>
                    <Search
                        className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-fg-faint"
                        aria-hidden="true"
                    />
                    <input
                        id="province-search"
                        type="search"
                        className="input pl-9"
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        placeholder={
                            lang === "vi"
                                ? "Tìm tỉnh/thành phố..."
                                : "Search province/city..."
                        }
                    />
                </div>

                <div
                    className="flex gap-1.5 overflow-x-auto pb-0.5"
                    role="group"
                    aria-label={
                        lang === "vi" ? "Bộ lọc rủi ro" : "Risk filters"
                    }
                >
                    {(Object.keys(filterLabels) as Filter[]).map((value) => (
                        <button
                            key={value}
                            className={`chip min-h-8 px-2.5 ${filter === value ? "chip-active" : ""}`}
                            onClick={() => setFilter(value)}
                            aria-pressed={filter === value}
                        >
                            {filterLabels[value]}
                        </button>
                    ))}
                </div>

                <div
                    className="scroll-area max-h-64 space-y-1 overflow-y-auto pr-1"
                    role="list"
                    aria-label={t.province_impact_title}
                >
                    {filtered.map((impact) => {
                        const level = getRiskLevel(impact.impact_level);
                        const token = RISK_TOKENS[level];
                        const active = selected?.id === impact.id;
                        return (
                            <button
                                key={impact.id}
                                role="listitem"
                                onClick={() => onSelectProvince(impact.id)}
                                className={`content-auto flex min-h-[58px] w-full items-center gap-3 rounded-control border px-3 py-2 text-left transition-colors duration-fast ${
                                    active
                                        ? "border-primary/45 bg-primary/[0.07]"
                                        : "border-transparent hover:border-line hover:bg-surface-2/70"
                                }`}
                            >
                                <span
                                    className={`h-2.5 w-2.5 shrink-0 rounded-full ${token.dot}`}
                                    aria-hidden="true"
                                />
                                <span className="min-w-0 flex-1">
                                    <span className="block truncate text-xs font-semibold text-fg">
                                        {impact.name}
                                    </span>
                                    <span className="mt-0.5 flex items-center gap-3 font-mono text-2xs text-fg-faint">
                                        <span className="flex items-center gap-1">
                                            <Navigation
                                                className="h-3 w-3"
                                                aria-hidden="true"
                                            />
                                            {formatKm(
                                                impact.min_forecast_distance_km,
                                            )}
                                            &nbsp;km
                                        </span>
                                        <span className="flex items-center gap-1">
                                            <Clock3
                                                className="h-3 w-3"
                                                aria-hidden="true"
                                            />
                                            {formatHours(impact.eta_hours)}
                                        </span>
                                    </span>
                                </span>
                                <span
                                    className={`badge shrink-0 ${token.border} ${token.bg} ${token.text}`}
                                >
                                    {t[RISK_LABEL_KEYS[level]] as string}
                                </span>
                            </button>
                        );
                    })}
                    {filtered.length === 0 ? (
                        <p className="py-8 text-center text-xs text-fg-muted">
                            {lang === "vi"
                                ? "Không tìm thấy tỉnh/thành phù hợp."
                                : "No matching province found."}
                        </p>
                    ) : null}
                </div>

                <p className="border-t border-line pt-2 text-2xs leading-4 text-fg-faint">
                    {t.impact_note}
                </p>
            </div>
        </section>
    );
};
