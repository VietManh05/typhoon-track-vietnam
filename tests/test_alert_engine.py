from datetime import datetime, timedelta, timezone

from typhoon_vn.alerts.channels import FakeTransport
from typhoon_vn.alerts.engine import InMemoryDeliveryState, Severity, deliver, evaluate


def fixture(distance=60, horizon=24):
    return (
        {"label": "Da Nang", "radius_km": 200, "lead_hours": 72, "cooldown_hours": 12},
        {
            "forecast_id": "f1",
            "storm_id": "s1",
            "issue_time": "2026-09-20T00:00:00+00:00",
            "sources": ["fixture-v1"],
            "disclaimer": "Experimental; consult official warnings.",
            "points": [{"horizon_hours": horizon, "distance_km": distance}],
        },
    )


def test_rule_boundaries_and_message_provenance():
    sub, fc = fixture()
    draft = evaluate("sub", sub, fc)
    assert draft.severity == Severity.EMERGENCY and "fixture-v1" in draft.message
    fc["points"][0]["distance_km"] = 200
    assert evaluate("sub", sub, fc).severity == Severity.WATCH
    fc["points"][0]["distance_km"] = 200.1
    assert evaluate("sub", sub, fc) is None
    fc["points"][0] = {"horizon_hours": 73, "distance_km": 1}
    assert evaluate("sub", sub, fc) is None


def test_delivery_retry_dedupe_cooldown_and_dead_letter():
    sub, fc = fixture(100)
    draft = evaluate("sub", sub, fc)
    state = InMemoryDeliveryState()
    transport = FakeTransport(fail_first=1)
    now = datetime(2026, 9, 20, tzinfo=timezone.utc)
    result = deliver(draft, transport, state, now=now, sleep=lambda _: None)
    assert (result.status, result.attempts, len(transport.sent)) == ("delivered", 2, 1)
    assert deliver(draft, transport, state, now=now).status == "duplicate"
    fc["forecast_id"] = "f2"
    second = evaluate("sub", sub, fc)
    assert (
        deliver(second, transport, state, now=now + timedelta(hours=11)).status
        == "throttled"
    )
    failed = deliver(
        second,
        FakeTransport(fail_first=99),
        InMemoryDeliveryState(),
        max_attempts=2,
        sleep=lambda _: None,
    )
    assert failed.status == "dead_letter" and failed.attempts == 2
