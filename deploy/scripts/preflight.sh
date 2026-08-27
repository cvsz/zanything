#!/usr/bin/env bash
set -euo pipefail
fail=0
for cmd in python3 curl; do
  if command -v "$cmd" >/dev/null; then echo "OK: $cmd"; else echo "MISSING: $cmd"; fail=1; fi
done
python3 -m venv --help >/dev/null 2>&1 || { echo "MISSING: python3 venv support"; fail=1; }
command -v docker >/dev/null && echo "OPTIONAL OK: docker" || echo "OPTIONAL: docker not installed"
command -v kubectl >/dev/null && echo "OPTIONAL OK: kubectl" || echo "OPTIONAL: kubectl not installed"
command -v helm >/dev/null && echo "OPTIONAL OK: helm" || echo "OPTIONAL: helm not installed"
exit "$fail"
