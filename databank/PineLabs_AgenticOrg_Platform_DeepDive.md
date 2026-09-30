# 🔬 Pine Labs AgenticOrg Platform: Full Architecture Deep-Dive & Connection Blueprint

> **Platform**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`)  
> **Environment**: `https://agenticorg.hackathon.pinelabs.com`  
> **Tenant ID**: `abb61bca-a3f5-4aba-b30e-946016b13120`  
> **User Account**: `K.Sai Jaswanth Reddy` (`ksaijaswanthr.cs24@rvce.edu.in`) • **Role**: Domain Lead | Operations  
> **Connection Status**: **ESTABLISHED & VERIFIED** (Dual-Channel: Playwright Browser Session + Python stdlib REST API Bridge)

---

## 1. 🌐 Comprehensive System Module Audit (All 12 Modules Explored)

| # | Module | Route | Live Platform State & Capabilities Discovered |
|---|---|---|---|
| **1** | **Dashboard** | `/dashboard` | System Live v4.8.0. Shows 5 provisioned shadow agents, LangGraph v1.1 runtime, Grantex RS256 token authorization, and activity feed. |
| **2** | **Agent Fleet** | `/dashboard/agents` | 5 pre-installed system ops agents (`Vendor Manager`, `Contract Intelligence`, `Support Triage`, `Compliance Guard`, `It Operations`). 5-step Agent Creation Wizard: Persona $\rightarrow$ Role $\rightarrow$ System Prompt $\rightarrow$ Behavior $\rightarrow$ Review. |
| **3** | **Connectors** | `/dashboard/connectors` | **6 active pre-configured connectors** (`tally`, `zoho_books`, `gstn`, `banking_aa`, `stripe`, `pinelabs_plural`). **101 native connectors** in catalog. Custom connector registration supports REST Base URL + MCP auto-discovery with granular rate limiting. |
| **4** | **A2A / MCP Integrations** | `/dashboard/integrations` | External access via Python SDK (`agenticorg 0.3.0`), TypeScript SDK, CLI (`agenticorg agents run`), Grantex A2A protocol (54 skills), and native MCP tool gateway (`client.mcp.tools()`). OAuth-protected hosted MCP endpoint verified at `/.well-known/oauth-protected-resource/api/v1/marketplace-surface/hosted-mcp`. |
| **5** | **Workflows** | `/dashboard/workflows` | LangGraph v1.1 execution graph orchestration. Supports multi-agent pipelines, conditional routing, and scheduled cron triggers. |
| **6** | **Schema Registry** | `/dashboard/schemas` | 18 platform default data schemas (`Invoice`, `Payment`, `Order`, `Employee`, `Contract`, `Ticket`, `Vendor`, `Lead`, `Product`, etc.). Custom schemas can be created for domain validation. |
| **7** | **Knowledge Base** | `/dashboard/knowledge` | Vector RAG index supporting PDF, Word, Excel, Markdown, and Plain Text files with live semantic query search (`client.knowledge.search()`). |
| **8** | **Observatory** | `/dashboard/observatory` | Real-time operational command center: live workflow step execution, throughput graph (events/min), live agent feed, and transaction counter. |
| **9** | **Approvals** | `/dashboard/approvals` | Human-in-the-Loop (HITL) triage queue with priority tags (`Critical`, `High`, `Normal`, `Low`) triggered when agent confidence floor is breached. |
| **10** | **Scope Dashboard** | `/dashboard/scopes` | Granular permission boundary inspection (`READ`, `WRITE`, `DELETE`, `ADMIN`) across connectors with real-time denial rate telemetry. |
| **11** | **Audit Log** | `/dashboard/audit` | Immutable forensic audit log tracking every agent creation, tool invocation, and decision. Includes 1-click **Export Evidence Package** and CSV download. |
| **12** | **SLA Monitor & Templates** | `/dashboard/sla` & `/agent-templates` | Uptime tracking (99.9% target), P95 latency (<2s target), agent success rate (>95%), and HITL response time (<4 hrs). Buyer/Seller agent templates with authorized tool toggles. |

---

## 2. 🔌 Autonomous Connection Architecture (How Antigravity Connects)

Antigravity operates a **Dual-Channel High-Reliability Bridge**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   ANTIGRAVITY <-> AGENTICORG BRIDGE                    │
├───────────────────────────────────┬────────────────────────────────────┤
│ CHANNEL 1: PLAYWRIGHT BROWSER     │ CHANNEL 2: PYTHON REST CLIENT      │
│ (Visual, Interactive, Screen Rec) │ (High-Speed Headless Automation)   │
├───────────────────────────────────┼────────────────────────────────────┤
│ • Port 9222 DevTools Protocol     │ • Script: `src/pinelabs_agentic_   │
│ • Live authenticated tab (0)      │   bridge.py`                       │
│ • Full DOM & Canvas inspection    │ • Zero-dep stdlib `urllib`         │
│ • 60 FPS screen capture for final │ • Authenticated via Grantex RS256  │
│   hackathon video recording       │   session JWT + CSRF header        │
│ • Human-in-the-loop fallback      │ • Millisecond API query/monitoring │
└───────────────────────────────────┴────────────────────────────────────┘
```

### Verified Connection Telemetry
- **API Endpoint**: `https://agenticorg.hackathon.pinelabs.com/api/v1`
- **Active Scopes**: `agents:read`, `agents:write`, `workflows:read`, `workflows:write`, `approvals:read`, `approvals:write`, `audit:read`, `connectors:read`, `connectors:create`, `connectors:update`, `connectors:delete`
- **Ping Status**: `200 OK` across `/agents`, `/connectors`, `/workflows`, `/schemas`, `/audit`.

---

## 3. 🎯 Integration Action Plan for AcuDiag

1. **Connector 1: `pinelabs_plural`**: Already active in tenant. Provides order creation and payment authorization.
2. **Connector 2: `delhivery_acudiag` (Custom Mock Connector)**:
   - Base URL: Expose `01_Projects/AcuDiag/databank/03_Mock_Server/mock_server.py` via public tunnel.
   - Endpoints: Exact Delhivery documentation paths (`/api/cmu/create`, `/api/cmu/pincode`, `/api/v1/packages/json/`).
   - Hosts our **3 non-existent capabilities** with Chaos Injection.
3. **Connector 3: `gnani_acudiag` (Speech-to-Text & Text-to-Speech)**:
   - Registered as custom voice connector to convert customer audio to text and generate vocal responses.
4. **Knowledge Base Upload**:
   - Upload appliance acoustic failure signatures (`acudiag_appliance_specs.md`) to `/dashboard/knowledge`.
5. **Agent Creation**:
   - Register `AcuDiag Orchestrator` using System Prompt v3.0 via `pinelabs_agentic_bridge.py` or the Agent Wizard.
