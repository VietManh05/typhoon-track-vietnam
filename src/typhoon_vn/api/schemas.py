"""Validated public contract. All times are UTC and positions are WGS84."""
from datetime import datetime, timedelta, timezone
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

DISCLAIMER = (
    "Decision support only; not an official weather warning. "
    "Follow official NCHMF guidance. / Chi tham khao; khong thay the ban tin NCHMF."
)

class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

class Fix(Contract):
    timestamp: datetime
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    wind_ms: float | None = Field(default=None, ge=0, le=150)
    pressure_hpa: float | None = Field(default=None, ge=850, le=1050)
    intensity: Literal["TD", "TS", "STS", "TY", "STY", "SUPERTY", "UNK"] = "UNK"
    source: str = Field(min_length=1, max_length=200)
    source_url: str | None = Field(default=None, max_length=2048)

    @field_validator("timestamp")
    @classmethod
    def utc(cls, value):
        if value.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        return value.astimezone(timezone.utc)

class ForecastRequest(Contract):
    storm_id: str = Field(min_length=1, max_length=80, pattern=r"^[\w.-]+$")
    observations: list[Fix] | None = Field(default=None, min_length=2, max_length=512)
    horizons: list[int] = Field(default_factory=lambda: [6, 12, 24, 48, 72])

    @model_validator(mode="after")
    def ordered(self):
        if not self.horizons or self.horizons != sorted(set(self.horizons)):
            raise ValueError("horizons must be unique and increasing")
        if any(h not in (6, 12, 24, 48, 72) for h in self.horizons):
            raise ValueError("supported horizons: 6, 12, 24, 48, 72 hours")
        if self.observations:
            times = [fix.timestamp for fix in self.observations]
            if any(a >= b for a, b in zip(times, times[1:])):
                raise ValueError("observations must be strictly chronological")
        return self

class ForecastPoint(Contract):
    horizon_hours: int
    valid_time: datetime

    @field_validator("valid_time")
    @classmethod
    def valid_time_utc(cls, value):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("valid_time must include a timezone")
        return value.astimezone(timezone.utc)
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    intensity: str
    radius_km: float = Field(ge=0)
    cone: dict

class ForecastResponse(Contract):
    forecast_id: str
    storm_id: str
    issue_time: datetime
    generated_at: datetime
    model_version: str
    model_kind: str
    dataset_version: str
    sources: list[str]
    uncertainty_method: str
    warnings: list[str]
    disclaimer: str = DISCLAIMER
    points: list[ForecastPoint]

    @field_validator("issue_time", "generated_at")
    @classmethod
    def response_time_utc(cls, value):
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("response times must include a timezone")
        return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def valid_times_match_horizons(self):
        for point in self.points:
            expected = self.issue_time + timedelta(hours=point.horizon_hours)
            if point.valid_time != expected:
                raise ValueError("valid_time must equal issue_time + horizon_hours")
        return self

class ObservationBatch(Contract):
    storm_id: str = Field(min_length=1, max_length=80, pattern=r"^[\w.-]+$")
    name: str = Field(min_length=1, max_length=120)
    observations: list[Fix] = Field(min_length=1, max_length=512)

class Subscription(Contract):
    label: str = Field(min_length=1, max_length=100)
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    radius_km: float = Field(default=200, gt=0, le=2000)
    lead_hours: int = Field(default=72, ge=6, le=72)
    cooldown_hours: int = Field(default=12, ge=1, le=168)
