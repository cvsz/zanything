# Observability Standard

## Logs
Structured JSON with:
- timestamp
- level
- service
- request_id
- trace_id
- operation
- integration
- latency_ms
- outcome

Never log credentials or bearer tokens.

## Metrics
- request rate/errors/duration
- task completion/failure
- queue depth
- worker saturation
- integration latency/error rate
- high-impact confirmations
- provider cost/tokens where applicable

## Tracing
Use OpenTelemetry-compatible tracing across API → workers → integrations.

## Reliability
Define SLOs and alerts for:
- availability
- latency
- error rate
- queue delay
- provider/integration failures
