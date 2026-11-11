"""Weather contracts and provider/API failure behavior."""

from datetime import UTC, datetime
from urllib.error import HTTPError

import pytest
from fastapi.testclient import TestClient

from typhoon_vn.api.app import create_app
from typhoon_vn.settings import Settings
from typhoon_vn.weather.errors import (
    LocationNotFoundError,
    ProviderQuotaError,
    ProviderUnavailableError,
)
from typhoon_vn.weather.locations import BY_ID, LOCATIONS, search_locations
from typhoon_vn.weather.models import SourceMetadata, WeatherLocation
from typhoon_vn.weather.providers import (
    AccuWeatherProvider,
    NchmfBulletinParser,
    OpenMeteoProvider,
)


@pytest.mark.parametrize(
    "location_id", ["da-nang", "ha-noi", "ho-chi-minh", "hai-phong", "hue", "an-giang"]
)
def test_supported_vietnam_locations(location_id):
    location = BY_ID[location_id]
    assert location.timezone == "Asia/Ho_Chi_Minh"
    assert -90 <= location.latitude <= 90
    assert -180 <= location.longitude <= 180


def test_location_search_and_validation():
    assert search_locations("da-nang")[0].provider_location_id == "352954"
    # Phú Quốc is served through its province entry, not its own id.
    assert [item.id for item in search_locations("Phú Quốc")] == ["an-giang"]
    with pytest.raises(ValueError):
        WeatherLocation(id="x", name="x", province="x", latitude=91, longitude=0)
    with pytest.raises(ValueError):
        SourceMetadata(
            source="x",
            provider="x",
            retrieved_at=datetime.now(),
            timezone="UTC",
            location_id="x",
        )


def test_catalog_has_all_current_provincial_units_and_alias_search():
    assert len(LOCATIONS) == 34
    assert len(BY_ID) == 34
    assert len({item.id for item in LOCATIONS}) == 34
    assert search_locations("da nang")[0].id == "da-nang"
    assert search_locations("binh duong")[0].id == "ho-chi-minh"
    assert search_locations("phu quoc")[0].id == "an-giang"


def test_provider_requires_license_key():
    with pytest.raises(ProviderUnavailableError):
        AccuWeatherProvider("")


def test_open_meteo_maps_keyless_current_weather():
    def response(*_args, **_kwargs):
        return {
            "current": {
                "time": "2026-09-21T11:00",
                "temperature_2m": 29.4,
                "relative_humidity_2m": 78,
                "apparent_temperature": 34.1,
                "weather_code": 95,
                "surface_pressure": 1004.6,
                "wind_speed_10m": 18.2,
                "wind_direction_10m": 45,
                "wind_gusts_10m": 31.0,
                "precipitation": 1.2,
                "rain": 1.2,
                "cloud_cover": 91,
            }
        }

    weather = OpenMeteoProvider(transport=response).current(BY_ID["da-nang"])

    assert weather.temperature_c == 29.4
    assert weather.condition.icon == "thunderstorm"
    assert weather.wind.speed_kmh == 18.2
    assert weather.metadata.provider == "open-meteo"
    assert weather.observation_time.utcoffset() is not None


def test_provider_maps_quota_not_found_and_timeout():
    location = BY_ID["da-nang"]
    for error, expected in [
        (HTTPError("u", 429, "quota", {}, None), ProviderQuotaError),
        (HTTPError("u", 404, "missing", {}, None), LocationNotFoundError),
        (TimeoutError(), ProviderUnavailableError),
    ]:

        def fail(*_args, error=error, **_kwargs):
            raise error

        with pytest.raises(expected):
            AccuWeatherProvider("key", transport=fail).current(location)


def test_nchmf_parser_preserves_source_without_inventing_regions():
    phrase = "m" + chr(432) + "a l" + chr(7899) + "n"
    alert = NchmfBulletinParser().parse(
        "<h1>Tin " + phrase + "</h1><p>Official source text.</p>",
        source_url="https://nchmf.gov.vn/kttv/test",
        published_at=datetime(2026, 9, 20, tzinfo=UTC),
    )
    assert alert.type == "heavy_rain"
    assert alert.affected_areas == []
    assert "Official source text" in alert.description
    assert alert.metadata.provider == "nchmf"


def test_weather_api_fails_closed_without_key():
    class Engine:
        def dispose(self):
            pass

    class Store:
        engine = Engine()

    app = create_app(
        Settings(
            cache_enabled=False,
            operational_database_url="sqlite:///:memory:",
            weather_provider="accuweather",
        ),
        store=Store(),
        forecaster=object(),
    )
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/api/weather/current?location_id=da-nang")
    assert response.status_code == 503
    assert "provider" in response.json()["error"]["message"].lower()
