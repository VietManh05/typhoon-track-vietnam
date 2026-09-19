import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ChevronDown } from 'lucide-react';
import { Language, translations } from '../i18n';

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
  const [contentHeight, setContentHeight] = useState<number | undefined>(undefined);
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
    // Re-measure on window resize
    window.addEventListener('resize', measureHeight);
    return () => window.removeEventListener('resize', measureHeight);
  }, [measureHeight, children]);

  const headerId = `${id}-header`;
  const panelId = `${id}-panel`;

  return (
    <div className="animate-fade-in-up">
      {/* Collapsible header — only interactive on mobile */}
      <button
        id={headerId}
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between gap-2 px-3 py-2 rounded-t-lg bg-slate-900/60 border border-slate-800 text-xs font-bold text-slate-200 uppercase tracking-wider font-display lg:hidden transition hover:bg-slate-800/60 focus-ring"
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
          className={`w-4 h-4 text-slate-400 transition-transform duration-300 ${
            effectiveOpen ? 'rotate-180' : ''
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
        className="collapsible-content lg:!max-h-none lg:!opacity-100"
        style={{
          maxHeight: effectiveOpen ? (contentHeight ? `${contentHeight}px` : '2000px') : '0px',
        }}
      >
        {children}
      </div>
    </div>
  );
};
