# Anything Enterprise Quickstart

This package extends Anything v2 into an enterprise deployment scaffold with a GUI, API,
integration contract, security baseline, CI, installers, Docker, Kubernetes, Helm, and systemd.

## Linux one-click

```bash
cd anything-v2
./enterprise/installer/preflight.sh
sudo ./enterprise/installer/install.sh
```

Then open:

`http://127.0.0.1:8080`

## Docker

```bash
docker compose -f enterprise/deploy/docker/docker-compose.yml up -d --build
```

## Kubernetes

```bash
kubectl apply -f enterprise/deploy/k8s/
```

## Helm

```bash
helm upgrade --install anything-v2 enterprise/deploy/helm/anything-v2   --namespace anything-v2 --create-namespace
```

## Upgrade

```bash
sudo ./enterprise/installer/upgrade.sh
```

## Important production integrations still required

Before public production deployment, connect:
- enterprise identity provider
- secret manager
- persistent database/queue/object storage
- actual AI/tool providers
- TLS ingress/reverse proxy
- network-policy allow rules
- observability backend
- backup/restore targets

The included API is an orchestration/integration scaffold, not a pre-bound external provider implementation.
