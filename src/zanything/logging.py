"""Structured JSON logging and request context."""

import json
import logging
import sys
import time
from contextvars import ContextVar
from typing import Any

# Context variables for correlation tracking across async tasks
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")
tenant_id_ctx: ContextVar[str] = ContextVar("tenant_id", default="-")


class JSONLogFormatter(logging.Formatter):
    """Formatter producing structured JSON log records with standard fields."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: dict[str, Any] = {
            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime(record.created)
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_ctx.get(),
            "tenant_id": tenant_id_ctx.get(),
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Merge custom attributes attached to log record if any
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_data.update(record.extra)

        return json.dumps(log_data)


def configure_logging(level: str = "INFO", json_format: bool = True) -> None:
    """Configure root logger with structured formatting."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level.upper())

    # Remove existing handlers to avoid duplicates
    for handler in list(root_logger.handlers):
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler(sys.stdout)
    if json_format:
        handler.setFormatter(JSONLogFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "[%(asctime)s] %(levelname)s [%(name)s] [%(request_id)s] %(message)s"
            )
        )

    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a logger instance with the specified name."""
    return logging.getLogger(name)
