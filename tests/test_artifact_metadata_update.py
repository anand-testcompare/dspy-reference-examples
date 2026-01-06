"""Tests for updating artifact metadata on load."""

from __future__ import annotations

import json

from src.serving.service import _update_artifact_model_metadata


def test_update_artifact_model_metadata_updates_model(tmp_path):
    model_path = tmp_path / "artifact.json"
    model_path.write_text(
        json.dumps({"metadata": {"model": "old-model", "classification_type": "ae-pc"}}),
        encoding="utf-8",
    )

    _update_artifact_model_metadata(model_path, "new-model")

    data = json.loads(model_path.read_text(encoding="utf-8"))
    assert data["metadata"]["model"] == "new-model"
    assert data["metadata"]["classification_type"] == "ae-pc"


def test_update_artifact_model_metadata_no_change_when_equal(tmp_path):
    model_path = tmp_path / "artifact.json"
    original = json.dumps({"metadata": {"model": "same-model", "classification_type": "ae-pc"}}, indent=2) + "\n"
    model_path.write_text(original, encoding="utf-8")

    _update_artifact_model_metadata(model_path, "same-model")

    assert model_path.read_text(encoding="utf-8") == original


def test_update_artifact_model_metadata_adds_metadata(tmp_path):
    model_path = tmp_path / "artifact.json"
    model_path.write_text(json.dumps({"foo": "bar"}), encoding="utf-8")

    _update_artifact_model_metadata(model_path, "new-model")

    data = json.loads(model_path.read_text(encoding="utf-8"))
    assert data["metadata"]["model"] == "new-model"
