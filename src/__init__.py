"""Core DSPy Ozempic classifier package."""

from .common import (
    CLASSIFICATION_CONFIGS,
    ComplaintClassifier,
    classification_metric,
    configure_lm,
    create_classification_signature,
    evaluate_model,
    prepare_datasets,
)
from .serving.service import (
    ComplaintRequest,
    ComplaintResponse,
    get_classification_function,
)

__all__ = [
    "CLASSIFICATION_CONFIGS",
    "create_classification_signature",
    "ComplaintClassifier",
    "classification_metric",
    "configure_lm",
    "evaluate_model",
    "prepare_datasets",
    "ComplaintRequest",
    "ComplaintResponse",
    "get_classification_function",
]
