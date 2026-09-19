import json
import re
import urllib.request

routes = [
    ("/", "text/html"),
    ("/favicon.svg", "image/svg+xml"),
    ("/data/vietnam_provinces.geojson", "application/json"),
    ("/data/vietnam_islands.json", "application/json"),
    ("/health", "application/json"),
    ("/version", "application/json"),
    ("/typhoons/active", "application/json"),
]

all_ok = True
for path, expected_ct in routes:
    url = f"http://127.0.0.1:8000{path}"
    try:
        with urllib.request.urlopen(url) as resp:
            ct = resp.headers.get("content-type", "")
            status = resp.status
            data_len = len(resp.read())
            print(f"ROUTE: {path:<35} STATUS: {status} LEN: {data_len:<8} CT: {ct}")
            if status != 200:
                all_ok = False
    except Exception as e:
        print(f"ROUTE: {path:<35} ERROR: {e}")
        all_ok = False

# Also check assets referenced by index.html
with urllib.request.urlopen("http://127.0.0.1:8000/") as resp:
    html = resp.read().decode("utf-8")
    scripts = re.findall(r'src="(/assets/[^"]+)"', html)
    csss = re.findall(r'href="(/assets/[^"]+)"', html)
    for asset in scripts + csss:
        with urllib.request.urlopen(f"http://127.0.0.1:8000{asset}") as a_resp:
            print(
                f"ASSET: {asset:<35} STATUS: {a_resp.status} LEN: {len(a_resp.read())}"
            )

print("\nALL VERIFICATION CHECKS PASSED:", all_ok)
assert all_ok
