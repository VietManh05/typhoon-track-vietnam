"""Check public map controls for overlap in headless Chrome without paid services."""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen

from websockets.sync.client import connect

CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
URL = "https://baoviet2026.pages.dev/"
ROOT = Path(__file__).resolve().parents[1]


def chrome_port(profile: Path) -> int:
    port_file = profile / "DevToolsActivePort"
    for _ in range(100):
        if port_file.exists():
            return int(port_file.read_text().splitlines()[0])
        time.sleep(0.1)
    raise RuntimeError("Chrome DevTools did not start")


class DevTools:
    def __init__(self, socket):
        self.socket = socket
        self.next_id = 0

    def call(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        message_id = self.next_id
        self.socket.send(
            json.dumps({"id": message_id, "method": method, "params": params or {}})
        )
        while True:
            message = json.loads(self.socket.recv(timeout=20))
            if message.get("id") == message_id:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message.get("result", {})

    def evaluate(self, expression: str):
        result = self.call(
            "Runtime.evaluate", {"expression": expression, "returnByValue": True}
        )
        if "exceptionDetails" in result:
            raise RuntimeError(result["exceptionDetails"])
        return result["result"].get("value")


GEOMETRY = """(() => {
  const selectors = ['.map-layer-toolbar', '.map-location-search', '.map-navigation'];
  const rect = (selector) => {
    const element = document.querySelector(selector);
    if (!element || getComputedStyle(element).visibility === 'hidden') return null;
    const r = element.getBoundingClientRect();
    return {left:r.left, right:r.right, top:r.top, bottom:r.bottom};
  };
  return Object.fromEntries(selectors.map(selector => [selector, rect(selector)]));
})()"""


def overlap(first: dict, second: dict) -> bool:
    return (
        first["left"] < second["right"]
        and second["left"] < first["right"]
        and first["top"] < second["bottom"]
        and second["top"] < first["bottom"]
    )


def main() -> None:
    if not CHROME.exists():
        raise RuntimeError(f"Chrome not found: {CHROME}")
    with tempfile.TemporaryDirectory(prefix="typhoon-ui-qa-") as profile_name:
        profile = Path(profile_name)
        process = subprocess.Popen(
            [
                str(CHROME),
                "--headless=new",
                "--disable-gpu",
                "--disable-background-networking",
                "--disable-extensions",
                "--no-first-run",
                "--no-default-browser-check",
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
                browser.call(
                    "Emulation.setDeviceMetricsOverride",
                    {
                        "width": 390,
                        "height": 844,
                        "deviceScaleFactor": 1,
                        "mobile": True,
                    },
                )
                browser.call("Page.navigate", {"url": URL})
                for _ in range(100):
                    if browser.evaluate(
                        "Boolean(document.querySelector('.map-toolbar-toggle'))"
                    ):
                        break
                    time.sleep(0.2)
                else:
                    raise RuntimeError("Map controls did not render")
                results = []
                status = browser.evaluate(
                    """(() => ({
                      badge: document.querySelector('.desktop-control')?.textContent?.trim(),
                      alertDisabled: document.querySelector('.header-alert-trigger')?.disabled,
                      loginHidden: !document.querySelector('.auth-trigger')
                    }))()"""
                )
                results.append(
                    {
                        "check": "demo-capabilities",
                        "pass": status
                        == {
                            "badge": "DEMO",
                            "alertDisabled": True,
                            "loginHidden": True,
                        },
                        "status": status,
                    }
                )
                for width in (320, 390, 430, 768, 1024, 1440):
                    browser.call(
                        "Emulation.setDeviceMetricsOverride",
                        {
                            "width": width,
                            "height": 844,
                            "deviceScaleFactor": 1,
                            "mobile": width < 768,
                        },
                    )
                    time.sleep(0.2)
                    states = (False, True) if width < 768 else (True,)
                    for expanded in states:
                        current = browser.evaluate(
                            "document.querySelector('.map-toolbar-toggle').getAttribute('aria-expanded') === 'true'"
                        )
                        if current != expanded:
                            browser.evaluate(
                                "document.querySelector('.map-toolbar-toggle').click()"
                            )
                            time.sleep(0.1)
                        geometry = browser.evaluate(GEOMETRY)
                        toolbar = geometry[".map-layer-toolbar"]
                        search = geometry[".map-location-search"]
                        navigation = geometry[".map-navigation"]
                        passed = (
                            bool(toolbar and search and navigation)
                            and not overlap(toolbar, search)
                            and not overlap(search, navigation)
                        )
                        results.append(
                            {
                                "check": "map-controls",
                                "width": width,
                                "expanded": expanded,
                                "pass": passed,
                                "geometry": geometry,
                            }
                        )
                evidence = ROOT / "reports" / "demo-ui-smoke-2026-09-23.json"
                evidence.parent.mkdir(parents=True, exist_ok=True)
                evidence.write_text(
                    json.dumps(
                        {
                            "url": URL,
                            "checkedAt": datetime.now(timezone.utc).isoformat(),
                            "passed": all(row["pass"] for row in results),
                            "results": results,
                        },
                        indent=2,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                print(
                    f"{sum(row['pass'] for row in results)}/{len(results)} UI checks passed; {evidence}"
                )
                if not all(row["pass"] for row in results):
                    raise SystemExit(1)
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()


if __name__ == "__main__":
    main()
