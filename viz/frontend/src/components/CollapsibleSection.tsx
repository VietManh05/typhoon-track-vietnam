import React, { useState, useRef, useEffect, useCallback } from "react";
import { ChevronDown } from "lucide-react";
import { Language, translations } from "../i18n";

interface CollapsibleSectionProps {
    title: string;
    icon?: React.ReactNode;
    badge?: React.ReactNode;
    defaultOpen?: boolean;
    /** Force open regardless of internal state (for desktop) */
    forceOpen?: boolean;
    lang: Language;
    children: React.ReactNode;
    id: string;
}

export const CollapsibleSection: React.FC<CollapsibleSectionProps> = ({
    title,
    icon,
    badge,
    defaultOpen = true,
    forceOpen,
    lang,
    children,
    id,
}) => {
    const [isOpen, setIsOpen] = useState(defaultOpen);
    const contentRef = useRef<HTMLDivElement>(null);
    const [contentHeight, setContentHeight] = useState<number | undefined>(
        undefined,
    );
    const t = translations[lang];

    const effectiveOpen = forceOpen !== undefined ? forceOpen : isOpen;

    // Measure content height for smooth animation
    const measureHeight = useCallback(() => {
        if (contentRef.current) {
            setContentHeight(contentRef.current.scrollHeight);
        }
    }, []);

    useEffect(() => {
        measureHeight();
        const element = contentRef.current;
        const observer = element ? new ResizeObserver(measureHeight) : null;
        if (element) observer?.observe(element);
        window.addEventListener("resize", measureHeight);
        return () => {
            observer?.disconnect();
            window.removeEventListener("resize", measureHeight);
        };
    }, [measureHeight, children]);

    const headerId = `${id}-header`;
    const panelId = `${id}-panel`;

    return (
        <div className="collapsible-section animate-fade-in-up">
            {/* Collapsible header — only interactive on mobile */}
            <button
                id={headerId}
                onClick={() => setIsOpen(!isOpen)}
                className={`collapsible-trigger flex min-h-11 w-full items-center justify-between gap-2 border border-line bg-surface-2/70 px-3 py-2 text-sm font-semibold text-fg transition-colors hover:bg-surface-3/70 focus-ring ${effectiveOpen ? "rounded-t-card" : "rounded-card"}`}
                aria-expanded={effectiveOpen}
                aria-controls={panelId}
                title={effectiveOpen ? t.collapse : t.expand}
            >
                <div className="flex items-center gap-2">
                    {icon}
                    <span>{title}</span>
                    {badge}
                </div>
                <ChevronDown
                    className={`h-4 w-4 text-fg-muted transition-transform duration-base ${
                        effectiveOpen ? "rotate-180" : ""
                    }`}
                />
            </button>

            {/* Content area */}
            <div
                id={panelId}
                ref={contentRef}
                role="region"
                aria-labelledby={headerId}
                aria-hidden={!effectiveOpen}
                className="collapsible-content"
                hidden={!effectiveOpen}
                style={{
                    maxHeight: effectiveOpen
                        ? contentHeight
                            ? `${contentHeight}px`
                            : "2000px"
                        : "0px",
                }}
            >
                {children}
            </div>
        </div>
    );
};
