<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=300&section=header&text=KAIROS&fontSize=120&animation=twinkling&fontAlignY=38&desc=Enterprise%20AI%20Site%20Reliability%20Engineer&descAlignY=55&descAlign=50" width="100%" />

  <h3>🧠 Intelligent Incident Response | 📊 AI-Driven Telemetry | ⚡ Distributed Execution</h3>

  <p align="center">
    <a href="https://github.com/bhargavatejagolla"><img src="https://img.shields.io/badge/Architected_By-Golla_Bhargava_Teja-000000?style=for-the-badge&logo=github&logoColor=white" alt="Architect" /></a>
    <a href="https://github.com/bhargavatejagolla/Kairos/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/bhargavatejagolla/Kairos/ci.yml?branch=main&label=CI%2FCD&logo=githubactions&logoColor=white&style=for-the-badge" alt="Build Status" /></a>
    <a href="#"><img src="https://img.shields.io/badge/Platform-Cloud_Native_Enterprise-4169E1?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Platform" /></a>
    <a href="#"><img src="https://img.shields.io/badge/AI_Engine-Groq%20%7C%20Llama_3-F55036?style=for-the-badge&logo=openai&logoColor=white" alt="AI Engine" /></a>
    <br/>
    <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI" /></a>
    <a href="https://reactjs.org/"><img src="https://img.shields.io/badge/Frontend-React%20%7C%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React" /></a>
    <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/Vector_DB-pgvector-336791?style=for-the-badge&logo=postgresql" alt="PostgreSQL" /></a>
    <a href="https://redis.io/"><img src="https://img.shields.io/badge/Broker-Redis-DC382D?style=for-the-badge&logo=redis" alt="Redis" /></a>
    <br/>
    <a href="https://opentelemetry.io/"><img src="https://img.shields.io/badge/Tracing-OpenTelemetry-2496ED?style=for-the-badge&logo=opentelemetry" alt="OpenTelemetry" /></a>
    <a href="https://kustomize.io/"><img src="https://img.shields.io/badge/Deploy-Kustomize-326CE5?style=for-the-badge&logo=kubernetes" alt="Kustomize" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License" /></a>
  </p>

  <p align="center">
    <a href="https://readme-typing-svg.herokuapp.com"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=20&duration=3000&pause=1000&color=F55036&center=true&vCenter=true&repeat=true&width=800&height=50&lines=Transform+Production+Incidents+into+Organizational+Knowledge;Autonomous+AI-Powered+Telemetry+Correlation;Vector+Similarity+Search+for+Rapid+Triage;Robust+Distributed+Processing+Engine;Deployed+via+Kubernetes+%26+Cloud+Native+Infrastructure" alt="Typing SVG" /></a>
  </p>
</div>

---

<details open>
<summary><b>📚 Table of Contents</b></summary>

- [🌟 The Problem: Swivel-Chair DevOps](#-the-problem-swivel-chair-devops)
- [💡 The Solution: Autonomous AI SRE](#-the-solution-autonomous-ai-sre)
- [🎯 Core Use Cases](#-core-use-cases)
- [⚙️ How It Works (Event-Driven Architecture)](#️-how-it-works-event-driven-architecture)
- [🛠️ Deep Dive: The Technology Stack](#️-deep-dive-the-technology-stack)
- [🏗️ Complete Enterprise Architecture](#-complete-enterprise-architecture)
- [🚀 Detailed Installation & Quick Start](#-detailed-installation--quick-start)
- [🌐 Accessing the Services](#-accessing-the-services)
- [🤝 Authors & Contributors](#-authors--contributors)

</details>

---

## 🌟 The Problem: Swivel-Chair DevOps

In modern enterprise environments (Site Reliability Engineering & DevOps), debugging production failures is a chaotic, fragmented nightmare. When an outage occurs, engineers are forced to play detective across disconnected, noisy tools:

<div align="center">
  <table>
    <tr>
      <td align="center"><img src="https://img.icons8.com/color/48/000000/grafana.png"/><br/><b>Grafana</b><br/>Searching for CPU/Memory spikes</td>
      <td align="center"><img src="https://img.icons8.com/color/48/000000/log.png"/><br/><b>Loki / ELK</b><br/>Scouring for error traces</td>
      <td align="center"><img src="https://img.icons8.com/color/48/000000/kubernetes.png"/><br/><b>Kubernetes</b><br/>Checking for CrashLoopBackOff</td>
      <td align="center"><img src="https://img.icons8.com/color/48/000000/github.png"/><br/><b>GitHub CI/CD</b><br/>Checking who broke the build</td>
    </tr>
  </table>
</div>

This **"Swivel-Chair DevOps"** wastes precious time. Furthermore, when the incident is finally resolved, the knowledge of *how* it was fixed lives only in a senior engineer's head or gets buried in an unread Slack channel. **The next time the exact same error happens, the team wastes another 3 hours solving it all over again.**

<br/>

## 💡 The Solution: Autonomous AI SRE

**KAIROS** acts as a centralized, autonomous **AI SRE**. 

It connects directly to your infrastructure, reads your logs and metrics in real-time, correlates them using Advanced LLMs (**Groq / Llama 3**), and generates plain-English root-cause analyses. 

Crucially, it commits every solved incident to a **Vector Database (pgvector)**, giving your organization a permanent, queryable "long-term memory" of how to fix production bugs.

<br/>

---

## 🎯 Core Use Cases

KAIROS radically transforms how engineering teams operate, shifting them from a reactive panic state to a proactive, automated mindset:

| ⚡ Use Case | ❌ Before KAIROS | ✅ After KAIROS |
| :--- | :--- | :--- |
| **🚨 Outage Triage** | Panic. 5 engineers on a Zoom call frantically checking different dashboards. | KAIROS automatically ingests the failing logs, correlates them with a recent code deployment, and tells you exactly what broke. |
| **📝 Root Cause Analysis (RCA)** | Writing RCAs takes days. Details are forgotten, and documents are sloppy. | KAIROS automatically generates a blameless, detailed Markdown RCA document the second the incident is resolved. |
| **🧠 Organizational Memory** | Junior engineers get stuck on bugs that senior engineers solved months ago. | When a junior engineer pastes an error trace, KAIROS performs a Vector Similarity Search and says: *"This is a Redis Timeout. John solved this 3 months ago by increasing the connection pool. Here is the playbook."* |
| **🔇 Alert Fatigue** | Slack is flooded with meaningless Prometheus CPU alerts that everyone ignores. | Alerts are intercepted by the KAIROS Background Workers, evaluated by AI, and only escalated to humans if they actually impact user experience. |

<br/>

---

## ⚙️ How It Works (Event-Driven Architecture)

KAIROS executes complex workflows through a decoupled, asynchronous pipeline designed for high throughput:

1. **Collect (Telemetry):** The platform continuously listens to your OpenTelemetry streams, Prometheus metrics, and Kubernetes events.
2. **Correlate (Context Window):** When an anomaly occurs, KAIROS bundles the raw JSON logs, the time-series metrics, and recent CI/CD deployments into a massive context window.
3. **Analyze (LLM Inference):** This context is sent to the ultra-fast Groq API (running Llama 3). The AI reasons over the data and extracts the exact root cause, filtering out the noise.
4. **Remember (Vectorization):** Once the incident is marked "Resolved", KAIROS converts the incident narrative into high-dimensional vector embeddings using HuggingFace embeddings.
5. **Retrieve (Semantic Search):** These embeddings are stored in PostgreSQL via `pgvector`. Future incidents are instantly matched against this database using cosine similarity.

<div align="center">

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#1E1E1E', 'textColor': '#FFFFFF', 'edgeLabelBackground':'#1E1E1E' }}}%%
flowchart TD
    A([📡 COLLECT]) -.->|Gather logs, metrics, events| B([🔗 CORRELATE])
    B -.->|Build unified timeline| C([🧠 ANALYZE])
    C -.->|Groq LLM synthesizes root-cause| D([💾 REMEMBER])
    D -.->|Generate vector embeddings| E([🔍 RETRIEVE])
    E -.->|Instantly match anomalies to past fixes| A

    style A fill:#4169E1,stroke:#FFFFFF,stroke-width:2px,color:#fff
    style B fill:#009688,stroke:#FFFFFF,stroke-width:2px,color:#fff
    style C fill:#F55036,stroke:#FFFFFF,stroke-width:2px,color:#fff
    style D fill:#336791,stroke:#FFFFFF,stroke-width:2px,color:#fff
    style E fill:#DC382D,stroke:#FFFFFF,stroke-width:2px,color:#fff
```

</div>

<br/>

---

## 🛠️ Deep Dive: The Technology Stack

We didn't just build an app; we built an **enterprise-grade distributed platform**. Here is exactly what tools we chose and *why*:

### 1. 🧠 The Intelligence Layer (Backend API)
* **Python 3.12 & FastAPI**: Chosen over Node/Go because Python is the undisputed king of AI/ML integration. FastAPI provides blazingly fast asynchronous routing, Pydantic data validation, and auto-generated OpenAPI docs.
* **Clean Architecture**: The codebase is strictly decoupled into Routers, Services, Repositories, and Core domains. You can swap out the database or AI provider without rewriting the business logic.
* **Security & Auth**: Built-in Role-Based Access Control (RBAC), multi-tenancy support, JWT token validation, and OWASP-compliant middleware.

### 2. ⚡ The Execution Layer (Background Jobs)
* **Celery & Redis Broker**: AI API calls (like sending a massive log chunk to an LLM) take time. If we did this on the main FastAPI thread, the server would lock up. We use Celery and Redis to push heavy AI reasoning and email notifications into asynchronous background queues, ensuring 100% API responsiveness.

### 3. 🗄️ The Memory Layer (Databases)
* **PostgreSQL 16**: The world's most robust relational database. Used for storing Users, RBAC Policies, Organizations, and Projects.
* **pgvector**: Instead of paying for expensive external vector databases (like Pinecone), we installed the `pgvector` extension directly into Postgres. This allows us to perform mathematical similarity searches (Cosine Distance) on historical incidents right alongside our relational data.
* **Redis Cache**: Used for lightning-fast rate limiting (preventing DDoS attacks) and caching heavy API responses via `FastAPICache`.

### 4. 🖥️ The Presentation Layer (Frontend)
* **React 19 & Vite**: React provides a component-driven UI. Vite ensures millisecond build times. 
* **TailwindCSS v4**: Allows us to build a gorgeous, dark-mode-first, fully responsive enterprise dashboard.
* **Framer Motion**: Adds butter-smooth micro-animations that make the platform feel premium and alive.
* **TanStack Query & Zustand**: State management handles robust server-state caching and instantaneous global state mutations without prop-drilling.

### 5. 🚢 The Infrastructure & CI/CD Layer
* **Kubernetes (k3d / Kustomize)**: The entire stack is containerized and managed by Kubernetes. We use Kustomize to manage environment-specific configurations (`base`, `local`, `production`) without the complexity of Helm charts.
* **Horizontal Pod Autoscaling (HPA)**: The system automatically spins up clone API pods if CPU usage spikes past 70%.
* **GitHub Actions**: Fully automated pipelines that run 95+ pytest unit/integration tests, build immutable Docker images, and push them to the GitHub Container Registry (GHCR) on every single commit.

<br/>

---

## 🏗️ Complete Enterprise Architecture

<div align="center">
  <img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png" width="100%" />
</div>

```mermaid
graph TB
    subgraph "1️⃣ Presentation Layer"
        UI[🖥️ React Dashboard<br/>Vite / Tailwind / Framer]
        GRAF[📊 Grafana Dashboards<br/>Metrics Vis]
    end

    subgraph "2️⃣ Intelligence & API Layer"
        API[⚡ KAIROS Core API<br/>FastAPI / Python 3.12]
        COLL[📥 Telemetry Collector<br/>Webhooks / gRPC]
        AI[🤖 AI Service<br/>Groq Llama 3]
    end

    subgraph "3️⃣ Distributed Execution"
        RED[(🔥 Redis<br/>Message Broker)]
        WK_AI[🧠 AI Worker Pool<br/>Celery]
        WK_AL[🚨 Alert Worker Pool<br/>Celery]
        WK_NT[✉️ Notification Pool<br/>Celery]
    end

    subgraph "4️⃣ Storage & Memory Layer"
        PG[(🗄️ PostgreSQL 16<br/>Relational Data)]
        VEC[(🌌 pgvector<br/>Cosine Similarity)]
        CACHE[(⚡ Redis<br/>Rate Limits / Cache)]
    end

    subgraph "5️⃣ Observability Infrastructure"
        PROM[📈 Prometheus]
        LOKI[📜 Loki]
        OTEL[🔍 OpenTelemetry]
    end

    %% Flow Connections
    UI <-->|REST API| API
    API -->|Enqueue Jobs| RED
    RED -->|Consume| WK_AI
    RED -->|Consume| WK_AL
    RED -->|Consume| WK_NT
    
    WK_AI <-->|Inference| AI
    WK_AI <-->|Persist| PG
    WK_AI <-->|Vectorize| VEC
    API <-->|Read/Write| PG
    API <-->|Rate Limit| CACHE
    
    OTEL -->|Metrics| PROM
    OTEL -->|Logs| LOKI
    PROM -->|Alerts| COLL
    LOKI -->|Alerts| COLL
    COLL -->|Webhook| API
```

<br/>

---

## 🚀 Detailed Installation & Quick Start

Get the entire **KAIROS** platform running on your local machine in minutes. 

### 📋 Prerequisites
- **Docker Engine & Docker Compose** (Make sure the daemon is running)
- **Kubernetes** (`k3d`, `minikube`, or `kind`)
- **Python 3.12+ & Node.js 20+**
- **Make** (Build automation tool)

### ⚡ Option 1: Docker Compose (For Rapid Development)

If you are a developer looking to write code and test quickly without Kubernetes overhead:

```bash
# 1. Clone the repository
git clone https://github.com/bhargavatejagolla/kairos.git
cd kairos

# 2. Configure environment variables
cp backend/.env.example backend/.env
# Open backend/.env and inject your GROQ_API_KEY to enable AI capabilities.

# 3. Launch the entire microservice platform in detached mode
docker-compose up -d --build

# 4. View logs to ensure Celery and FastAPI started correctly
docker-compose logs -f backend celery_worker
```

### ☸️ Option 2: Kubernetes (For Production/Enterprise Deployment)

If you want to simulate or deploy to a real cloud-native cluster with Autoscaling (HPA) and Ingress controllers:

```bash
# 1. Create a local k3d Kubernetes cluster with Ingress ports mapped to your localhost
make k3d-create

# 2. Deploy all Kustomize manifests (DB, Redis, Backend, Frontend, Ingress, HPA)
make deploy-local

# 3. Watch the pods spin up (Wait for them to reach 'Running' state)
kubectl get pods -n kairos -w

# 4. Check the Horizontal Pod Autoscaler status
kubectl get hpa -n kairos

# 5. (Optional) Run the disaster recovery / backup scripts
./k8s/scripts/backup_postgres.sh
```
> [!NOTE]
> For detailed operational debugging and production commands, refer to the [Production Runbook (docs/RUNBOOK.md)](docs/RUNBOOK.md).

<br/>

---

## 🌐 Accessing the Services

Once successfully deployed (via Compose or Kubernetes), access the respective portals via your browser:

| Service | URL | Description |
| :--- | :--- | :--- |
| **KAIROS React Dashboard** | `http://app.kairos.local` | Main interactive web interface for incident management |
| **FastAPI Swagger UI** | `http://api.kairos.local/docs` | Interactive OpenAPI documentation and API tester |
| **Flower (Celery Monitor)** | `http://localhost:5555` | GUI for monitoring async background jobs and worker health |

*(Note: If using Kubernetes locally, you must add `127.0.0.1 app.kairos.local api.kairos.local` to your machine's `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts` file to resolve the Ingress domain names).*

<br/>

---

## 🤝 Authors & Contributors

<div align="center">
  <a href="https://github.com/bhargavatejagolla">
    <img src="https://img.shields.io/badge/Architected_&_Engineered_By-Golla_Bhargava_Teja-000000?style=for-the-badge&logo=github&logoColor=white&scale=1.5" alt="Author" />
  </a>
</div>

<br/>

We welcome contributions from developers, DevOps engineers, and SREs! 
1. **Fork** the repository
2. **Create** your feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request against the `main` branch.

<br/>

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=timeGradient&height=120&section=footer" width="100%" />
</div>
