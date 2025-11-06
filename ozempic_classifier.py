"""
DSPy-based classifier for Ozempic complaints.
Distinguishes between Adverse Events and Product Complaints.
"""

import os
import dspy
from dotenv import load_dotenv
from data_generator import generate_training_data, generate_test_data

# Load environment variables
load_dotenv()


class ComplaintClassification(dspy.Signature):
    """Classify Ozempic-related complaints as either Adverse Events or Product Complaints.

    Adverse Events involve patient safety, medical reactions, or health outcomes.
    Product Complaints involve device defects, packaging issues, or quality problems without patient harm.
    """

    complaint = dspy.InputField(desc="The complaint text about Ozempic")
    classification = dspy.OutputField(desc="Either 'Adverse Event' or 'Product Complaint'")
    justification = dspy.OutputField(desc="Brief explanation for the classification")


class ComplaintClassifier(dspy.Module):
    """DSPy Module for classifying Ozempic complaints."""

    def __init__(self):
        super().__init__()
        self.classify = dspy.ChainOfThought(ComplaintClassification)

    def forward(self, complaint):
        result = self.classify(complaint=complaint)
        return dspy.Prediction(
            classification=result.classification,
            justification=result.justification
        )


def prepare_datasets():
    """Convert raw data to DSPy Example format."""

    train_raw = generate_training_data()
    test_raw = generate_test_data()

    # Convert to DSPy Examples
    trainset = [
        dspy.Example(
            complaint=item["complaint"],
            classification=item["label"]
        ).with_inputs("complaint")
        for item in train_raw
    ]

    testset = [
        dspy.Example(
            complaint=item["complaint"],
            classification=item["label"]
        ).with_inputs("complaint")
        for item in test_raw
    ]

    return trainset, testset


def classification_metric(example, pred, trace=None):
    """
    Evaluation metric: Returns 1.0 if classification matches, 0.0 otherwise.
    """
    # Normalize both strings for comparison (handle case and whitespace)
    predicted = pred.classification.strip().lower()
    actual = example.classification.strip().lower()

    return float(predicted == actual)


def evaluate_model(model, dataset, dataset_name="Dataset"):
    """Evaluate model on a dataset and return accuracy."""
    correct = 0
    total = len(dataset)

    print(f"\n{'='*60}")
    print(f"Evaluating on {dataset_name} ({total} examples)")
    print(f"{'='*60}\n")

    for i, example in enumerate(dataset, 1):
        pred = model(complaint=example.complaint)
        is_correct = classification_metric(example, pred)
        correct += is_correct

        status = "✓" if is_correct else "✗"
        print(f"{status} Example {i}/{total}")
        print(f"  Complaint: {example.complaint[:80]}...")
        print(f"  Predicted: {pred.classification}")
        print(f"  Actual: {example.classification}")
        if not is_correct:
            print(f"  Justification: {pred.justification}")
        print()

    accuracy = correct / total
    print(f"{'='*60}")
    print(f"Accuracy: {correct}/{total} = {accuracy:.1%}")
    print(f"{'='*60}\n")

    return accuracy


def main():
    """Main execution function."""

    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please set your API key:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("or create a .env file with:")
        print("  OPENAI_API_KEY=your-api-key-here")
        return

    print("\n" + "="*60)
    print("DSPy Ozempic Complaint Classifier")
    print("Adverse Events vs Product Complaints")
    print("="*60 + "\n")

    # Configure DSPy with OpenAI
    lm = dspy.LM('openai/gpt-4o-mini', api_key=api_key)
    dspy.configure(lm=lm)

    # Prepare datasets
    print("Loading training and test data...")
    trainset, testset = prepare_datasets()
    print(f"✓ Loaded {len(trainset)} training examples")
    print(f"✓ Loaded {len(testset)} test examples\n")

    # Create unoptimized classifier
    print("Creating baseline (unoptimized) classifier...")
    baseline_classifier = ComplaintClassifier()

    # Evaluate baseline
    print("\n" + "🔵 BASELINE PERFORMANCE (No Optimization)")
    baseline_accuracy = evaluate_model(baseline_classifier, testset, "Test Set")

    # Optimize with DSPy
    print("\n" + "🔄 OPTIMIZING WITH DSPy...")
    print("Using BootstrapFewShotWithRandomSearch optimizer")
    print("This will take a few minutes...\n")

    from dspy.teleprompt import BootstrapFewShotWithRandomSearch

    optimizer = BootstrapFewShotWithRandomSearch(
        metric=classification_metric,
        max_bootstrapped_demos=3,  # Number of examples to use in few-shot
        num_candidate_programs=8,   # Number of candidate programs to try
    )

    optimized_classifier = optimizer.compile(
        ComplaintClassifier(),
        trainset=trainset
    )

    print("✓ Optimization complete!\n")

    # Evaluate optimized model
    print("\n" + "🟢 OPTIMIZED PERFORMANCE")
    optimized_accuracy = evaluate_model(optimized_classifier, testset, "Test Set")

    # Summary
    print("\n" + "="*60)
    print("FINAL RESULTS SUMMARY")
    print("="*60)
    print(f"Baseline Accuracy:   {baseline_accuracy:.1%}")
    print(f"Optimized Accuracy:  {optimized_accuracy:.1%}")
    print(f"Improvement:         {optimized_accuracy - baseline_accuracy:+.1%}")
    print("="*60 + "\n")

    # Save the optimized model
    print("Saving optimized model...")
    optimized_classifier.save("ozempic_classifier_optimized.json")
    print("✓ Saved to: ozempic_classifier_optimized.json\n")


if __name__ == "__main__":
    main()
