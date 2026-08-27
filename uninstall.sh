#!/usr/bin/env bash
set -Eeuo pipefail
[[ $EUID -eq 0 ]] || { echo "Run with sudo/root."; exit 1; }
systemctl disable --now anything-v2.service 2>/dev/null || true
rm -f /etc/systemd/system/anything-v2.service
systemctl daemon-reload
echo "Service removed. /opt/anything-v2 and /etc/anything-v2 are preserved for recovery."
