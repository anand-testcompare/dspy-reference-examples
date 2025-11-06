"""
Quick setup verification script.
Checks that all dependencies and configuration are ready.
"""

import sys
import os


def check_python_version():
    """Check Python version is 3.8+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    required = ["dspy", "openai", "dotenv"]
    missing = []

    for package in required:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)

    if missing:
        print(f"\nInstall missing packages with:")
        print(f"  pip install -r requirements.txt")
        return False

    return True


def check_api_key():
    """Check if OpenAI API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set")
        print("\nSet your API key:")
        print("  export OPENAI_API_KEY='your-key-here'")
        print("or create a .env file with:")
        print("  OPENAI_API_KEY=your-key-here")
        return False

    # Mask the key for security
    masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
    print(f"✓ OPENAI_API_KEY configured ({masked_key})")
    return True


def check_data_files():
    """Check if data generator is available"""
    try:
        from data_generator import generate_training_data, generate_test_data
        train_data = generate_training_data()
        test_data = generate_test_data()
        print(f"✓ Training data: {len(train_data)} examples")
        print(f"✓ Test data: {len(test_data)} examples")
        return True
    except Exception as e:
        print(f"❌ Data generator error: {e}")
        return False


def main():
    print("\n" + "="*50)
    print("DSPy Ozempic Classifier - Setup Check")
    print("="*50 + "\n")

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("API Key", check_api_key),
        ("Data Files", check_data_files),
    ]

    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())

    print("\n" + "="*50)
    if all(results):
        print("✓ All checks passed! Ready to run:")
        print("  python ozempic_classifier.py")
    else:
        print("❌ Some checks failed. Fix issues above.")
    print("="*50 + "\n")

    return all(results)


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
