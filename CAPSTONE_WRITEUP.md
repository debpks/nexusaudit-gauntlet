# 🛡️ NexusAudit-Gauntlet: Autonomous DevSecOps & AI Safety Compliance Auditor

[![GitHub Repository](https://img.shields.io/badge/GitHub-debpks%2Fnexusaudit--gauntlet-181717?logo=github)](https://github.com/debpks/nexusaudit-gauntlet)
[![Google 5-Day AI Intensive](https://img.shields.io/badge/Kaggle-5--Day%20AI%20Agents%20Intensive-20BEFF?logo=kaggle)](https://www.kaggle.com/)
[![Live Cloud Run Demo](https://img.shields.io/badge/Google%20Cloud%20Run-Live%20Streaming%20Dashboard-4285F4?logo=google-cloud&logoColor=white)](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)

## Submission Details
*   **Track:** Agents for Business 🏢
*   **Demo Video:** [Insert YouTube / Loom Presentation Video Link Here]
*   **Public Codebase:** [https://github.com/debpks/nexusaudit-gauntlet](https://github.com/debpks/nexusaudit-gauntlet)
*   **Live Cloud Run Web Dashboard:** [https://nexusaudit-gauntlet-257473292027.us-central1.run.app](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)
*   **Kaggle Interactive Notebook:** [nexusaudit_gauntlet_kaggle_submission.ipynb](nexusaudit_gauntlet_kaggle_submission.ipynb)

---

## 🎯 1. The Pitch: Problem, Solution & Business Value

### 🚨 The Problem
As enterprises rush to deploy Large Language Models (LLMs) and autonomous agents in customer-facing roles, they expose themselves to unprecedented legal, regulatory, and cybersecurity risks:
1. **Hidden Prompt Injection & Bypasses:** Chatbots frequently suffer from indirect prompt injection (OWASP LLM-01) and system prompt leakage, allowing attackers to override pricing rules, extract PII, or force unauthorized actions.
2. **Crushing Regulatory Fines (EU AI Act & FTC):** The EU AI Act imposes fines up to **€35 Million or 7% of global annual turnover** for deploying non-compliant or deceptive high-risk AI systems (Annex III).
3. **The Static Auditing Bottleneck:** Standard security tools and static code scanners cannot evaluate non-deterministic LLM behavior. Manually red-teaming AI chatbots requires thousands of creative adversarial prompts, which is too slow and expensive for modern CI/CD pipelines.

### 💡 The Solution: NexusAudit-Gauntlet
**NexusAudit-Gauntlet** solves this real-world bottleneck. It is an autonomous DevSecOps red-teaming platform powered by a **4-Agent Google ADK Adversarial Loop** and **FastMCP Server** configured via a centralized `model_config.json`. Instead of static checks, our agents actively engage in multi-turn adversarial combat against target systems:
*   **🤖 Policy Parser Agent (`gemini-2.5-flash` | Temp: 0.0):** Deconstructs regulatory knowledge bases (`commerce_policy_kb.json`) and evaluates the system's compliance claims.
*   **🕵️ Threat Modeler Agent (`gemini-2.5-pro` | Temp: 0.4):** Autonomously executes external tool calls (`search_past_vulnerabilities`) to query historical CVEs and OWASP exploits, formulating targeted attack hypotheses.
*   **⚔️ Red-Team Simulator Agent (`gemini-2.5-pro` | Temp: 0.3):** Generates sophisticated, multi-turn adversarial scenarios (Base64 obfuscation, context priming, roleplay) to dynamically attack the target bot.
*   **⚖️ Evaluator Agent & HITL Guardrail (`gemini-2.5-pro` | Temp: 0.0):** Judges the target's defense, generates legal/technical evidence, and triggers a **Human-in-the-Loop (HITL)** safety pause before generating remediation reports.
*   **🎯 Target AI System / Chatbot (`gemini-2.5-flash-lite` | Temp: 1.0):** The simulated e-commerce chatbot under adversarial audit, configurable for vulnerable or remediated states across 12 statutory clauses.

---

## 📊 2. Business Impact & KPI Risk Mapping

By translating technical AI safety vulnerabilities into tangible executive risk metrics, NexusAudit-Gauntlet demonstrates immediate return on investment (ROI):

| Technical Vulnerability (OWASP / AI Act) | Attack Vector & Technical Failure | Tangible Business & Revenue Risk | Quantified Impact & KPI Penalty |
| :--- | :--- | :--- | :--- |
| **OWASP LLM-01: Indirect Prompt Injection** | Attackers embed hidden instructions in product reviews or user profiles, tricking the chatbot into offering unauthorized 99% discounts or issuing fake refunds. | **Direct Financial Loss & Margin Erosion:** Immediate revenue loss from unauthorized promotional discounts and fraudulent transaction approvals. | **Up to 15-20% loss** in promotional gross margins during active exploit windows. |
| **EU AI Act Annex III Violation (Unlabeled Profiling)** | E-commerce bot secretly scores users based on browsing latency or postal code without explicit transparency disclosure (`COMM_GDPR_02`). | **Regulatory Fines & Legal Sanctions:** Severe regulatory penalties from EU data protection authorities and FTC enforcement actions against deceptive AI practices. | **Fines up to €35M** or **7% of global turnover**, plus mandatory system shutdowns. |
| **OWASP LLM-06: Sensitive Information Disclosure** | Chatbot fails to sanitize multi-turn conversation memory, leaking personal data (PII) or system prompt architecture to social engineering attacks. | **Brand Damage & Customer Churn:** Catastrophic loss of consumer trust, class-action lawsuits, and enterprise contract terminations. | **30%+ increase** in customer churn and permanent brand reputation damage. |
| **OWASP LLM-09: Overreliance & Hallucination** | Bot makes definitive legal or medical claims without human oversight, leading users to take harmful or incorrect actions based on fabricated facts. | **Liability & Support Escalations:** Massive surge in customer support ticket volume and legal liability for erroneous AI guidance. | **4x increase** in tier-3 human support escalations and legal defense costs. |

---

## 🏗️ 3. Architectural Excellence & System Flow

NexusAudit-Gauntlet utilizes a **Dual-Architecture Design**, providing both a sleek, real-time streaming web UI for interactive pair-programming and a headless Google ADK `SequentialAgent` router for automated CI/CD pipelines.

### The 4-Agent DevSecOps Red-Teaming Loop (ASCII Architecture Flowchart)

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 NEXUSAUDIT 4-AGENT RED-TEAMING LOOP                                    │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │ [System Specs & Regulatory KB]
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1️⃣ POLICY PARSER AGENT (gemini-2.5-flash | Temp: 0.0)                                                  │
│    • Deconstructs target system instructions against regulatory statutes (EU AI Act, FTC, GDPR, OWASP) │
│    • Outputs type-safe ClaimSchema isolating exact legal commitments                                   │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │ [Compliance Claim]
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 2️⃣ THREAT MODELER AGENT (gemini-2.5-pro | Temp: 0.4)                                                   │
│    • Autonomously invokes external tool: search_past_vulnerabilities(policy_id)                        │
│    • Queries FastMCP server (commerce_policy_kb.json) for historical CVEs & exploit vectors           │
│    • Formulates adversarial attack hypothesis (ThreatHypothesisSchema)                                 │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │ [Threat Hypothesis]
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 3️⃣ RED-TEAM SIMULATOR AGENT (gemini-2.5-pro | Temp: 0.3)                                               │
│    • Translates hypothesis into multi-turn attack payload (Base64 encoding, Stored XSS, roleplay)       │
│    • Dynamically escalates attack complexity to test defense boundaries                                │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │ [Adversarial Attack Payload]
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🎯 TARGET AI SYSTEM / CHATBOT (gemini-2.5-flash-lite | Temp: 1.0)                                      │
│    • Simulated corporate chatbot (NovaMart ShopBot, Electronics Assistant, or Care Bot)                │
│    • Configurable for vulnerable or remediated states across 12 statutory benchmarks                   │
└───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                    │ [Chatbot Defense Output & Conversation Trace]
                                                    ▼
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ 4️⃣ EVALUATOR JUDGE AGENT (gemini-2.5-pro | Temp: 0.0)                                                  │
│    • Impartial DevSecOps judge cross-referencing chatbot response against statutory legal text         │
│    • Renders formal verdict: COMPLIANT, NON_COMPLIANT, or ESCALATE                                     │
└─────────────────────────┬─────────────────────────────────────────────────┬────────────────────────────┘
                          │ [Verdict: COMPLIANT]                            │ [Verdict: NON_COMPLIANT]
                          ▼                                                 ▼
┌───────────────────────────────────────────────────┐     ┌──────────────────────────────────────────────┐
│ ✅ AUDIT PASSED                                   │     │ 🛑 HUMAN-IN-THE-LOOP (HITL) GUARDRAIL        │
│ • Issue Cryptographic Proof Certificate           │     │ • Execution frozen via ADKHumanApprovalNode   │
│ • Allow CI/CD Pipeline to Proceed                 │     │ • Awaiting DevSecOps Authorization           │
└───────────────────────────────────────────────────┘     └───────────────────────┬──────────────────────┘
                                                                                  │ [DevSecOps Approved]
                                                                                  ▼
                                                          ┌──────────────────────────────────────────────┐
                                                          │ 🛠️ AUTO-REMEDIATION SYNTHESIZER              │
                                                          │ • Generate XML Patch Delimiters              │
                                                          │ • Output ready-to-merge developer patch      │
                                                          └──────────────────────────────────────────────┘
```


### Dual-Architecture: UI Streaming vs. Headless ADK Execution

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           NEXUSAUDIT DUAL-ARCHITECTURE                            │
└─────────────────────────────────────┬─────────────────────────────────────────────┘
                                      │
              ┌───────────────────────┴───────────────────────┐
              ▼                                               ▼
┌───────────────────────────┐                   ┌───────────────────────────┐
│  INTERACTIVE WEB DASHBOARD │                   │   HEADLESS ADK ROUTER     │
│   (dashboard/app.py)      │                   │ (adk_hybrid_router.py)    │
├───────────────────────────┤                   ├───────────────────────────┤
│ • Server-Sent Events (SSE)│                   │ • Native Google ADK       │
│ • Real-time UX Streaming  │                   │ • SequentialAgent Pipeline│
│ • Live Cyberpunk Trace UI │                   │ • Automated CI/CD Grading │
└─────────────┬─────────────┘                   └─────────────┬─────────────┘
              │                                               │
              └───────────────────────┬───────────────────────┘
                                      ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                     CORE DEVSECOPS RED-TEAMING ENGINE                             │
│  [Policy Parser] ──► [Threat Modeler + Tools] ──► [Red-Team Simulator] ──► [HITL] │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏆 4. Course Concepts & Kaggle Rubric Mapping

NexusAudit-Gauntlet strictly demonstrates every required concept from the Google 5-Day AI Agents Intensive curriculum:

| Course Requirement | Implementation File / Module | Details & Verification Proof |
| :--- | :--- | :--- |
| **Google ADK & Multi-Agent Pipeline** | [agents/adk_hybrid_router.py](agents/adk_hybrid_router.py) | Wraps all 4 DevSecOps agents into native `BaseAgent` subclasses and connects them using a true `SequentialAgent` workflow pipeline. Includes seamless fallback for local environments. |
| **Model Context Protocol (FastMCP)** | [agents/mcp_server.py](agents/mcp_server.py) | Implements an official FastMCP server exposing `@mcp.resource("commerce_policy_kb.json")` and an interactive `@mcp.tool("audit_system")` for external IDE or agent invocation. |
| **Agent Tool Calling (Function Calling)** | [agents/threat_modeler.py](agents/threat_modeler.py) | Demonstrates autonomous tool execution. The `ThreatModelerAgent` queries `search_past_vulnerabilities(policy_id)` to check historical OWASP/FTC exploits before generating attack hypotheses. |
| **Human-in-the-Loop (HITL) Guardrail** | [agents/adk_hybrid_router.py](agents/adk_hybrid_router.py) | Implements `ADKHumanApprovalNode`. Halts the autonomous loop when a severity-high violation is detected, requiring human authorization (or `AUTO_APPROVE_HITL=true` override) before remediation. |
| **Antigravity IDE & Customizations** | [.gemini/config/](.gemini/config/) | Built using pair-programming prompts, interactive CLI debugging sessions, and custom system rules inside the Google Antigravity IDE environment. |
| **Structured JSON Schemas (Pydantic)** | [schemas/](schemas/) | Strictly enforces type-safe LLM outputs using Pydantic models (`ClaimSchema`, `ThreatHypothesisSchema`, `RedTeamScenarioSchema`, `EvaluationSchema`) with Gemini structured generation. |

---

## 🔬 5. Advanced Technical Implementation & 12/12 Benchmark Pass Rate

### Adversarial Complexity Escalation & Stored Injections
The `RedTeamSimulatorAgent` features dynamic complexity escalation. If the target chatbot defends against a basic attack, the simulator automatically ramps up its sophistication. Tactics include:
*   **Base64 Payload Obfuscation:** Encoding malicious instructions to bypass basic keyword filters.
*   **Stored Indirect Prompt Injection (OWASP LLM-01):** Embedding payloads inside simulated database records (e.g., product reviews) to exploit the "semantic gap" where LLMs confuse untrusted data with system instructions.
*   **Multi-Turn Roleplay Priming:** Establishing a "developer" or "VIP user" persona over multiple chat turns to socially engineer the bot into leaking PII (GDPR Article 5 violations).

### Verified 100% Benchmark Suite & Ad-Hoc System Auditing
We evaluated NexusAudit against the **NovaMart Corporation** benchmark profile across 12 distinct statutory clauses (EU AI Act, GDPR, FTC Section 5, OWASP Top 10, NIST AI RMF, and PCI DSS). Our platform achieved a **100% verified classification accuracy (12/12 pass rate)**, successfully distinguishing between vulnerable and remediated chatbot architectures.

Furthermore, our live dashboard features an **Ad-Hoc System Audit** mode, allowing engineers to select any of our 3 predefined Target Systems (**NovaMart ShopBot**, **Electronics Assistant**, or **Care Bot**) and audit them on the fly against any regulatory standard.

---

## 🚀 6. Running the System (Turnkey Deployment)

### 1. ⚡ Live Cloud Run Dashboard (Zero Setup Required)
Our cyberpunk streaming UI is live and publicly accessible on Google Cloud Run:
👉 **[Launch Live Cloud Run Dashboard](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)** | **[View Architecture & Rubric](https://nexusaudit-gauntlet-257473292027.us-central1.run.app/about)**

### 2. 📓 Kaggle Static & Interactive Notebook Execution (For Course Judges)
We provide a complete, beautifully formatted Jupyter Notebook ready for Kaggle import: [nexusaudit_gauntlet_kaggle_submission.ipynb](nexusaudit_gauntlet_kaggle_submission.ipynb). Simply upload this notebook to Kaggle, configure your `GEMINI_API_KEY` under Kaggle User Secrets, and run all cells!

Alternatively, you can copy & paste our zero-configuration turnkey cell script [kaggle_submission_cell.py](kaggle_submission_cell.py) into Cell 1 of any blank notebook or run it locally:
```bash
python kaggle_submission_cell.py
```

### 3. Run the Headless ADK Pipeline (Kaggle / CI-CD Mode)
Execute the native Google ADK `SequentialAgent` workflow directly from the command line:
```bash
python -m agents.adk_hybrid_router
```

### 4. Launch the Interactive Cyberpunk Dashboard (Local UX Mode)
Experience the live Server-Sent Events (SSE) streaming dashboard with real-time terminal trace locally:
```bash
python dashboard/app.py
```
Open your browser to `http://localhost:5000` to interact with the Agentic Gauntlet and view the project **About Page** at `http://localhost:5000/about`.

### 5. Run the FastMCP Server
Start the standalone Model Context Protocol server:
```bash
python agents/mcp_server.py
```
