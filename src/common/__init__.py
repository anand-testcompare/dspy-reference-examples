"""Shared DSPy classifier components."""

from .classifier import ComplaintClassification, ComplaintClassifier, classification_metric, evaluate_model
from .config import LLMConfig, configure_lm, load_llm_config
from .data_utils import prepare_datasets
from .paths import (
    ARTIFACTS_DIR,
    DATA_DIR,
    DEFAULT_CLASSIFIER_PATH,
    ROOT_DIR,
    TEST_DATA_PATH,
    TRAIN_DATA_PATH,
)

__all__ = [
    "ComplaintClassification",
    "ComplaintClassifier",
    "classification_metric",
    "evaluate_model",
    "configure_lm",
    "LLMConfig",
    "load_llm_config",
    "prepare_datasets",
    "ROOT_DIR",
    "DATA_DIR",
    "ARTIFACTS_DIR",
    "TRAIN_DATA_PATH",
    "TEST_DATA_PATH",
    "DEFAULT_CLASSIFIER_PATH",
]
