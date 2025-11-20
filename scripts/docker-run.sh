#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-my-playwright-tests:latest}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"


echo "[docker-run] Script dir:  $SCRIPT_DIR"
echo "[docker-run] Project root: $PROJECT_ROOT"
echo "[docker-run] Using image: $IMAGE_NAME"

if [ "$#" -eq 0 ]; then
  echo "[docker-run] Pytest args: <none>"
else
  echo "[docker-run] Pytest args: $*"
fi

if ! docker image inspect "$IMAGE_NAME" >/dev/null 2>&1; then
  echo "[docker-run] Image not found, building..."
  docker build -t "$IMAGE_NAME" "$PROJECT_ROOT"
fi

ENV_VARS=(STAND_USER LOCKED_USER PROBLEM_USER PERF_GLITCH_USER ERROR_USER VISUAL_USER PASSWORD)
DOCKER_ENV_ARGS=()
for VAR in "${ENV_VARS[@]}"; do
  if [[ -n "${!VAR-}" ]]; then
    DOCKER_ENV_ARGS+=(-e "$VAR")
  fi
done

echo "[docker-run] Running docker container..."
echo "[docker-run] docker run --rm -v \"$PROJECT_ROOT\":/app -w /app ${DOCKER_ENV_ARGS[*]} $IMAGE_NAME pytest $*"

docker run --rm \
  -v "$PROJECT_ROOT":/app \
  -w /app \
  "${DOCKER_ENV_ARGS[@]}" \
  "$IMAGE_NAME" \
  pytest "$@"