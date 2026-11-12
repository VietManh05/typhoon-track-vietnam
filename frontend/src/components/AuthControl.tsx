import React, { useEffect, useRef, useState } from "react";
import { clearCredentials, loginWithKey, loginWithPassword } from "../services/api";
import { Language } from "../i18n";
import { LogIn } from "lucide-react";

export function AuthControl({ lang, onAuthenticated }: {
    lang: Language; onAuthenticated: () => void | Promise<void>;
}) {
    const dialog = useRef<HTMLDialogElement>(null);
    const [mode, setMode] = useState<"password" | "key">("password");
    const [username, setUsername] = useState("");
    const [secret, setSecret] = useState("");
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");
    const [available, setAvailable] = useState(false);
    const vi = lang === "vi";
    useEffect(() => {
        const controller = new AbortController();
        fetch("/auth/capabilities", { signal: controller.signal })
            .then(async (response) => response.ok ? response.json() : null)
            .then((payload) => { if (!controller.signal.aborted) setAvailable(payload?.available === true); })
            .catch(() => { if (!controller.signal.aborted) setAvailable(false); });
        return () => controller.abort();
    }, []);
    const close = () => { setSecret(""); setError(""); dialog.current?.close(); };
    const submit = async (event: React.FormEvent) => {
        event.preventDefault();
        setBusy(true); setError("");
        try {
            if (mode === "key") await loginWithKey(secret);
            else await loginWithPassword(username, secret);
            close();
            await onAuthenticated();
        } catch (cause) {
            setError(cause instanceof Error ? cause.message : "Login failed");
        } finally { setBusy(false); }
    };
    if (!available) return null;
    return <>
        <button type="button" className="btn auth-trigger" onClick={() => dialog.current?.showModal()}>
            <LogIn size={16} aria-hidden="true" />
            {vi ? "Đăng nhập" : "Sign in"}
        </button>
        <dialog ref={dialog} onCancel={() => setSecret("")} aria-labelledby="auth-title"
            className="m-auto w-[min(90vw,380px)] rounded-xl border border-line bg-page p-5 text-fg backdrop:bg-black/60">
            <form onSubmit={submit} className="flex flex-col gap-4">
                <h2 id="auth-title" className="text-lg font-semibold">{vi ? "Đăng nhập" : "Sign in"}</h2>
                <label>{vi ? "Phương thức" : "Method"}
                    <select value={mode} onChange={event => { setMode(event.target.value as "password" | "key"); setSecret(""); }} className="w-full rounded border border-line bg-surface p-2">
                        <option value="password">{vi ? "Tài khoản" : "Account"}</option>
                        <option value="key">API key</option>
                    </select>
                </label>
                {mode === "password" && <label>{vi ? "Tên đăng nhập" : "Username"}
                    <input required autoComplete="username" value={username} onChange={e => setUsername(e.target.value)} className="w-full rounded border border-line bg-surface p-2" />
                </label>}
                <label>{mode === "key" ? "API key" : vi ? "Mật khẩu" : "Password"}
                    <input required type="password" autoComplete={mode === "key" ? "off" : "current-password"} value={secret} onChange={e => setSecret(e.target.value)} className="w-full rounded border border-line bg-surface p-2" />
                </label>
                {error && <p role="alert" className="text-danger">{error}</p>}
                <button type="submit" disabled={busy} className="btn-primary">{busy ? "…" : vi ? "Đăng nhập" : "Sign in"}</button>
                <button type="button" disabled={busy} onClick={async () => { clearCredentials(); close(); await onAuthenticated(); }} className="btn-ghost">{vi ? "Đăng xuất" : "Sign out"}</button>
                <button type="button" disabled={busy} onClick={close} className="btn-ghost">{vi ? "Đóng" : "Close"}</button>
            </form>
        </dialog>
    </>;
}
