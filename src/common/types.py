"""Shared typing helpers."""

from __future__ import annotations

from typing import Literal

ClassificationType = Literal["ae-pc", "ae-category", "pc-category"]
CLASSIFICATION_TYPE_VALUES: tuple[ClassificationType, ...] = ("ae-pc", "ae-category", "pc-category")

__all__ = ["ClassificationType", "CLASSIFICATION_TYPE_VALUES"]
