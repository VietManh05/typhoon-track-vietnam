"""Source-specific download and parser adapters."""

from typhoon_vn.ingestion.providers.cma import CMAProvider
from typhoon_vn.ingestion.providers.strategies import (
    DEFAULT_PROVIDER_FACTORY,
    ProviderFactory,
    ProviderStrategy,
)

__all__ = [
    "CMAProvider",
    "DEFAULT_PROVIDER_FACTORY",
    "ProviderFactory",
    "ProviderStrategy",
]
