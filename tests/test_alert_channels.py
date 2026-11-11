import pytest

from typhoon_vn.alerts.channels import (
    PROVIDERS,
    DisabledProviderTransport,
    FakeTransport,
)


def test_provider_registry_and_real_delivery_disabled():
    assert set(PROVIDERS) == {"email", "sms", "telegram", "zalo"}
    with pytest.raises(RuntimeError, match="disabled"):
        DisabledProviderTransport("telegram").send(None, "delivery")
    assert FakeTransport().sent == []
