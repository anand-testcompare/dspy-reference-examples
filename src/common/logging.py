"""Logging configuration helpers."""

from __future__ import annotations

import json
import logging
import os
import uuid
from contextvars import ContextVar, Token
from datetime import datetime, timezone

_REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="-")
_RUN_ID = os.getenv("DSPY_RUN_ID") or os.getenv("RUN_ID") or uuid.uuid4().hex
_CONFIGURED = False


def set_request_id(request_id: str) -> Token:
    return _REQUEST_ID.set(request_id)


def reset_request_id(token: Token) -> None:
    _REQUEST_ID.reset(token)


def _get_request_id() -> str:
    return _REQUEST_ID.get()


class _ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _get_request_id()
        record.run_id = _RUN_ID
        return True


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
            "run_id": getattr(record, "run_id", _RUN_ID),
            "request_id": getattr(record, "request_id", _get_request_id()),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def configure_logging(default_level: str = "INFO") -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    level_name = os.getenv("DSPY_LOG_LEVEL") or os.getenv("LOG_LEVEL") or default_level
    level = getattr(logging, level_name.upper(), logging.INFO)
    format_style = (os.getenv("DSPY_LOG_FORMAT") or "json").lower()

    handler = logging.StreamHandler()
    handler.addFilter(_ContextFilter())

    if format_style == "text":
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s run_id=%(run_id)s request_id=%(request_id)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
        )
    else:
        formatter = _JsonFormatter()
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True

    _CONFIGURED = True


__all__ = ["configure_logging", "reset_request_id", "set_request_id"]
