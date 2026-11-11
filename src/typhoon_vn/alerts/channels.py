"""Alert adapters; only the fake transport is enabled."""

from dataclasses import dataclass, field

from .engine import AlertDraft


@dataclass(slots=True)
class FakeTransport:
    fail_first: int = 0
    attempts: int = 0
    sent: list[tuple[str, AlertDraft]] = field(default_factory=list)

    def send(self, draft: AlertDraft, delivery_id: str) -> None:
        self.attempts += 1
        if self.attempts <= self.fail_first:
            raise RuntimeError("simulated transport failure")
        self.sent.append((delivery_id, draft))


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    provider: str
    credential_env: str


PROVIDERS = {
    name: ProviderConfig(name, env)
    for name, env in {
        "email": "ALERT_EMAIL_CREDENTIAL",
        "sms": "ALERT_SMS_CREDENTIAL",
        "telegram": "ALERT_TELEGRAM_TOKEN",
        "zalo": "ALERT_ZALO_TOKEN",
    }.items()
}


class DisabledProviderTransport:
    def __init__(self, provider: str):
        if provider not in PROVIDERS:
            raise ValueError("unsupported provider")
        self.provider = provider

    def send(self, draft: AlertDraft, delivery_id: str) -> None:
        raise RuntimeError(
            f"{self.provider} delivery is disabled until operator configuration and recipient approval"
        )
