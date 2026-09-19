"""Point-in-time contracts for optional environmental forecasts."""

from datetime import datetime, timezone

import pytest

from typhoon_vn.ingestion.providers.environment import ForecastField, select_forecast_field


UTC = timezone.utc


def test_point_in_time_selection_never_uses_future_issuance() -> None:
    fields = [
        ForecastField("gfs", datetime(2025, 1, 1, 0, tzinfo=UTC), 12, "0p25", "old"),
        ForecastField("gfs", datetime(2025, 1, 1, 6, tzinfo=UTC), 6, "0p25", "future"),
    ]
    selected = select_forecast_field(
        fields,
        issue_time=datetime(2025, 1, 1, 3, tzinfo=UTC),
        valid_time=datetime(2025, 1, 1, 12, tzinfo=UTC),
    )
    assert selected.cache_key.endswith("old")


def test_environment_forecast_has_explicit_missing_fallback() -> None:
    selected = select_forecast_field(
        [],
        issue_time=datetime(2025, 1, 1, tzinfo=UTC),
        valid_time=datetime(2025, 1, 2, tzinfo=UTC),
        allow_missing=True,
    )
    assert selected is None
    with pytest.raises(LookupError, match="available"):
        select_forecast_field(
            [],
            issue_time=datetime(2025, 1, 1, tzinfo=UTC),
            valid_time=datetime(2025, 1, 2, tzinfo=UTC),
        )
