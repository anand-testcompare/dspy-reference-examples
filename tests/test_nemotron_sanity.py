"""Quick sanity test for nemotron model invocation via local llama.cpp server."""

from __future__ import annotations

import socket
from urllib.parse import urlparse

import dspy
import pytest
import requests

from src.common.config import configure_lm, load_llm_config


def _skip_if_unreachable(api_base: str | None) -> None:
    if not api_base:
        pytest.skip("No API base configured for local LLM.")
    parsed = urlparse(api_base)
    host = parsed.hostname or "localhost"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1.0)
        try:
            sock.connect((host, port))
        except OSError:
            pytest.skip(f"Local LLM server not reachable at {host}:{port}.")


@pytest.fixture(scope="session")
def cfg():
    try:
        cfg = load_llm_config()
    except RuntimeError as exc:
        pytest.skip(str(exc))
    return cfg


@pytest.fixture(scope="session")
def local_cfg(cfg):
    if not cfg.is_local:
        pytest.skip("Expected local provider. Set DSPY_PROVIDER=local in .env.")
    _skip_if_unreachable(cfg.api_base)
    return cfg


def test_config_loads(cfg):
    """Verify config loads correctly for local provider."""
    print(f"\n[Config] Provider: {'local' if cfg.is_local else 'openrouter'}")
    print(f"[Config] Model: {cfg.model}")
    print(f"[Config] API Base: {cfg.api_base}")
    if not cfg.is_local:
        pytest.skip("Expected local provider. Set DSPY_PROVIDER=local in .env.")
    assert "nemotron" in cfg.model.lower(), f"Expected Nemotron model, got: {cfg.model}"


def test_raw_api_call(local_cfg):
    """Test raw HTTP call to llama.cpp /v1/chat/completions endpoint."""
    url = f"{local_cfg.api_base}/chat/completions"
    payload = {
        "model": local_cfg.model,
        "messages": [{"role": "user", "content": "What is 2 + 2? Answer with just the number."}],
        "max_tokens": 50,
        "temperature": 0.0,
    }
    print(f"\n[Raw API] POST {url}")
    print(f"[Raw API] Payload: {payload}")

    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        pytest.skip(f"Local LLM request failed: {exc}")

    print(f"[Raw API] Status: {resp.status_code}")
    print(f"[Raw API] Response: {data}")

    content = data["choices"][0]["message"]["content"]
    print(f"[Raw API] Content: {content}")
    assert content, "Expected non-empty content"
    return data


def test_nemotron_basic_completion(local_cfg):
    """Sanity test: invoke nemotron with a simple prompt."""
    lm = configure_lm()
    print(f"\n[LM] Configured: {lm}")

    # Simple completion test
    response = lm("What is 2 + 2? Answer with just the number.")
    print(f"[Response] {response}")

    assert response, "Expected non-empty response from model"
    assert "4" in str(response), f"Expected '4' in response, got: {response}"


def test_nemotron_dspy_predict(local_cfg):
    """Sanity test: use DSPy Predict module."""
    lm = configure_lm()

    class SimpleQA(dspy.Signature):
        """Answer the question concisely."""

        question: str = dspy.InputField()
        answer: str = dspy.OutputField()

    predictor = dspy.Predict(SimpleQA)

    # Debug: show raw LM history after prediction
    try:
        result = predictor(question="What is the capital of France?")
        print(f"\n[Predict] Answer: {result.answer}")
        assert result.answer, "Expected non-empty answer"
        assert "paris" in result.answer.lower(), f"Expected 'Paris' in answer, got: {result.answer}"
    except Exception as e:
        print(f"\n[Predict] Error: {e}")
        print("\n[Debug] Last LM call history:")
        if lm.history:
            last_call = lm.history[-1]
            print(f"  Prompt: {last_call.get('prompt', last_call.get('messages', 'N/A'))[:500]}...")
            print(f"  Response: {last_call.get('response', 'N/A')}")
        raise


if __name__ == "__main__":
    print("=" * 60)
    print("Nemotron Sanity Test")
    print("=" * 60)

    print("\n1. Testing config...")
    cfg = test_config_loads()
    print("   ✓ Config OK")

    print("\n2. Testing raw API call to llama.cpp...")
    test_raw_api_call(cfg)
    print("   ✓ Raw API OK")

    print("\n3. Testing DSPy basic completion...")
    test_nemotron_basic_completion()
    print("   ✓ Basic completion OK")

    print("\n4. Testing DSPy Predict...")
    test_nemotron_dspy_predict()
    print("   ✓ DSPy Predict OK")

    print("\n" + "=" * 60)
    print("All sanity tests passed! Model is ready for full runs.")
    print("=" * 60)
