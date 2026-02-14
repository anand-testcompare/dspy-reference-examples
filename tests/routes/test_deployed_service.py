"""Smoke tests for deployed environments addressed by BASE_URL."""

from __future__ import annotations

import os

import httpx
import pytest

BASE_URL = (os.getenv("BASE_URL") or "").rstrip("/")
if not BASE_URL:
    pytest.skip("BASE_URL is required for deployed smoke tests", allow_module_level=True)


@pytest.fixture(scope="module")
def client() -> httpx.Client:
    with httpx.Client(base_url=BASE_URL, timeout=30.0, follow_redirects=True) as smoke_client:
        yield smoke_client


def test_health(client: httpx.Client):
    response = client.get("/health")
    assert response.status_code == 200

    payload = response.json()
    assert payload.get("status") in {"ok", "degraded", "healthy"}


def test_root_endpoint(client: httpx.Client):
    response = client.get("/")
    assert response.status_code == 200

    payload = response.json()
    assert payload.get("name")
    assert payload.get("endpoints")


def test_openapi_contains_classify_routes(client: httpx.Client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json().get("paths", {})
    assert "/classify/ae-pc" in paths
    assert "/classify/ae-category" in paths
    assert "/classify/pc-category" in paths
