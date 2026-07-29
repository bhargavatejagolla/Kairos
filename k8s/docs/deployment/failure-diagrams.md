# Kubernetes Failure & Traffic Diagrams

## API Pod Crash Recovery

This diagram demonstrates how Kubernetes handles a catastrophic crash within an API pod seamlessly.

```mermaid
sequenceDiagram
    participant User
    participant Ingress
    participant Service
    participant Pod A
    participant Kubelet
    participant Pod B (New)

    User->>Ingress: GET /api/v1/incidents
    Ingress->>Service: Forward Request
    Service->>Pod A: Route Traffic
    Note over Pod A: Critical Error / OOM Killed
    Pod A-->>Kubelet: Process Exited (Crash)
    Kubelet-->>Service: Mark Pod A as Unready
    Note over Service: Instantly removes Pod A from routing pool
    Kubelet->>Pod B (New): Spin up replacement pod
    User->>Ingress: GET /api/v1/incidents (Retry)
    Ingress->>Service: Forward Request
    Note over Pod B (New): Startup Probe Passes
    Service->>Pod B (New): Route Traffic
    Pod B (New)-->>User: 200 OK
```

## Zero Downtime Rolling Update

This diagram demonstrates how traffic is handled during a new release rollout without dropping connections.

```mermaid
sequenceDiagram
    participant LoadBalancer
    participant Old Pod (v1)
    participant New Pod (v2)
    participant Kubernetes

    Note over Kubernetes: Developer triggers deployment v2
    Kubernetes->>New Pod (v2): Create container
    LoadBalancer->>Old Pod (v1): Send live user traffic
    New Pod (v2)-->>Kubernetes: /health returns 200 OK (Startup Passed)
    New Pod (v2)-->>Kubernetes: /ready returns 200 OK (Ready Passed)
    Note over Kubernetes: New Pod is added to Service Pool
    Kubernetes->>Old Pod (v1): Send SIGTERM (Initiate Graceful Shutdown)
    Old Pod (v1)-->>Kubernetes: /ready instantly returns 503
    Note over Kubernetes: Old Pod removed from Service Pool
    LoadBalancer->>New Pod (v2): Route all NEW traffic here
    Note over Old Pod (v1): Finishes processing active requests
    Old Pod (v1)-->>Kubernetes: Exits cleanly
```
