#!/usr/bin/env bash

set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-dspy-reference-examples:portability}"
TARGET_PLATFORM="${TARGET_PLATFORM:-linux/amd64}"
SPEC_PATH="${SPEC_PATH:-openapi.foundry.json}"
BUILD_IMAGE="${BUILD_IMAGE:-1}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required"
  exit 1
fi

if [[ "${BUILD_IMAGE}" == "1" ]]; then
  if [[ ! -f "${SPEC_PATH}" ]]; then
    echo "missing Foundry OpenAPI spec: ${SPEC_PATH}"
    exit 1
  fi

  if ! command -v uv >/dev/null 2>&1; then
    echo "uv is required to load ${SPEC_PATH} for image labeling"
    exit 1
  fi

  OPENAPI_JSON="$(uv run python -c 'import json, sys; print(json.dumps(json.load(open(sys.argv[1], encoding="utf-8")), separators=(",", ":")))' "${SPEC_PATH}")"

  echo "Building ${IMAGE_NAME} for ${TARGET_PLATFORM}..."
  docker build \
    --platform "${TARGET_PLATFORM}" \
    --build-arg SERVER_OPENAPI="${OPENAPI_JSON}" \
    -t "${IMAGE_NAME}" \
    .
fi

check_health() {
  local host_port="$1"
  local attempts=40
  for _ in $(seq 1 "${attempts}"); do
    if curl -fsS "http://127.0.0.1:${host_port}/health" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 1
}

run_profile() {
  local profile_name="$1"
  local app_port="$2"
  local host_port="$3"

  echo "Running ${profile_name} profile (PORT=${app_port}, host=${host_port})..."
  local container_id
  container_id="$(docker run -d --rm -e PORT="${app_port}" -e DSPY_PROVIDER=local -p "${host_port}:${app_port}" "${IMAGE_NAME}")"
  trap 'docker rm -f "${container_id}" >/dev/null 2>&1 || true' RETURN

  if ! check_health "${host_port}"; then
    echo "Profile ${profile_name} failed health check"
    docker logs "${container_id}" || true
    exit 1
  fi

  echo "Profile ${profile_name} passed"
  docker rm -f "${container_id}" >/dev/null 2>&1 || true
  trap - RETURN
}

run_profile "railway-like" 8080 18080
run_profile "foundry-like" 5000 15000

echo "Portability smoke test passed for Railway and Foundry runtime profiles."
