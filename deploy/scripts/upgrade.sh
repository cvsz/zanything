#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo/root."; exit 1; }
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${APP_DIR:-/opt/anything-v2}"
BACKUP_DIR="${BACKUP_DIR:-/opt/anything-v2-backups}"
mkdir -p "$BACKUP_DIR"
stamp="$(date +%Y%m%d-%H%M%S)"
if [[ -d "$APP_DIR" ]]; then
  tar -C "$(dirname "$APP_DIR")" -czf "$BACKUP_DIR/anything-v2-$stamp.tgz" "$(basename "$APP_DIR")"
fi
exec "$SCRIPT_DIR/install.sh"
