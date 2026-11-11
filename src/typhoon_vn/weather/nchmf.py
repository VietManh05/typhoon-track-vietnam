"""Bounded public NCHMF homepage ingestion; no invented observation fields."""

from __future__ import annotations

import hashlib
import re
from copy import deepcopy
from datetime import UTC, datetime, timedelta, timezone
from html.parser import HTMLParser
from threading import Lock
from time import monotonic
from urllib.error import URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from .errors import ProviderUnavailableError

HOME = "https://nchmf.gov.vn/kttvsite/"
VN = timezone(timedelta(hours=7))
MAX_BYTES = 2_000_000


def source_url(value: str) -> str:
    url = urljoin(HOME, value)
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.netloc != "nchmf.gov.vn":
        raise ValueError("NCHMF source URL must remain on the official HTTPS host")
    if not parts.path.startswith("/kttvsite/"):
        raise ValueError("NCHMF source URL outside public weather section")
    return url


class _SameHostRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        source_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_home(timeout: float = 8.0) -> bytes:
    request = Request(HOME, headers={"User-Agent": "TyphoonVN/0.1 (public weather)"})
    with build_opener(_SameHostRedirect).open(request, timeout=timeout) as response:
        source_url(response.url)
        if response.headers.get_content_type() != "text/html":
            raise ValueError("NCHMF response is not HTML")
        raw = response.read(MAX_BYTES + 1)
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError("NCHMF response is empty or too large")
    return raw


class _Homepage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.capture = None
        self.parts = []
        self.attrs = {}
        self.station = None
        self.observations = []
        self.bulletins = {}
        self.observed_at = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = values.get("class", "").split()
        if tag == "li":
            self.station = None
        if tag in ("a", "h2") or (tag == "div" and "temp-wt-city" in classes):
            self.capture = tag
            self.parts = []
            self.attrs = values

    def handle_data(self, data):
        if self.capture:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == "li":
            self.station = None
        if tag != self.capture:
            return
        text = " ".join(" ".join(self.parts).split())
        attrs = self.attrs
        self.capture = None
        if tag == "h2" and "THỜI TIẾT" in text.upper():
            stamp = re.search(r"(\d{1,2})h\s*-\s*(\d{2}/\d{2}/\d{4})", text)
            if stamp:
                self.observed_at = (
                    datetime.strptime(stamp[1] + " " + stamp[2], "%H %d/%m/%Y")
                    .replace(tzinfo=VN)
                    .isoformat()
                )
        elif tag == "a":
            try:
                url = source_url(attrs.get("href", ""))
            except ValueError:
                return
            if "name-wt-city" in attrs.get("class", "").split():
                self.station = (text, url)
            else:
                stamp = re.search(r"\((\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})\)", text)
                if stamp and re.search(r"-post\d+\.html$", url):
                    self.bulletins[url] = {
                        "id": hashlib.sha256(url.encode()).hexdigest()[:20],
                        "title": text[: stamp.start()].strip(),
                        "issuedAt": datetime.strptime(stamp[1], "%d/%m/%Y %H:%M:%S")
                        .replace(tzinfo=VN)
                        .isoformat(),
                        "sourceUrl": url,
                    }
        elif tag == "div" and self.station:
            match = re.fullmatch(r"(-?\d+(?:[.,]\d+)?)\s*°\s*C", text)
            if not match:
                raise ValueError("Unrecognized NCHMF temperature")
            temperature = float(match[1].replace(",", "."))
            if not -80 <= temperature <= 65:
                raise ValueError("NCHMF temperature outside physical range")
            name, url = self.station
            self.observations.append(
                {
                    "id": url.rsplit("/", 1)[-1].removesuffix(".html"),
                    "name": name,
                    "temperatureC": temperature,
                    "sourceUrl": url,
                }
            )
            self.station = None


def parse_home(raw: bytes, *, retrieved_at: datetime | None = None) -> dict:
    if not raw or len(raw) > MAX_BYTES:
        raise ValueError("NCHMF response is empty or too large")
    parser = _Homepage()
    parser.feed(raw.decode("utf-8-sig"))
    parser.close()
    if not parser.observations or parser.observed_at is None:
        raise ValueError("NCHMF weather markup or observation time missing")
    now = retrieved_at or datetime.now(UTC)
    if now.utcoffset() is None:
        raise ValueError("retrieved_at must be timezone-aware")
    observed = datetime.fromisoformat(parser.observed_at)
    if observed > now + timedelta(hours=1):
        raise ValueError("NCHMF observation time is in the future")
    observations = list({x["id"]: x for x in parser.observations}.values())
    return {
        "observedAt": parser.observed_at,
        "observations": observations,
        "bulletins": sorted(
            parser.bulletins.values(), key=lambda x: x["issuedAt"], reverse=True
        ),
        "metadata": {
            "provider": "nchmf",
            "source": "Trung tâm Dự báo KTTV quốc gia",
            "sourceUrl": HOME,
            "retrievedAt": now.isoformat(),
            "timezone": "Asia/Ho_Chi_Minh",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "isStale": now - observed > timedelta(hours=6),
            "scope": "Public homepage observations and bulletin links",
        },
    }


class NchmfService:
    """One homepage request per TTL; failures back off and label cached data."""

    def __init__(self, *, transport=fetch_home, ttl=600, timeout=8.0):
        self.transport, self.ttl, self.timeout = transport, ttl, timeout
        self.lock = Lock()
        self.value = None
        self.expires = 0.0
        self.retry_after = 0.0

    def get(self) -> dict:
        with self.lock:
            now = monotonic()
            if self.value is not None and now < self.expires:
                result = deepcopy(self.value)
                observed = datetime.fromisoformat(result["observedAt"])
                result["metadata"]["isStale"] |= datetime.now(
                    UTC
                ) - observed > timedelta(hours=6)
                return result
            if now >= self.retry_after:
                try:
                    value = parse_home(self.transport(self.timeout))
                except (OSError, URLError, ValueError) as exc:
                    self.retry_after = monotonic() + 60
                    if self.value is None:
                        raise ProviderUnavailableError(
                            "NCHMF unavailable or schema changed"
                        ) from exc
                else:
                    self.value, self.expires = value, monotonic() + self.ttl
                    self.retry_after = 0.0
                    return deepcopy(value)
            if self.value is None:
                raise ProviderUnavailableError("NCHMF retry backoff active")
            result = deepcopy(self.value)
            result["metadata"]["isStale"] = True
            return result
