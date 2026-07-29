# Deployment Strategy

## Overview
KAIROS uses a **RollingUpdate** deployment strategy combined with **Horizontal Pod Autoscaling (HPA)** and **Pod Disruption Budgets (PDB)** to guarantee zero-downtime upgrades and high availability.

## Strategy Definition
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```

- `maxUnavailable: 0` ensures that Kubernetes will never kill an existing running pod until a new replacement pod is fully Ready.
- `maxSurge: 1` allows Kubernetes to spin up one extra pod above the replica limit during the rollout process to take over traffic seamlessly.

## Image Versioning
We use **immutable image tags** (Git commit hashes) rather than `latest`. 
Example: `kairos-api:a3f4b2c`
This ensures that if a bad deployment occurs, rolling back is exactly deterministic. 

## Rollback Procedure
If an issue is detected post-deployment, rollback immediately using:
```bash
kubectl rollout undo deployment/backend -n kairos
```
Kubernetes maintains a ReplicaSet history and will seamlessly transition traffic back to the previous stable ReplicaSet.

## Graceful Shutdown
Our backend API listens for `SIGTERM` signals. Upon receiving the signal from Kubernetes:
1. It instantly fails its `/ready` probe, causing the Load Balancer to stop sending new requests.
2. It waits for all currently executing requests to finish processing.
3. It closes the database connection cleanly.
4. It exits successfully.
