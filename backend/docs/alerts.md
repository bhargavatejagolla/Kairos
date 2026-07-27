# Alert Management Architecture

This document describes the Alert Management Domain within KAIROS, introduced in Phase 10.

## Overview
Alert Management in KAIROS is designed as an Enterprise Observability Platform. We do not conflate Signals with Alerts.
Instead, we orchestrate them through a rigid pipeline using the **Alert Workflow Engine**.

## Architecture Pipeline

```text
Prometheus / Loki / External Integrations
        │
        ▼
   Signal Ingestion (Immutable Telemetry)
        │
        ▼
   Rule Evaluation Engine (Stateless thresholds, > 90% CPU)
        │
        ▼
   Fingerprint Engine (Deterministic Deduplication)
        │
        ▼
   Alert Workflow Layer (The Master Orchestrator)
        │
    ┌───┴───┐
    ▼       ▼
Correlation  Policy Application (Incident Creation)
    │
    ▼
Alert Engine (Lifecycle: OPEN -> ACKNOWLEDGED -> RESOLVED)
```

## REST APIs & Integration
All APIs require a hierarchical Context (`Organization -> Project -> Service -> Alert Context`).
Telemetry endpoints expect `POST /api/v1/services/{service_id}/signals` payloads natively matching internal definitions, ready to accept Prometheus metrics.

## No Mock Data Policy
KAIROS is tested via full-stack automated Test Suites that generate synthetic signals and push them through the REST layer, allowing the engine to generate *real* Alerts and *real* Incidents. The database seed scripts only seed *Rules*, not fake alerts.
