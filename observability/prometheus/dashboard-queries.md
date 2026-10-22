# Voting App Prometheus Dashboard Queries

## 1. Request rate (requests per second)

```promql
sum(rate(vote_http_requests_total[5m]))
```

## 2. 95th-percentile request latency (p95, seconds)

```promql
histogram_quantile(
  0.95,
  sum by (le) (
    rate(vote_http_request_duration_seconds_bucket[5m])
  )
)
```

## 3. HTTP 5xx error rate (percentage)

```promql
100 *
(
  sum(rate(vote_http_requests_total{http_status=~"5.."}[5m]))
  or vector(0)
)
/
clamp_min(sum(rate(vote_http_requests_total[5m])), 1e-9)
```

## Notes

- The Vote service exposes metrics at `/metrics`.
- Prometheus scrapes the service every 15 seconds.
- The error-rate query returns zero when no 5xx series exists.
- Zero means no 5xx rate was recorded in the window, not that errors
  are impossible.
- Evaluate p95 latency under sustained, representative traffic before
  defining an SLO.

## 4. Availability SLO (proposed)

- **Objective:** 99% of Vote-service HTTP requests return a non-5xx status.
- **Window:** Rolling 30 days.
- **Measurement:** Successful requests divided by all recorded requests.
- **Error budget:** 1% of requests may return HTTP 5xx responses.
- **Status:** Proposed; evaluate under representative traffic before treating it as an operational commitment.

PromQL (success ratio):

```promql
1 -
(
  sum(rate(vote_http_requests_total{http_status=~"5.."}[5m]))
  /
  clamp_min(sum(rate(vote_http_requests_total[5m])), 1e-9)
)

## 5. Error-budget burn rate

For the proposed 99% availability SLO, the allowed error ratio is 1%.

```promql
(
  sum(rate(vote_http_requests_total{http_status=~"5.."}[1h]))
  /
  clamp_min(sum(rate(vote_http_requests_total[1h])), 1e-9)
) / 0.01

## Incident Drill: HTTP 5xx Alert

- **Scenario:** Simulated an HTTP 500 incident using a temporary local-only test endpoint.
- **Detection:** Prometheus transitioned `VotingAppHighHttp5xxRate` to Firing after the HTTP 5xx rate exceeded 5% for the configured 2-minute duration.
- **Recovery:** Removed the temporary endpoint and rebuilt the Vote service.
- **Verification:** The Vote page returned HTTP 200; the removed test endpoint returned HTTP 404.
- **Impact:** Controlled local test only; no AWS or production environment involved.
- **Lesson learned:** Prometheus alert rules can detect sustained HTTP 5xx errors. Future work includes notification delivery, a formal recovery-time measurement, and a fuller postmortem.
