#!/usr/bin/env bash
set -Eeuo pipefail

APP_USER="${APP_USER:-anything}"
APP_DIR="${APP_DIR:-/opt/anything-v2}"
ETC_DIR="${ETC_DIR:-/etc/anything-v2}"

log(){ printf '[anything] %s\n' "$*"; }
die(){ printf '[anything] ERROR: %s\n' "$*" >&2; exit 1; }

[[ $EUID -eq 0 ]] || die "Run with sudo/root."
command -v python3 >/dev/null || die "python3 is required."
command -v curl >/dev/null || die "curl is required."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

log "Running pre-flight checks..."
"$SCRIPT_DIR/preflight.sh"

if ! id "$APP_USER" >/dev/null 2>&1; then
  useradd --system --home "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
fi

install -d -m 0755 "$APP_DIR" "$ETC_DIR"
rm -rf "$APP_DIR/api" "$APP_DIR/gui"
cp -a "$BASE_DIR/enterprise/api" "$APP_DIR/"
cp -a "$BASE_DIR/enterprise/gui" "$APP_DIR/"

python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/api/requirements.txt"

if [[ ! -f "$ETC_DIR/anything.env" ]]; then
  cp "$BASE_DIR/enterprise/config/anything.env.example" "$ETC_DIR/anything.env"
  chmod 0600 "$ETC_DIR/anything.env"
fi

install -m 0644 "$BASE_DIR/enterprise/deploy/systemd/anything-v2.service" /etc/systemd/system/anything-v2.service
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

systemctl daemon-reload
systemctl enable --now anything-v2.service

for _ in {1..20}; do
  if curl -fsS http://127.0.0.1:8080/healthz >/dev/null 2>&1; then
    log "Installed successfully."
    log "GUI/API: http://127.0.0.1:8080"
    exit 0
  fi
  sleep 1
done

systemctl --no-pager --full status anything-v2.service || true
die "Health verification failed."
