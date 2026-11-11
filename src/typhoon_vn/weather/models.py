"""Provider-neutral weather contracts for TYPHOON VN."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WeatherModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=lambda s: s.split("_")[0]
        + "".join(p.title() for p in s.split("_")[1:]),
        populate_by_name=True,
        extra="forbid",
    )


class WeatherLocation(WeatherModel):
    id: str
    name: str
    province: str
    country: str = "VN"
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = "Asia/Ho_Chi_Minh"
    provider_location_id: str | None = None
    aliases: list[str] = Field(default_factory=list)


class SourceMetadata(WeatherModel):
    source: str
    provider: str
    retrieved_at: datetime
    timezone: str
    location_id: str
    source_url: str | None = None
    is_stale: bool = False

    @field_validator("retrieved_at")
    @classmethod
    def aware(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("retrieved_at must be timezone-aware")
        return value


class WeatherCondition(WeatherModel):
    code: str
    label: str
    icon: str


class Wind(WeatherModel):
    speed_kmh: float = Field(ge=0)
    gust_kmh: float | None = Field(default=None, ge=0)
    direction_deg: float | None = Field(default=None, ge=0, le=360)
    direction_label: str | None = None


class Precipitation(WeatherModel):
    probability_percent: float | None = Field(default=None, ge=0, le=100)
    rain_mm: float | None = Field(default=None, ge=0)


class CurrentWeather(WeatherModel):
    location: WeatherLocation
    observation_time: datetime
    temperature_c: float
    feels_like_c: float | None = None
    condition: WeatherCondition
    humidity_percent: float | None = Field(default=None, ge=0, le=100)
    wind: Wind
    pressure_hpa: float | None = Field(default=None, gt=0)
    visibility_km: float | None = Field(default=None, ge=0)
    dew_point_c: float | None = None
    cloud_cover_percent: float | None = Field(default=None, ge=0, le=100)
    uv_index: float | None = Field(default=None, ge=0)
    precipitation: Precipitation = Field(default_factory=Precipitation)
    air_quality_index: float | None = Field(default=None, ge=0)
    metadata: SourceMetadata


class HourlyForecast(WeatherModel):
    forecast_time: datetime
    temperature_c: float
    feels_like_c: float | None = None
    condition: WeatherCondition
    precipitation: Precipitation = Field(default_factory=Precipitation)
    humidity_percent: float | None = Field(default=None, ge=0, le=100)
    wind: Wind
    pressure_hpa: float | None = Field(default=None, gt=0)
    uv_index: float | None = Field(default=None, ge=0)
    metadata: SourceMetadata


class DailyForecast(WeatherModel):
    forecast_date: date
    min_temperature_c: float
    max_temperature_c: float
    condition: WeatherCondition
    precipitation: Precipitation = Field(default_factory=Precipitation)
    wind: Wind
    sunrise: datetime | None = None
    sunset: datetime | None = None
    metadata: SourceMetadata


class WeatherAlert(WeatherModel):
    id: str
    type: str
    severity: str
    title: str
    description: str
    affected_areas: list[str] = Field(default_factory=list)
    issued_at: datetime
    valid_from: datetime | None = None
    valid_until: datetime | None = None
    metadata: SourceMetadata


class WeatherBundle(WeatherModel):
    location: WeatherLocation
    current: CurrentWeather | None = None
    hourly: list[HourlyForecast] = Field(default_factory=list)
    daily: list[DailyForecast] = Field(default_factory=list)
    alerts: list[WeatherAlert] = Field(default_factory=list)
