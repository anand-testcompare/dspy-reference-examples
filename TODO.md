# Foundry OpenAPI Deployment TODO (AI-First)

## Status Board

- [x] M1 Generate `openapi.foundry.json` from FastAPI
- [x] M2 Enforce Foundry OpenAPI constraints in generated spec
- [x] M3 Add explicit `operation_id` values for the 3 classify routes
- [x] M4 Ensure Docker image is compute-module compatible (`linux/amd64`, numeric non-root user, non-`latest` tag flow)
- [x] M5 Attach OpenAPI to image via `server.openapi` label
- [x] M6 Add local validation command/tests for spec + image metadata
- [x] M7 Prepare exact build/push/import command sequence
- [ ] H1 Provide artifact registry push credentials/token
- [ ] H2 Do Foundry UI actions: link image, detect/import functions
- [ ] H3 Approve/configure OpenRouter egress + secret wiring
- [ ] H4 Final acceptance smoke test in Foundry

## Targets (Fill In)

Replace these with values from your Foundry enrollment:

- `FOUNDRY_URL=https://<your-stack>.palantirfoundry.com`
- `COMPUTE_MODULE_RID=ri.foundry.main.deployed-app.<uuid>`
- `FOUNDRY_REPOSITORY=<artifact-repository-name>`
- `FOUNDRY_PROJECT_PATH=/<project>/<folder>/<repo>`

## Contract Definition (Final)

- Allowed operations only:
  - `POST /classify/ae-pc` (`operationId=classifyAePc`)
  - `POST /classify/ae-category` (`operationId=classifyAeCategory`)
  - `POST /classify/pc-category` (`operationId=classifyPcCategory`)
- Static OpenAPI artifact: `openapi.foundry.json`
- Required constraints:
  - OpenAPI `3.0.x` (`3.0.3` emitted)
  - `servers = [{"url": "http://localhost:5000"}]`
  - one response code per operation
  - one response content type per operation: `application/json`
  - no `anyOf`, `oneOf`, `allOf`

## Commands (Copy/Paste)

```bash
uv run python scripts/deploy/foundry_openapi.py --generate --spec-path openapi.foundry.json
uv run python scripts/deploy/foundry_openapi.py --spec-path openapi.foundry.json
```

Build and validate image metadata:

```bash
export REGISTRY_HOST="<from Foundry Container tab>"
export IMAGE_NAME="dspy-reference-examples"
export IMAGE_TAG="$(date -u +%Y%m%d-%H%M%S)-$(git rev-parse --short HEAD)"
export IMAGE_REF="${REGISTRY_HOST}/${FOUNDRY_REPOSITORY}/${IMAGE_NAME}:${IMAGE_TAG}"
export OPENAPI_JSON="$(uv run python -c 'import json; print(json.dumps(json.load(open("openapi.foundry.json")), separators=(",", ":")))')"

docker buildx build \
  --platform linux/amd64 \
  --build-arg SERVER_OPENAPI="${OPENAPI_JSON}" \
  --tag "${IMAGE_REF}" \
  --load \
  .

uv run python scripts/deploy/foundry_openapi.py \
  --spec-path openapi.foundry.json \
  --image-ref "${IMAGE_REF}"
```

Push and import sequence is documented in `docs/foundry-openapi-runbook.md`.

Local verification evidence:

- `uv run python scripts/deploy/foundry_openapi.py --spec-path openapi.foundry.json --image-ref dspy-reference-examples:foundry-local` -> passed
- `docker run -e DSPY_PROVIDER=local ...` then `GET /health` -> `{"status":"ok",...}`

## Human Blockers (Only)

1. H1: Provide `REGISTRY_HOST`, `FOUNDRY_REGISTRY_USER`, and short-lived registry token.
2. H2: In Foundry UI, link image + run `Detect from OpenAPI specification` import.
3. H3: Approve egress to `openrouter.ai:443` and map `OPENROUTER_API_KEY` secret.
4. H4: Execute final smoke test from imported Foundry functions.
