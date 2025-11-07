"""Entrypoint for training and optimizing the Ozempic DSPy classifier."""

from __future__ import annotations

from dspy.teleprompt import BootstrapFewShotWithRandomSearch

from ..common.classifier import (
    ComplaintClassifier,
    classification_metric,
    evaluate_model,
)
from ..common.config import configure_lm
from ..common.data_utils import prepare_datasets
from ..common.paths import ARTIFACTS_DIR, DEFAULT_CLASSIFIER_PATH


def run_pipeline() -> None:
    """Train, optimize, and evaluate the classifier, then persist the artifact."""

    print("\n" + "=" * 60)
    print("DSPy Ozempic Complaint Classifier")
    print("Adverse Events vs Product Complaints")
    print("=" * 60 + "\n")

    configure_lm()

    print("Loading training and test data...")
    trainset, testset = prepare_datasets()
    print(f"✓ Loaded {len(trainset)} training examples")
    print(f"✓ Loaded {len(testset)} test examples\n")

    baseline_classifier = ComplaintClassifier()

    print("\n" + "🔵 BASELINE PERFORMANCE (No Optimization)")
    baseline_accuracy = evaluate_model(baseline_classifier, testset, "Test Set")

    print("\n" + "🔄 OPTIMIZING WITH DSPy...")
    print("Using BootstrapFewShotWithRandomSearch optimizer")
    print("This may take a few minutes...\n")

    optimizer = BootstrapFewShotWithRandomSearch(
        metric=classification_metric,
        max_bootstrapped_demos=3,
        num_candidate_programs=8,
    )

    optimized_classifier = optimizer.compile(
        ComplaintClassifier(),
        trainset=trainset,
    )

    print("✓ Optimization complete!\n")

    print("\n" + "🟢 OPTIMIZED PERFORMANCE")
    optimized_accuracy = evaluate_model(optimized_classifier, testset, "Test Set")

    print("\n" + "=" * 60)
    print("FINAL RESULTS SUMMARY")
    print("=" * 60)
    print(f"Baseline Accuracy:   {baseline_accuracy:.1%}")
    print(f"Optimized Accuracy:  {optimized_accuracy:.1%}")
    print(f"Improvement:         {optimized_accuracy - baseline_accuracy:+.1%}")
    print("=" * 60 + "\n")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    print("Saving optimized model...")
    optimized_classifier.save(str(DEFAULT_CLASSIFIER_PATH))
    print(f"✓ Saved to: {DEFAULT_CLASSIFIER_PATH}\n")


def main() -> None:
    run_pipeline()


if __name__ == "__main__":
    main()
