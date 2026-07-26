# KAIROS Architecture

## Overview
KAIROS is an enterprise AIOps and SRE platform. 
The backend is built with FastAPI, SQLAlchemy (Async), and PostgreSQL.

## Core Modules
- **Authentication**: JWT-based with Refresh tokens.
- **RBAC**: Strict role-based access control.
- **Organization & Project**: Tenant isolation.
- **Service Domain**: Catalog of monitored microservices and APIs.
- **Incident Domain**: State-machine driven incident response.

## Command Bus & Workflow Engine
The API layer contains zero business logic. Instead, REST controllers construct `Command` objects and dispatch them to the `CommandBus`.

```text
API -> CommandBus -> CommandHandler -> IncidentService -> WorkflowEngine -> Database
```

## Future Extensions (Phase 10)
Before implementing Alert Management, a **Correlation Engine** will be introduced as a shared platform component.

```text
Alert Sources
      │
      ▼
Correlation Engine
      │
 ├── Deduplication
 ├── Similarity Detection
 ├── Dependency Analysis
 ├── Time Window Correlation
 ├── Service Impact Analysis
 └── Incident Linking
      │
      ▼
Incident Workflow
```
This architecture prevents alert storms by intelligently grouping noisy alerts into a single actionable incident.
