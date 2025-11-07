"""Configuration helpers for DSPy LM setup."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional

import dspy
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b"
DEFAULT_OPENROUTER_BASE = "https://openrouter.ai/api/v1"


@dataclass
class LLMConfig:
    """Runtime configuration for the underlying language model."""

    model: str = DEFAULT_MODEL
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    headers: Dict[str, str] = field(default_factory=dict)

    @property
    def is_openrouter(self) -> bool:
        base = (self.api_base or "").lower()
        return "openrouter" in base


def _load_extra_headers() -> Dict[str, str]:
    """Build extra headers from env (JSON or individual fields)."""

    headers: Dict[str, str] = {}

    raw = os.getenv("DSPY_HTTP_HEADERS")
    if raw:
        try:
            headers.update(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON in DSPY_HTTP_HEADERS environment variable"
            ) from exc

    referer = os.getenv("OPENROUTER_HTTP_REFERER")
    if referer:
        headers.setdefault("HTTP-Referer", referer)

    app_name = os.getenv("OPENROUTER_APP_TITLE")
    if app_name:
        headers.setdefault("X-Title", app_name)

    return headers


def load_llm_config() -> LLMConfig:
    """Load LM configuration from environment variables."""

    cfg = LLMConfig()

    cfg.model = os.getenv("DSPY_MODEL_NAME", DEFAULT_MODEL)

    cfg.api_key = (
        os.getenv("DSPY_API_KEY")
        or os.getenv("OPENROUTER_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )

    if not cfg.api_key:
        raise RuntimeError(
            "No API key found. Set OPENROUTER_API_KEY, OPENAI_API_KEY, or DSPY_API_KEY."
        )

    cfg.api_base = (
        os.getenv("DSPY_API_BASE")
        or os.getenv("OPENROUTER_API_BASE")
        or (DEFAULT_OPENROUTER_BASE if os.getenv("OPENROUTER_API_KEY") else None)
    )

    cfg.headers = _load_extra_headers()

    return cfg


def configure_lm() -> dspy.LM:
    """Configure DSPy with the loaded LM settings and return the LM instance."""

    cfg = load_llm_config()
    lm = dspy.LM(
        cfg.model,
        api_key=cfg.api_key,
        api_base=cfg.api_base,
        headers=cfg.headers or None,
    )
    dspy.configure(lm=lm)
    return lm


__all__ = ["LLMConfig", "configure_lm", "load_llm_config", "DEFAULT_MODEL"]
