from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "deploy" / "scripts"


def read_script(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8")


def test_install_is_fail_fast_and_health_verified():
    script = read_script("install.sh")
    assert "set -Eeuo pipefail" in script
    assert "systemctl restart anything-v2.service" in script
    assert "curl -fsS http://127.0.0.1:8080/healthz" in script
    assert 'die "Health verification failed."' in script


def test_upgrade_preserves_recovery_snapshot_before_install():
    script = read_script("upgrade.sh")
    backup = 'tar -C "$(dirname "$APP_DIR")" -czf "$BACKUP_DIR/anything-v2-$stamp.tgz"'
    install = 'exec "$SCRIPT_DIR/install.sh"'
    assert backup in script
    assert install in script
    assert script.index(backup) < script.index(install)


def test_uninstall_preserves_application_and_configuration_data():
    script = read_script("uninstall.sh")
    assert "rm -rf /opt/anything-v2" not in script
    assert "rm -rf /etc/anything-v2" not in script
    assert "/opt/anything-v2 and /etc/anything-v2 are preserved for recovery" in script
