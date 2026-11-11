"""Central logging configuration for API, ingestion, and workers."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any

_STANDARD = set(logging.makeLogRecord({}).__dict__) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    """Emit one machine-readable JSON object per log record."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(
            {
                key: value
                for key, value in record.__dict__.items()
                if key not in _STANDARD and not key.startswith("_")
            }
        )
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def configure_logging(level: str = "INFO", *, json_logs: bool = True) -> None:
    """Configure process-wide logging once, while allowing level updates."""

    root = logging.getLogger()
    root.setLevel(level.upper())
    managed = next(
        (
            handler
            for handler in root.handlers
            if getattr(handler, "_typhoon_vn", False)
        ),
        None,
    )
    if managed is None:
        managed = logging.StreamHandler()
        managed._typhoon_vn = True  # type: ignore[attr-defined]
        root.addHandler(managed)
    formatter: logging.Formatter
    formatter = (
        JsonFormatter()
        if json_logs
        else logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    managed.setFormatter(formatter)
