# 🧠 AcuDiag: Knowledge Base, MCP & A2A Architectural Strategy

> **Platform Framework**: Pine Labs AgenticOrg (`v4.8.0` / LangGraph `v1.1`)  
> **Origin**: Strategic evaluation of the Pine Labs Webinar guidance (Prakhar Gour & Shubham) cross-referenced with AgenticOrg platform capabilities.

---

## 1. 📚 Knowledge Bases: How We Use Them & Why
* **Webinar Ground Truth**: Devansh Mangal asked if knowledge bases are like Gemini Gems or Claude Skills. Prakhar Gour clarified: Knowledge bases are vector-embedded document stores (`POST /knowledge`) that any agent in the tenant can search to retrieve domain ground truth.
* **AcuDiag Implementation**:
  - We maintain [`acudiag_appliance_specs.md`](file:///c:/Users/jaswa/Antigravity/01_Projects/AcuDiag/docs/acudiag_appliance_specs.md) containing the exact mechanical failure frequencies (1,450 Hz BPFO bearing spall, 320 Hz pump cavitation, 220 Hz belt squeal), OEM part SKUs (`BEAR-6205-2RS`), and standardized labor costs (₹1,250).
  - **Why It Elevates the Demo**: Instead of the LLM hallucinating repair fees or part numbers, AcuDiag explicitly cites its vector knowledge base. This proves enterprise grounding to the judges.

---

## 2. 🔌 Native Connectors vs. MCP: Why Native Wins
* **Webinar Ground Truth**:
  - Harshik asked if participants must build an external MCP server for every integration.
  - Prakhar responded: *"You can use MCP server, or you can use the existing connectors, the native connector that I just showed you, right? There are 100 plus connectors there. So, one of them must have satisfied your use case, right?"*
  - Multiple students (Vaani, Ameya) ran into severe blockers with external MCPs (missing authorized tools, tunnel timeouts, authentication JSON format issues).
  - Prakhar explicitly advised: *"Focus on 3 aspects: agent creation, connectors, and agent intelligence—this covers 60–70% of the platform."*
* **AcuDiag Implementation**:
  - We adopt **100% Native Typed Connectors** (`pinelabs_plural`, `whatsapp`, `gstn`, `zendesk`, `tally`) from the official [`mishrasanjeev/agentic-org`](https://github.com/mishrasanjeev/agentic-org) codebase.
  - **Advantage**: Zero tunneling instability, zero auth payload errors, and complete Grantex namespace isolation (`connector__tool`), preventing the MCP tool collision issues raised by Sathish Babu.

---

## 3. 🤖 A2A Protocol (Agent-to-Agent): The External Enterprise Bridge
* **Platform Ground Truth**: AgenticOrg implements Google's Agent-to-Agent (A2A) protocol where agents publish Agent Cards to be discovered by external agents.
* **Prakhar's Architectural Warning**: Prakhar cautioned against fragmenting your internal business logic into 5 separate agents that struggle to coordinate via sub-prompts. He recommended the **SRE Single-Agent Paradigm** (one deterministic agent controlling all tools).
* **AcuDiag Implementation**:
  - **Internal Architecture**: AcuDiag operates as a single unified orchestrator owning all 14 connectors, ensuring deterministic, non-flaky execution of the 6 physical invariants.
  - **A2A External Exposure**: AcuDiag exposes an A2A Agent Card (`AcuDiag Reliability Orchestrator`) so external OEM warranty bots (e.g. Godrej or Whirlpool enterprise agents) can query AcuDiag's diagnostic verdict via standard agent-to-agent negotiation.
