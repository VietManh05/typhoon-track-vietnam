"""Check the public storm badge and alert dialog in an isolated Chrome profile."""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.request import urlopen

from verify_demo_ui import CHROME, DevTools, chrome_port
from websockets.sync.client import connect

URL = "https://baoviet2026.pages.dev/"


def main() -> None:
    if not CHROME.is_file():
        raise RuntimeError(f"Chrome not found: {CHROME}")
    with tempfile.TemporaryDirectory(prefix="typhoon-live-ui-") as temporary:
        profile = Path(temporary)
        process = subprocess.Popen(
            [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--disable-background-networking",
                "--disable-extensions",
                "--no-first-run",
                "--remote-debugging-port=0",
                "--remote-allow-origins=*",
                f"--user-data-dir={profile}",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        try:
            port = chrome_port(profile)
            pages = json.load(urlopen(f"http://127.0.0.1:{port}/json", timeout=5))
            page = next(item for item in pages if item["type"] == "page")
            with connect(page["webSocketDebuggerUrl"], open_timeout=10) as socket:
                browser = DevTools(socket)
                browser.call("Page.enable")
                browser.call("Runtime.enable")
                browser.call("Page.navigate", {"url": URL})
                state = None
                for _ in range(100):
                    state = browser.evaluate(
                        """(() => ({
                            badge: document.querySelector('.desktop-control')?.textContent?.trim(),
                            alertButton: !!document.querySelector('.header-alert-trigger:not(:disabled)'),
                        }))()"""
                    )
                    if (
                        state
                        and state.get("badge") == "BÃO LIVE"
                        and state.get("alertButton")
                    ):
                        break
                    time.sleep(0.2)
                else:
                    raise RuntimeError(
                        f"Live badge or alert button unavailable: {state}"
                    )
                browser.evaluate(
                    "document.querySelector('.header-alert-trigger').click()"
                )
                for _ in range(50):
                    dialog = browser.evaluate(
                        """(() => ({
                            open: !!document.querySelector('[role="dialog"][aria-modal="true"]'),
                            text: document.querySelector('[role="dialog"]')?.textContent || '',
                            form: !!document.querySelector('[role="dialog"] form'),
                        }))()"""
                    )
                    if dialog["open"] and "NCHMF" in dialog["text"]:
                        break
                    time.sleep(0.2)
                else:
                    raise RuntimeError(
                        f"Alert dialog did not show NCHMF fallback: {dialog}"
                    )
                if dialog["form"]:
                    raise RuntimeError(
                        "Unavailable alert delivery exposed a subscription form"
                    )
                browser.evaluate(
                    "document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true}))"
                )
                for _ in range(25):
                    if not browser.evaluate(
                        "Boolean(document.querySelector('[role=dialog]'))"
                    ):
                        break
                    time.sleep(0.1)
                else:
                    raise RuntimeError("Alert dialog did not close with Escape")
                browser.call(
                    "Emulation.setDeviceMetricsOverride",
                    {
                        "width": 390,
                        "height": 844,
                        "deviceScaleFactor": 1,
                        "mobile": True,
                    },
                )
                time.sleep(0.2)
                mobile = browser.evaluate(
                    """(() => {
                        const button = document.querySelector('.header-alert-trigger');
                        const r = button?.getBoundingClientRect();
                        if (!r) return null;
                        const hit = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2);
                        return {width:r.width, height:r.height, hittable:hit === button || button.contains(hit)};
                    })()"""
                )
                if (
                    not mobile
                    or mobile["width"] < 40
                    or mobile["height"] < 40
                    or not mobile["hittable"]
                ):
                    raise RuntimeError(
                        f"Mobile alert button is blocked or too small: {mobile}"
                    )
                print(
                    json.dumps(
                        {
                            "url": URL,
                            "badge": state["badge"],
                            "alert_dialog": "unavailable with NCHMF link",
                            "mobile_alert_button": mobile,
                            "pass": True,
                        },
                        ensure_ascii=False,
                    )
                )
        finally:
            process.terminate()
            process.wait(timeout=10)


if __name__ == "__main__":
    main()
