import { useEffect, useRef, useState } from "react";
import { MapPin, Search } from "lucide-react";
import { Language } from "../../i18n";
import { WeatherLocation } from "../../types";

interface Props {
    lang: Language;
    locations: WeatherLocation[];
    onSelect: (id: string) => void;
}

const normalize = (value: string) => value
    .toLocaleLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d");

export function MapLocationSearch({ lang, locations, onSelect }: Props) {
    const [query, setQuery] = useState("");
    const [open, setOpen] = useState(false);
    const rootRef = useRef<HTMLDivElement>(null);
    const vi = lang === "vi";
    const results = query.trim()
        ? locations.filter((item) => normalize(`${item.name} ${item.province ?? ""}`).includes(normalize(query.trim()))).slice(0, 8)
        : [];

    useEffect(() => {
        const closeOnOutsidePress = (event: PointerEvent) => {
            if (!rootRef.current?.contains(event.target as Node)) setOpen(false);
        };
        document.addEventListener("pointerdown", closeOnOutsidePress);
        return () => document.removeEventListener("pointerdown", closeOnOutsidePress);
    }, []);

    const select = (id: string) => {
        onSelect(id);
        setQuery("");
        setOpen(false);
    };

    return (
        <div className="map-location-search" ref={rootRef} role="search">
            <label htmlFor="map-location-query" className="map-location-field">
                <Search size={17} aria-hidden="true" />
                <input
                    id="map-location-query"
                    type="search"
                    autoComplete="off"
                    value={query}
                    placeholder={vi ? "Tìm địa điểm thời tiết..." : "Find a weather location..."}
                    aria-label={vi ? "Tìm địa điểm thời tiết trên bản đồ" : "Find a weather location on the map"}
                    aria-controls="map-location-results"
                    aria-expanded={open && !!query.trim()}
                    onChange={(event) => { setQuery(event.target.value); setOpen(true); }}
                    onFocus={() => setOpen(true)}
                    onKeyDown={(event) => {
                        if (event.key === "Escape") setOpen(false);
                        if (event.key === "ArrowDown" && results.length) {
                            event.preventDefault();
                            rootRef.current?.querySelector<HTMLButtonElement>(".map-location-results button")?.focus();
                        }
                        if (event.key === "Enter" && results.length) {
                            event.preventDefault();
                            select(results[0].id);
                        }
                    }}
                />
            </label>
            {open && query.trim() && (
                <div id="map-location-results" className="map-location-results">
                    {results.length ? results.map((item) => (
                        <button type="button" key={item.id} onClick={() => select(item.id)}>
                            <MapPin size={15} aria-hidden="true" />
                            <span>{item.name}</span>
                        </button>
                    )) : <p>{vi ? "Không có địa điểm phù hợp." : "No matching location."}</p>}
                </div>
            )}
        </div>
    );
}
