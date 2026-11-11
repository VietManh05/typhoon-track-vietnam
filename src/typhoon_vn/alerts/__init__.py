"""Safe, draft-first alert evaluation and delivery adapters."""

from .engine import (
    AlertDraft,
    AlertRule,
    DeliveryResult,
    InMemoryDeliveryState,
    Severity,
    deliver,
    evaluate,
)

__all__ = [
    "AlertDraft",
    "AlertRule",
    "DeliveryResult",
    "InMemoryDeliveryState",
    "Severity",
    "deliver",
    "evaluate",
]
