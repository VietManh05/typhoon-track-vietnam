"""Licensed provider adapters and conservative NCHMF bulletin parsing."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from html import unescape
from typing import Any, Callable, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from .errors import LocationNotFoundError, ProviderQuotaError, ProviderUnavailableError
from .models import (
    CurrentWeather,
    DailyForecast,
    HourlyForecast,
    Precipitation,
    SourceMetadata,
    WeatherAlert,
    WeatherCondition,
    WeatherLocation,
    Wind,
)


class WeatherProvider(Protocol):
    def current(self, location: WeatherLocation) -> CurrentWeather: ...
    def hourly(self, location: WeatherLocation) -> list[HourlyForecast]: ...
    def daily(self, location: WeatherLocation) -> list[DailyForecast]: ...
    def alerts(self, location: WeatherLocation) -> list[WeatherAlert]: ...


Transport = Callable[[str, dict[str, str], float], Any]


def _request(url: str, headers: dict[str, str], timeout: float) -> Any:
    with urlopen(Request(url, headers=headers), timeout=timeout) as response:
        return json.load(response)


def _value(item: dict[str, Any] | None) -> float | None:
    if not item or item.get("Value") is None:
        return None
    return float(item["Value"])


def _condition(icon: int | None, phrase: str) -> WeatherCondition:
    text = phrase.casefold()
    code = "cloudy"
    if "thunder" in text or "dÃƒÆ’Ã‚Â´ng" in text:
        code = "thunderstorm"
    elif "rain" in text or "mÃƒâ€ Ã‚Â°a" in text:
        code = "rain"
    elif "fog" in text or "sÃƒâ€ Ã‚Â°Ãƒâ€ Ã‚Â¡ng" in text:
        code = "fog"
    elif "sun" in text or "nÃƒÂ¡Ã‚ÂºÃ‚Â¯ng" in text or "clear" in text:
        code = "clear-day"
    elif "partly" in text:
        code = "partly-cloudy"
    return WeatherCondition(code=str(icon or code), label=phrase, icon=code)


class AccuWeatherProvider:
    """Official AccuWeather API only; never scrapes consumer pages."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://dataservice.accuweather.com",
        timeout: float = 8,
        transport: Transport = _request,
    ):
        if not api_key.strip():
            raise ProviderUnavailableError("AccuWeather API key is not configured")
        self.api_key, self.base_url, self.timeout, self.transport = (
            api_key,
            base_url.rstrip("/"),
            timeout,
            transport,
        )

    def _get(self, path: str, **params: Any) -> Any:
        params["apikey"] = self.api_key
        url = f"{self.base_url}{path}?{urlencode(params)}"
        try:
            return self.transport(
                url,
                {"Accept": "application/json", "User-Agent": "typhoon-vn/0.1"},
                self.timeout,
            )
        except HTTPError as exc:
            if exc.code == 404:
                raise LocationNotFoundError("weather location not found") from exc
            if exc.code == 429:
                raise ProviderQuotaError("weather provider quota exceeded") from exc
            raise ProviderUnavailableError(f"weather provider HTTP {exc.code}") from exc
        except (TimeoutError, URLError, OSError) as exc:
            raise ProviderUnavailableError("weather provider unavailable") from exc

    def _key(self, location: WeatherLocation) -> str:
        if location.provider_location_id:
            return location.provider_location_id
        data = self._get(
            "/locations/v1/cities/geoposition/search",
            q=f"{location.latitude},{location.longitude}",
        )
        if not data or not data.get("Key"):
            raise LocationNotFoundError("weather location not found")
        return str(data["Key"])

    def _meta(self, location: WeatherLocation, url: str) -> SourceMetadata:
        return SourceMetadata(
            source="AccuWeather official API",
            provider="accuweather",
            retrieved_at=datetime.now(UTC),
            timezone=location.timezone,
            location_id=location.id,
            source_url=url,
        )

    def current(self, location: WeatherLocation) -> CurrentWeather:
        key = self._key(location)
        path = f"/currentconditions/v1/{key}"
        rows = self._get(path, details="true", language="vi-vn")
        if not rows:
            raise LocationNotFoundError("current weather not found")
        x = rows[0]
        precip = Precipitation(rain_mm=_value(x.get("Precip1hr", {}).get("Metric")))
        return CurrentWeather(
            location=location,
            observation_time=datetime.fromisoformat(x["LocalObservationDateTime"]),
            temperature_c=_value(x.get("Temperature", {}).get("Metric")) or 0,
            feels_like_c=_value(x.get("RealFeelTemperature", {}).get("Metric")),
            condition=_condition(
                x.get("WeatherIcon"), x.get("WeatherText", "KhÃƒÆ’Ã‚Â´ng rÃƒÆ’Ã‚Âµ")
            ),
            humidity_percent=x.get("RelativeHumidity"),
            wind=Wind(
                speed_kmh=_value(x.get("Wind", {}).get("Speed", {}).get("Metric")) or 0,
                gust_kmh=_value(x.get("WindGust", {}).get("Speed", {}).get("Metric")),
                direction_deg=x.get("Wind", {}).get("Direction", {}).get("Degrees"),
                direction_label=x.get("Wind", {}).get("Direction", {}).get("Localized"),
            ),
            pressure_hpa=_value(x.get("Pressure", {}).get("Metric")),
            visibility_km=_value(x.get("Visibility", {}).get("Metric")),
            dew_point_c=_value(x.get("DewPoint", {}).get("Metric")),
            cloud_cover_percent=x.get("CloudCover"),
            uv_index=x.get("UVIndex"),
            precipitation=precip,
            metadata=self._meta(location, path),
        )

    def hourly(self, location: WeatherLocation) -> list[HourlyForecast]:
        key = self._key(location)
        path = f"/forecasts/v1/hourly/12hour/{key}"
        rows = self._get(path, details="true", metric="true", language="vi-vn")
        meta = self._meta(location, path)
        result = []
        for x in rows:
            result.append(
                HourlyForecast(
                    forecast_time=datetime.fromisoformat(x["DateTime"]),
                    temperature_c=_value(x.get("Temperature")) or 0,
                    feels_like_c=_value(x.get("RealFeelTemperature")),
                    condition=_condition(
                        x.get("WeatherIcon"),
                        x.get("IconPhrase", "KhÃƒÆ’Ã‚Â´ng rÃƒÆ’Ã‚Âµ"),
                    ),
                    precipitation=Precipitation(
                        probability_percent=x.get("PrecipitationProbability"),
                        rain_mm=_value(x.get("Rain")),
                    ),
                    humidity_percent=x.get("RelativeHumidity"),
                    wind=Wind(
                        speed_kmh=_value(x.get("Wind", {}).get("Speed")) or 0,
                        gust_kmh=_value(x.get("WindGust", {}).get("Speed")),
                        direction_deg=x.get("Wind", {})
                        .get("Direction", {})
                        .get("Degrees"),
                        direction_label=x.get("Wind", {})
                        .get("Direction", {})
                        .get("Localized"),
                    ),
                    uv_index=x.get("UVIndex"),
                    metadata=meta,
                )
            )
        return result

    def daily(self, location: WeatherLocation) -> list[DailyForecast]:
        key = self._key(location)
        path = f"/forecasts/v1/daily/5day/{key}"
        data = self._get(path, details="true", metric="true", language="vi-vn")
        meta = self._meta(location, path)
        out = []
        for x in data.get("DailyForecasts", []):
            day = x.get("Day", {})
            out.append(
                DailyForecast(
                    forecast_date=datetime.fromisoformat(x["Date"]).date(),
                    min_temperature_c=_value(x.get("Temperature", {}).get("Minimum"))
                    or 0,
                    max_temperature_c=_value(x.get("Temperature", {}).get("Maximum"))
                    or 0,
                    condition=_condition(
                        day.get("Icon"), day.get("IconPhrase", "KhÃƒÆ’Ã‚Â´ng rÃƒÆ’Ã‚Âµ")
                    ),
                    precipitation=Precipitation(
                        probability_percent=day.get("PrecipitationProbability"),
                        rain_mm=_value(day.get("Rain")),
                    ),
                    wind=Wind(
                        speed_kmh=_value(day.get("Wind", {}).get("Speed")) or 0,
                        gust_kmh=_value(day.get("WindGust", {}).get("Speed")),
                    ),
                    sunrise=(
                        datetime.fromisoformat(x["Sun"]["Rise"])
                        if x.get("Sun", {}).get("Rise")
                        else None
                    ),
                    sunset=(
                        datetime.fromisoformat(x["Sun"]["Set"])
                        if x.get("Sun", {}).get("Set")
                        else None
                    ),
                    metadata=meta,
                )
            )
        return out

    def alerts(self, location: WeatherLocation) -> list[WeatherAlert]:
        return []


def _wmo_condition(value: int | float | None) -> WeatherCondition:
    code = int(value or 0)
    if code == 0:
        icon, label = "clear-day", "Trời quang"
    elif code in {1, 2}:
        icon, label = "partly-cloudy", "Có mây rải rác"
    elif code == 3:
        icon, label = "cloudy", "Nhiều mây"
    elif code in {45, 48}:
        icon, label = "fog", "Sương mù"
    elif code in {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}:
        icon, label = "rain", "Có mưa"
    elif code in {71, 73, 75, 77, 85, 86}:
        icon, label = "snow", "Có tuyết"
    elif code in {95, 96, 99}:
        icon, label = "thunderstorm", "Mưa dông"
    else:
        icon, label = "cloudy", "Thời tiết biến đổi"
    return WeatherCondition(code=f"wmo-{code}", label=label, icon=icon)


def _local_time(value: str, timezone: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=ZoneInfo(timezone))


class OpenMeteoProvider:
    """Keyless Open-Meteo adapter for development and public previews."""

    def __init__(
        self,
        *,
        base_url: str = "https://api.open-meteo.com/v1/forecast",
        timeout: float = 8,
        transport: Transport = _request,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport

    def _get(self, location: WeatherLocation, **params: Any) -> Any:
        params.update(
            latitude=location.latitude,
            longitude=location.longitude,
            timezone=location.timezone,
        )
        url = f"{self.base_url}?{urlencode(params)}"
        try:
            return self.transport(
                url,
                {"Accept": "application/json", "User-Agent": "typhoon-vn/0.1"},
                self.timeout,
            )
        except HTTPError as exc:
            if exc.code == 429:
                raise ProviderQuotaError("weather provider quota exceeded") from exc
            if exc.code in {400, 404}:
                raise LocationNotFoundError("weather location not found") from exc
            raise ProviderUnavailableError(f"weather provider HTTP {exc.code}") from exc
        except (TimeoutError, URLError, OSError) as exc:
            raise ProviderUnavailableError("weather provider unavailable") from exc

    def _meta(self, location: WeatherLocation) -> SourceMetadata:
        return SourceMetadata(
            source="Open-Meteo forecast API",
            provider="open-meteo",
            retrieved_at=datetime.now(UTC),
            timezone=location.timezone,
            location_id=location.id,
            source_url="https://open-meteo.com/",
        )

    def current(self, location: WeatherLocation) -> CurrentWeather:
        data = self._get(
            location,
            current=(
                "temperature_2m,relative_humidity_2m,apparent_temperature,"
                "weather_code,surface_pressure,wind_speed_10m,"
                "wind_direction_10m,wind_gusts_10m,precipitation,rain,cloud_cover"
            ),
        )
        item = data.get("current") or {}
        if not item.get("time"):
            raise ProviderUnavailableError("weather provider returned no current data")
        return CurrentWeather(
            location=location,
            observation_time=_local_time(item["time"], location.timezone),
            temperature_c=float(item.get("temperature_2m", 0)),
            feels_like_c=item.get("apparent_temperature"),
            condition=_wmo_condition(item.get("weather_code")),
            humidity_percent=item.get("relative_humidity_2m"),
            wind=Wind(
                speed_kmh=float(item.get("wind_speed_10m", 0)),
                gust_kmh=item.get("wind_gusts_10m"),
                direction_deg=item.get("wind_direction_10m"),
            ),
            pressure_hpa=item.get("surface_pressure"),
            cloud_cover_percent=item.get("cloud_cover"),
            precipitation=Precipitation(
                rain_mm=item.get("rain") or item.get("precipitation")
            ),
            metadata=self._meta(location),
        )

    def hourly(self, location: WeatherLocation) -> list[HourlyForecast]:
        data = self._get(
            location,
            hourly=(
                "temperature_2m,apparent_temperature,relative_humidity_2m,"
                "precipitation_probability,rain,weather_code,surface_pressure,"
                "wind_speed_10m,wind_direction_10m,wind_gusts_10m,uv_index"
            ),
            forecast_hours=24,
        )
        hourly = data.get("hourly") or {}
        times = hourly.get("time") or []
        meta = self._meta(location)
        return [
            HourlyForecast(
                forecast_time=_local_time(value, location.timezone),
                temperature_c=float(hourly["temperature_2m"][index]),
                feels_like_c=hourly.get("apparent_temperature", [None] * len(times))[
                    index
                ],
                condition=_wmo_condition(hourly["weather_code"][index]),
                precipitation=Precipitation(
                    probability_percent=hourly.get(
                        "precipitation_probability", [None] * len(times)
                    )[index],
                    rain_mm=hourly.get("rain", [None] * len(times))[index],
                ),
                humidity_percent=hourly.get(
                    "relative_humidity_2m", [None] * len(times)
                )[index],
                wind=Wind(
                    speed_kmh=float(hourly["wind_speed_10m"][index]),
                    gust_kmh=hourly.get("wind_gusts_10m", [None] * len(times))[index],
                    direction_deg=hourly.get("wind_direction_10m", [None] * len(times))[
                        index
                    ],
                ),
                pressure_hpa=hourly.get("surface_pressure", [None] * len(times))[index],
                uv_index=hourly.get("uv_index", [None] * len(times))[index],
                metadata=meta,
            )
            for index, value in enumerate(times)
        ]

    def daily(self, location: WeatherLocation) -> list[DailyForecast]:
        data = self._get(
            location,
            daily=(
                "weather_code,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max,rain_sum,wind_speed_10m_max,"
                "wind_gusts_10m_max,sunrise,sunset"
            ),
            forecast_days=7,
        )
        daily = data.get("daily") or {}
        times = daily.get("time") or []
        meta = self._meta(location)
        return [
            DailyForecast(
                forecast_date=datetime.fromisoformat(value).date(),
                min_temperature_c=float(daily["temperature_2m_min"][index]),
                max_temperature_c=float(daily["temperature_2m_max"][index]),
                condition=_wmo_condition(daily["weather_code"][index]),
                precipitation=Precipitation(
                    probability_percent=daily.get(
                        "precipitation_probability_max", [None] * len(times)
                    )[index],
                    rain_mm=daily.get("rain_sum", [None] * len(times))[index],
                ),
                wind=Wind(
                    speed_kmh=float(daily["wind_speed_10m_max"][index]),
                    gust_kmh=daily.get("wind_gusts_10m_max", [None] * len(times))[
                        index
                    ],
                ),
                sunrise=_local_time(daily["sunrise"][index], location.timezone),
                sunset=_local_time(daily["sunset"][index], location.timezone),
                metadata=meta,
            )
            for index, value in enumerate(times)
        ]

    def alerts(self, location: WeatherLocation) -> list[WeatherAlert]:
        return []


class NchmfBulletinParser:
    """Extracts source text only; it never fabricates severity or affected regions."""

    TAGS = re.compile(r"<[^>]+>")
    SPACE = re.compile(r"\s+")

    def parse(
        self, content: str, *, source_url: str, published_at: datetime | None = None
    ) -> WeatherAlert:
        text = self.SPACE.sub(" ", unescape(self.TAGS.sub(" ", content))).strip()
        if not text:
            raise ValueError("empty NCHMF bulletin")
        title = text[:240]
        kind = "bulletin"
        checks = (
            (chr(98) + chr(227) + chr(111), "tropical_cyclone"),
            (chr(225) + "p th" + chr(7845) + "p", "tropical_depression"),
            ("m" + chr(432) + "a l" + chr(7899) + "n", "heavy_rain"),
            ("d" + chr(244) + "ng", "thunderstorm"),
            ("bi" + chr(7875) + "n", "marine"),
        )
        for token, value in checks:
            if token in text.casefold():
                kind = value
                break
        issued = published_at or datetime.now(UTC)
        meta = SourceMetadata(
            source="NCHMF bulletin",
            provider="nchmf",
            retrieved_at=datetime.now(UTC),
            timezone="Asia/Ho_Chi_Minh",
            location_id="vietnam",
            source_url=source_url,
        )
        return WeatherAlert(
            id=f"nchmf-{int(issued.timestamp())}",
            type=kind,
            severity="official",
            title=title,
            description=text,
            issued_at=issued,
            metadata=meta,
        )
