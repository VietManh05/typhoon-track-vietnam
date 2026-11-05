import React, { useEffect, useId, useRef, useState } from "react";
import { createPortal } from "react-dom";
import {
    BellRing,
    Check,
    Info,
    LoaderCircle,
    MapPin,
    Radar,
    X,
} from "lucide-react";
import { Language, translations } from "../i18n";
import { authHeaders } from "../services/api";

interface AlertModalProps {
    isOpen: boolean;
    onClose: () => void;
    lang: Language;
    available: boolean;
    loadingCapability: boolean;
    unavailableReason: string | null;
}

interface ApiErrorPayload {
    detail?: string;
    error?: { message?: string };
}

const focusableSelector =
    'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [href], [tabindex]:not([tabindex="-1"])';

export const AlertModal: React.FC<AlertModalProps> = ({
    isOpen,
    onClose,
    lang,
    available,
    loadingCapability,
    unavailableReason,
}) => {
    const [label, setLabel] = useState("Trạm Cảnh báo ven biển");
    const [lat, setLat] = useState("16.05");
    const [lon, setLon] = useState("108.20");
    const [radius, setRadius] = useState("250");
    const [submitted, setSubmitted] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const dialogRef = useRef<HTMLDivElement>(null);
    const initialFocusRef = useRef<HTMLInputElement>(null);
    const returnFocusRef = useRef<HTMLElement | null>(null);
    const titleId = useId();
    const descriptionId = useId();
    const errorId = useId();
    const t = translations[lang];

    useEffect(() => {
        if (!isOpen) return;
        returnFocusRef.current = document.activeElement as HTMLElement | null;
        const previousOverflow = document.body.style.overflow;
        document.body.style.overflow = "hidden";
        window.requestAnimationFrame(() => initialFocusRef.current?.focus());

        return () => {
            document.body.style.overflow = previousOverflow;
            returnFocusRef.current?.focus();
        };
    }, [isOpen]);

    useEffect(() => {
        if (!isOpen) return;

        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === "Escape" && !loading) {
                event.preventDefault();
                onClose();
                return;
            }
            if (event.key !== "Tab" || !dialogRef.current) return;

            const focusable = Array.from(
                dialogRef.current.querySelectorAll<HTMLElement>(focusableSelector),
            );
            if (focusable.length === 0) return;
            const first = focusable[0];
            const last = focusable[focusable.length - 1];

            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
                event.preventDefault();
                first.focus();
            }
        };

        document.addEventListener("keydown", handleKeyDown);
        return () => document.removeEventListener("keydown", handleKeyDown);
    }, [isOpen, loading, onClose]);

    if (!isOpen) return null;

    const readApiError = async (response: Response): Promise<string> => {
        try {
            const payload = (await response.json()) as ApiErrorPayload;
            return (
                payload.error?.message ||
                payload.detail ||
                (lang === "vi"
                    ? "Không thể lưu đăng ký. Vui lòng thử lại."
                    : "Could not save the subscription. Please try again.")
            );
        } catch {
            return lang === "vi"
                ? `Không thể lưu đăng ký (HTTP ${response.status}).`
                : `Could not save subscription (HTTP ${response.status}).`;
        }
    };

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await fetch("/subscriptions", {
                method: "POST",
                headers: { "Content-Type": "application/json", ...authHeaders() },
                body: JSON.stringify({
                    label: label.trim(),
                    lat: Number(lat),
                    lon: Number(lon),
                    radius_km: Number(radius),
                    lead_hours: 72,
                    cooldown_hours: 12,
                }),
            });

            if (!response.ok) throw new Error(await readApiError(response));
            setSubmitted(true);
        } catch (caught) {
            setError(
                caught instanceof Error
                    ? caught.message
                    : lang === "vi"
                      ? "Không thể kết nối dịch vụ cảnh báo."
                      : "Could not connect to the alert service.",
            );
        } finally {
            setLoading(false);
        }
    };

    return createPortal(
        <div
            className="fixed inset-0 z-[2000] flex items-center justify-center overflow-y-auto bg-slate-950/55 px-4 py-6 backdrop-blur-[2px] sm:px-6"
            onMouseDown={(event) => {
                if (event.target === event.currentTarget && !loading) onClose();
            }}
        >
            <div
                ref={dialogRef}
                role="dialog"
                aria-modal="true"
                aria-labelledby={titleId}
                aria-describedby={descriptionId}
                className="relative my-auto w-full max-w-[540px] overflow-hidden rounded-panel border border-line-strong bg-surface shadow-[0_24px_80px_-20px_rgba(2,6,23,0.75)]"
            >
                <header className="flex items-start gap-4 border-b border-line bg-surface-2/65 px-5 py-5 pr-16 sm:px-6">
                    <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-card border border-primary/25 bg-primary/10 text-primary">
                        <BellRing className="h-5 w-5" aria-hidden="true" />
                    </div>
                    <div className="min-w-0">
                        <div className="section-label mb-1">TYPHOON VN ALERTS</div>
                        <h2 id={titleId} className="text-lg font-bold text-fg">
                            {t.subscribe_alerts}
                        </h2>
                        <p
                            id={descriptionId}
                            className="mt-1 text-xs leading-5 text-fg-muted"
                        >
                            {lang === "vi"
                                ? "Theo dõi nguy cơ bão đi vào bán kính bạn thiết lập."
                                : "Monitor when a tropical cyclone enters your configured radius."}
                        </p>
                    </div>
                </header>

                <button
                    type="button"
                    onClick={onClose}
                    disabled={loading}
                    className="btn-icon absolute right-4 top-4 z-10 border-transparent bg-transparent"
                    aria-label={t.alert_close}
                    title={t.alert_close}
                >
                    <X className="h-[18px] w-[18px]" aria-hidden="true" />
                </button>

                {submitted ? (
                    <div className="flex flex-col items-center px-6 py-10 text-center">
                        <div className="flex h-14 w-14 items-center justify-center rounded-full border border-success/30 bg-success/10 text-success">
                            <Check className="h-7 w-7" aria-hidden="true" />
                        </div>
                        <h3 className="mt-4 text-base font-bold text-fg">
                            {t.alert_success_title}
                        </h3>
                        <p className="mt-2 max-w-sm text-sm leading-6 text-fg-muted">
                            {t.alert_success_desc}
                        </p>
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn-primary mt-6 min-w-32"
                        >
                            {t.alert_close}
                        </button>
                    </div>
                ) : loadingCapability || !available ? (
                    <div className="space-y-4 p-5 sm:p-6">
                        <div role="status" className="flex items-start gap-3 rounded-card bg-warning/10 p-4 text-sm leading-6 text-fg ring-1 ring-inset ring-warning/25">
                            <Info className="mt-0.5 h-5 w-5 shrink-0 text-warning" aria-hidden="true" />
                            <div>
                                <p className="font-semibold">{loadingCapability
                                    ? (lang === "vi" ? "Đang kiểm tra dịch vụ cảnh báo…" : "Checking alert service…")
                                    : (lang === "vi" ? "Dịch vụ cảnh báo chưa khả dụng" : "Alert service is unavailable")}</p>
                                <p className="mt-1 text-fg-muted">{loadingCapability
                                    ? (lang === "vi" ? "Vui lòng đợi trong giây lát." : "Please wait a moment.")
                                    : (unavailableReason || (lang === "vi"
                                        ? "Bản triển khai hiện tại chưa kết nối backend lưu đăng ký và gửi cảnh báo. Chuông vẫn hoạt động để hiển thị trạng thái này; hệ thống chưa nhận đăng ký của bạn."
                                        : "This deployment is not connected to a backend that stores subscriptions and sends alerts. No subscription has been received."))}</p>
                            </div>
                        </div>
                        {!loadingCapability && (
                            <a
                                href="https://nchmf.gov.vn/kttv/vi-VN/1/bao-ap-thap-nhiet-doi-2049-15.html"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="inline-flex min-h-11 items-center rounded-control px-2 text-sm font-semibold text-primary underline underline-offset-4 focus-ring"
                            >
                                {lang === "vi" ? "Xem bản tin bão và áp thấp nhiệt đới từ NCHMF" : "View official NCHMF tropical cyclone bulletins"}
                            </a>
                        )}
                        <footer className="flex justify-end border-t border-line pt-4">
                            <button type="button" onClick={onClose} className="btn-primary min-w-24">{t.alert_close}</button>
                        </footer>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="space-y-5 p-5 sm:p-6">
                        <div>
                            <label
                                htmlFor="alert-label"
                                className="mb-2 block text-xs font-semibold text-fg"
                            >
                                {t.alert_subscription_label}
                            </label>
                            <input
                                ref={initialFocusRef}
                                id="alert-label"
                                type="text"
                                value={label}
                                onChange={(event) => setLabel(event.target.value)}
                                minLength={2}
                                maxLength={120}
                                required
                                aria-describedby={error ? errorId : undefined}
                                className="input focus-ring h-11"
                                placeholder={
                                    lang === "vi"
                                        ? "Ví dụ: Nhà riêng Đà Nẵng"
                                        : "Example: Da Nang residence"
                                }
                            />
                        </div>

                        <fieldset>
                            <legend className="mb-2 flex items-center gap-2 text-xs font-semibold text-fg">
                                <MapPin
                                    className="h-4 w-4 text-primary"
                                    aria-hidden="true"
                                />
                                {lang === "vi"
                                    ? "Tọa độ khu vực giám sát"
                                    : "Monitoring location"}
                            </legend>
                            <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                                <div className="relative">
                                    <label
                                        htmlFor="alert-lat"
                                        className="mb-1.5 block text-xs text-fg-muted"
                                    >
                                        {t.alert_lat}
                                    </label>
                                    <input
                                        id="alert-lat"
                                        type="number"
                                        step="0.01"
                                        min="-90"
                                        max="90"
                                        inputMode="decimal"
                                        value={lat}
                                        onChange={(event) =>
                                            setLat(event.target.value)
                                        }
                                        required
                                        className="input focus-ring h-11 pr-9 font-mono"
                                    />
                                    <span className="pointer-events-none absolute bottom-3 right-3 text-xs text-fg-faint">
                                        °
                                    </span>
                                </div>
                                <div className="relative">
                                    <label
                                        htmlFor="alert-lon"
                                        className="mb-1.5 block text-xs text-fg-muted"
                                    >
                                        {t.alert_lon}
                                    </label>
                                    <input
                                        id="alert-lon"
                                        type="number"
                                        step="0.01"
                                        min="-180"
                                        max="180"
                                        inputMode="decimal"
                                        value={lon}
                                        onChange={(event) =>
                                            setLon(event.target.value)
                                        }
                                        required
                                        className="input focus-ring h-11 pr-9 font-mono"
                                    />
                                    <span className="pointer-events-none absolute bottom-3 right-3 text-xs text-fg-faint">
                                        °
                                    </span>
                                </div>
                            </div>
                        </fieldset>

                        <div className="relative">
                            <label
                                htmlFor="alert-radius"
                                className="mb-1.5 flex items-center gap-2 text-xs font-semibold text-fg"
                            >
                                <Radar
                                    className="h-4 w-4 text-primary"
                                    aria-hidden="true"
                                />
                                {t.alert_radius}
                            </label>
                            <input
                                id="alert-radius"
                                type="number"
                                min="10"
                                max="2000"
                                step="10"
                                inputMode="numeric"
                                value={radius}
                                onChange={(event) => setRadius(event.target.value)}
                                required
                                className="input focus-ring h-11 pr-14 font-mono"
                            />
                            <span className="pointer-events-none absolute bottom-3 right-3 text-xs text-fg-faint">
                                km
                            </span>
                            <p className="mt-1.5 text-[11px] leading-4 text-fg-faint">
                                {lang === "vi"
                                    ? "Phạm vi hợp lệ từ 10 đến 2.000 km."
                                    : "Valid range from 10 to 2,000 km."}
                            </p>
                        </div>

                        <div className="flex items-start gap-3 rounded-card bg-primary/[0.06] p-3 text-xs leading-5 text-fg-muted ring-1 ring-inset ring-primary/15">
                            <Info
                                className="mt-0.5 h-4 w-4 shrink-0 text-primary"
                                aria-hidden="true"
                            />
                            <span>{t.alert_delivery_note}</span>
                        </div>

                        {error && (
                            <div
                                id={errorId}
                                role="alert"
                                className="rounded-card bg-danger/10 px-3 py-2.5 text-xs leading-5 text-danger ring-1 ring-inset ring-danger/25"
                            >
                                {error}
                            </div>
                        )}

                        <footer className="flex flex-col-reverse gap-2 border-t border-line pt-4 sm:flex-row sm:justify-end">
                            <button
                                type="button"
                                onClick={onClose}
                                disabled={loading}
                                className="btn-ghost sm:min-w-24"
                            >
                                {lang === "vi" ? "Hủy" : "Cancel"}
                            </button>
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn-primary sm:min-w-44"
                            >
                                {loading ? (
                                    <>
                                        <LoaderCircle
                                            className="h-4 w-4 animate-spin"
                                            aria-hidden="true"
                                        />
                                        {t.alert_submitting}
                                    </>
                                ) : (
                                    <>
                                        <BellRing
                                            className="h-4 w-4"
                                            aria-hidden="true"
                                        />
                                        {t.alert_submit}
                                    </>
                                )}
                            </button>
                        </footer>
                    </form>
                )}
            </div>
        </div>,
        document.body,
    );
};
