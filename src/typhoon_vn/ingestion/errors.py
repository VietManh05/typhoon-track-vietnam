"""Domain-specific failures raised by the data-ingestion boundary."""


class IngestionError(RuntimeError):
    """Base error for a recoverable ingestion failure."""


class DownloadError(IngestionError):
    """Raised when an upstream object cannot be downloaded and verified."""


class OptionalDependencyError(IngestionError):
    """Raised when a feature needs an optional ingestion dependency."""
