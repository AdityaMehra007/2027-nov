#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE:-http://127.0.0.1:8765}"
curl -sS "$BASE/healthz"
echo
curl -sS -X POST "$BASE/v1/tasks" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Draft a research plan","action":"demo.echo","action_class":"draft","payload":{"topic":"Evaluate user workflow"}}'
echo
