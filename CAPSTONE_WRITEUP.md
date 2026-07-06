# 🛡️ NexusAudit-Gauntlet: Autonomous DevSecOps & AI Safety Compliance Auditor

[![GitHub Repository](https://img.shields.io/badge/GitHub-debpks%2Fnexusaudit--gauntlet-181717?logo=github)](https://github.com/debpks/nexusaudit-gauntlet)
[![Google 5-Day AI Intensive](https://img.shields.io/badge/Kaggle-5--Day%20AI%20Agents%20Intensive-20BEFF?logo=kaggle)](https://www.kaggle.com/code/singhaleo/kaggle-submission)
[![Live Cloud Run Demo](https://img.shields.io/badge/Google%20Cloud%20Run-Live%20Streaming%20Dashboard-4285F4?logo=google-cloud&logoColor=white)](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)
[![YouTube Demo Video](https://img.shields.io/badge/YouTube-Watch%20Live%20Demo-FF0000?logo=youtube&logoColor=white)](https://youtu.be/cCeDdKY-rog)

![NexusAudit-Gauntlet Hero Banner](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/nexusaudit_thumbnail_card.jpg)

## Submission Details
*   **Track:** Agents for Business 🏢
*   **Demo Video:** [https://youtu.be/cCeDdKY-rog](https://youtu.be/cCeDdKY-rog) 📺
*   **Public Codebase:** [https://github.com/debpks/nexusaudit-gauntlet](https://github.com/debpks/nexusaudit-gauntlet)
*   **Live Cloud Run Web Dashboard:** [https://nexusaudit-gauntlet-257473292027.us-central1.run.app](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)
*   **Kaggle Interactive Notebook:** [https://www.kaggle.com/code/singhaleo/kaggle-submission](https://www.kaggle.com/code/singhaleo/kaggle-submission)

---

## 🎯 1. The Pitch: Problem, Solution & Business Value

### 🚨 The Problem
As enterprises rush to deploy Large Language Models (LLMs) and autonomous agents in customer-facing roles, they expose themselves to unprecedented legal, regulatory, and cybersecurity risks:
1. **Hidden Prompt Injection & Bypasses:** Chatbots frequently suffer from indirect prompt injection (OWASP LLM-01) and system prompt leakage, allowing attackers to override pricing rules, extract PII, or force unauthorized actions.
2. **Crushing Regulatory Fines (EU AI Act & FTC):** The EU AI Act imposes fines up to **€35 Million or 7% of global annual turnover** for deploying non-compliant or deceptive high-risk AI systems (Annex III).
3. **The Static Auditing Bottleneck:** Standard security tools and static code scanners cannot evaluate non-deterministic LLM behavior. Manually red-teaming AI chatbots requires thousands of creative adversarial prompts, which is too slow and expensive for modern CI/CD pipelines.

![Story 1: Enterprise AI Vulnerability & Regulatory Fines](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/story_1_ai_risk.jpg)

### 💡 The Solution: NexusAudit-Gauntlet
**NexusAudit-Gauntlet** solves this real-world bottleneck. It is an autonomous DevSecOps red-teaming platform powered by a **4-Agent Google ADK Adversarial Loop** and **FastMCP Server** configured via a centralized `model_config.json`. Instead of static checks, our agents actively engage in multi-turn adversarial combat against target systems:
*   **🤖 Policy Parser Agent (`gemini-2.5-flash` | Temp: 0.0):** Deconstructs regulatory knowledge bases (`commerce_policy_kb.json`) and evaluates the system's compliance claims.
*   **🕵️ Threat Modeler Agent (`gemini-2.5-pro` | Temp: 0.4):** Autonomously executes external tool calls (`search_past_vulnerabilities`) to query historical CVEs and OWASP exploits, formulating targeted attack hypotheses.
*   **⚔️ Red-Team Simulator Agent (`gemini-2.5-pro` | Temp: 0.3):** Generates sophisticated, multi-turn adversarial scenarios (Base64 obfuscation, context priming, roleplay) to dynamically attack the target bot.
*   **⚖️ Evaluator Agent & HITL Guardrail (`gemini-2.5-pro` | Temp: 0.0):** Judges the target's defense, generates legal/technical evidence, and triggers a **Human-in-the-Loop (HITL)** safety pause before generating remediation reports.
*   **🎯 Target AI System / Chatbot (`gemini-2.5-flash-lite` | Temp: 1.0):** The simulated e-commerce chatbot under adversarial audit, configurable for vulnerable or remediated states across 12 statutory clauses.

![Story 2: The 4-Agent DevSecOps Red-Teaming Gauntlet](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/story_2_four_agent_gauntlet.jpg)

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
+----------------------------------------------------------+
|            NEXUSAUDIT 4-AGENT RED-TEAMING LOOP           |
+----------------------------------------------------------+
                             |
                             v
+----------------------------------------------------------+
| 1. POLICY PARSER AGENT (gemini-2.5-flash | Temp: 0.0)    |
|  * Deconstructs bot instructions vs statutory rules      |
|  * Outputs ClaimSchema isolating exact legal commitments |
+----------------------------------------------------------+
                             | [Compliance Claim]
                             v
+----------------------------------------------------------+
| 2. THREAT MODELER AGENT (gemini-2.5-pro | Temp: 0.4)     |
|  * Tool: search_past_vulnerabilities(policy_id)          |
|  * Queries FastMCP KB for historical CVEs & exploits     |
|  * Formulates attack hypothesis (ThreatHypothesisSchema) |
+----------------------------------------------------------+
                             | [Threat Hypothesis]
                             v
+----------------------------------------------------------+
| 3. RED-TEAM SIMULATOR (gemini-2.5-pro | Temp: 0.3)       |
|  * Builds multi-turn attack (Base64, Stored XSS, roleplay)|
|  * Dynamically escalates attack complexity               |
+----------------------------------------------------------+
                             | [Attack Payload]
                             v
+----------------------------------------------------------+
| 4. TARGET AI CHATBOT (gemini-2.5-flash-lite | Temp: 1.0) |
|  * Simulated bot (ShopBot, Electronics, or Care Bot)     |
|  * Tested across 12 statutory benchmarks                 |
+----------------------------------------------------------+
                             | [Bot Defense Output]
                             v
+----------------------------------------------------------+
| 5. EVALUATOR JUDGE AGENT (gemini-2.5-pro | Temp: 0.0)    |
|  * Judges chatbot output against legal standards         |
|  * Verdict: COMPLIANT, NON_COMPLIANT, or ESCALATE        |
+----------------------------------------------------------+
               |                            |
  [COMPLIANT]  |                            | [NON_COMPLIANT]
               v                            v
+---------------------------+  +---------------------------+
| ✅ AUDIT PASSED           |  | 🛑 HITL SAFETY GUARDRAIL  |
| * Issue Proof Certificate |  | * Pipeline frozen by ADK  |
| * Allow CI/CD to Proceed  |  | * Awaiting Authorization  |
+---------------------------+  +---------------------------+
                                            |
                                            v
                               +---------------------------+
                               | 🛠️ XML PATCH SYNTHESIZER  |
                               | * Generates XML Delimiter |
                               | * Outputs developer patch |
                               +---------------------------+
```

![Story 3: Autonomous Threat Modeling & FastMCP Tool Calling](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/story_3_threat_modeling.jpg)

### Dual-Architecture: UI Streaming vs. Headless ADK Execution

```
+--------------------------------------------------------+
|              NEXUSAUDIT DUAL-ARCHITECTURE              |
+---------------------------+----------------------------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
+--------------------------+  +--------------------------+
| INTERACTIVE DASHBOARD    |  | HEADLESS ADK ROUTER      |
| (dashboard/app.py)       |  | (adk_hybrid_router.py)   |
+--------------------------+  +--------------------------+
| * Server-Sent Events     |  | * Native Google ADK      |
| * Real-time UX Streaming |  | * Sequential Pipeline    |
| * Live Cyberpunk Trace   |  | * Automated CI/CD Grading|
+------------+-------------+  +------------+-------------+
             |                             |
             +--------------+--------------+
                            |
                            v
+--------------------------------------------------------+
|           CORE DEVSECOPS RED-TEAMING ENGINE            |
| Parser -> Modeler (+ MCP Tools) -> Simulator -> HITL   |
+--------------------------------------------------------+
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

![Story 4: Human-In-The-Loop Safety Guardrail](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/story_4_hitl_guardrail.jpg)

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

![Story 5: Verified Compliance Certificate & Automated XML Remediation](https://raw.githubusercontent.com/debpks/nexusaudit-gauntlet/main/assets/story_5_compliance_certificate.jpg)

---

## 🚀 6. Running the System (Turnkey Deployment)

### 1. ⚡ Live Cloud Run Dashboard (Zero Setup Required)
Our cyberpunk streaming UI is live and publicly accessible on Google Cloud Run:
👉 **[Launch Live Cloud Run Dashboard](https://nexusaudit-gauntlet-257473292027.us-central1.run.app)** | **[View Architecture & Rubric](https://nexusaudit-gauntlet-257473292027.us-central1.run.app/about)**

### 2. 📓 Kaggle Static & Interactive Notebook Execution (For Course Judges)
We provide our complete, beautifully formatted Jupyter Notebook live on Kaggle: [https://www.kaggle.com/code/singhaleo/kaggle-submission](https://www.kaggle.com/code/singhaleo/kaggle-submission) (and locally via [nexusaudit_gauntlet_kaggle_submission.ipynb](nexusaudit_gauntlet_kaggle_submission.ipynb)). Simply open the live Kaggle link, configure your `GEMINI_API_KEY` under Kaggle User Secrets, and run all cells!

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
