"""Typed failures raised by the data-ingestion boundary."""


class IngestionError(RuntimeError):
    """Base error for a recoverable ingestion failure."""


class DownloadError(IngestionError):
    """Raised when an upstream object cannot be downloaded and verified."""


class DownloadTimeoutError(DownloadError):
    """Raised when an upstream source exceeds the bounded download timeout."""


class ProviderError(IngestionError):
    """Base error for failures isolated to one external provider."""


class ProviderSchemaError(ProviderError):
    """Raised when a source payload no longer matches its parser contract."""


class UnsupportedProviderError(ProviderError):
    """Raised when no registered strategy exists for a requested source."""


class OptionalDependencyError(IngestionError):
    """Raised when a feature needs an optional ingestion dependency."""
