"""Validation tests for Foundry OpenAPI deployment artifacts."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "deploy" / "foundry_openapi.py"
CANONICAL_SPEC = REPO_ROOT / "openapi.foundry.json"
EXPECTED_PATHS = {
    "/classify/ae-pc",
    "/classify/ae-category",
    "/classify/pc-category",
}
EXPECTED_SERVER_URL = "http://localhost:5000"


def _run_script(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _contains_combiners(node: object) -> bool:
    if isinstance(node, dict):
        if any(key in {"anyOf", "oneOf", "allOf"} for key in node):
            return True
        return any(_contains_combiners(value) for value in node.values())
    if isinstance(node, list):
        return any(_contains_combiners(value) for value in node)
    return False


def test_checked_spec_is_valid():
    result = _run_script("--spec-path", str(CANONICAL_SPEC))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Foundry validation passed." in result.stdout


def test_generate_produces_constrained_spec(tmp_path: Path):
    generated_spec_path = tmp_path / "openapi.foundry.generated.json"
    result = _run_script("--generate", "--spec-path", str(generated_spec_path))

    assert result.returncode == 0, result.stdout + result.stderr
    assert generated_spec_path.exists()

    generated = json.loads(generated_spec_path.read_text(encoding="utf-8"))
    assert generated["openapi"].startswith("3.0")
    assert generated["servers"] == [{"url": EXPECTED_SERVER_URL}]
    assert set(generated["paths"]) == EXPECTED_PATHS
    assert not _contains_combiners(generated)


def test_generate_respects_server_url_override(tmp_path: Path):
    generated_spec_path = tmp_path / "openapi.foundry.generated.json"
    custom_server_url = "http://localhost:8080"
    result = _run_script(
        "--generate",
        "--spec-path",
        str(generated_spec_path),
        "--server-url",
        custom_server_url,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    generated = json.loads(generated_spec_path.read_text(encoding="utf-8"))
    assert generated["servers"] == [{"url": custom_server_url}]
