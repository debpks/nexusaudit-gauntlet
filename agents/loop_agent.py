import json
import os
import sys
from typing import Dict, Any, List

# To support running directly or as package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.policy_parser import PolicyParserAgent
from agents.threat_modeler import ThreatModelerAgent
from agents.red_team_simulator import RedTeamSimulatorAgent
from agents.evaluator import EvaluatorAgent
from agents.commerce_bot import CommerceBot

from schemas.claim import ClaimSchema
from schemas.threat import ThreatHypothesisSchema
from schemas.red_team import RedTeamScenarioSchema
from schemas.evaluation import EvaluationSchema

class LoopAgent:
    def __init__(self, kb_path: str, reports_dir: str = "reports"):
        self.kb_path = kb_path
        self.reports_dir = reports_dir
        self.raw_logs_dir = os.path.join(reports_dir, "raw_logs")
        
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.raw_logs_dir, exist_ok=True)
        
        self.parser = PolicyParserAgent(kb_path=kb_path)
        self.modeler = ThreatModelerAgent(kb_path=kb_path)
        self.simulator = RedTeamSimulatorAgent(kb_path=kb_path)
        self.evaluator = EvaluatorAgent(kb_path=kb_path)

    def run_system_audit(self, system_name: str, system_description: str, remediated: bool = False, zip_code: str = None, device_type: str = None) -> Dict[str, Any]:
        print(f"\n=======================================================")
        print(f"Starting Multi-Agent Compliance Audit: {system_name}")
        print(f"=======================================================")
        
        # Check if we are running an active chatbot audit
        is_active_chatbot = "commerce" in self.kb_path.lower() or "shopbot" in system_name.lower() or "retail" in system_name.lower()
        bot = CommerceBot() if is_active_chatbot else None
        if is_active_chatbot:
            print("-> Detected Active E-Commerce Chatbot Audit. Sandbox enabled.")

        # 1. Policy Parser Claim
        print("-> Running Policy Parser...")
        claim = self.parser.parse_system(system_name, system_description)
        print(f"   Status claimed: {claim.claimed_status.upper()}")
        print(f"   Category: {claim.annex_iii_category or 'None'}")
        
        round_num = 1
        max_rounds = 3
        escalation_context = None
        rounds_data = []
        final_verdict = None
        
        # Threat modeling and evaluation loop
        while round_num <= max_rounds:
            print(f"\n======================================================================")
            print(f"-> Threat/Red-Team/Evaluation Loop (Round {round_num} of {max_rounds})")
            print(f"======================================================================")
            
            # A. Threat Modeler
            print("\n[STAGE 1] Running Threat Modeler Agent...")
            print(f"   Input Claim Status: {claim.claimed_status.upper()}")
            print(f"   Input Scope Clause: {claim.annex_iii_category or 'None'}")
            hypothesis = self.modeler.model_threat(
                system_name, system_description, claim, escalation_context
            )
            print(f"   >>> Formulated Hypothesis: \"{hypothesis.hypothesis}\"")
            print(f"   >>> Target Rule ID: {hypothesis.target_clause}")
            print(f"   >>> Test Strategy: {hypothesis.test_strategy}")
            
            # B. Red-Team Simulator
            print("\n[STAGE 2] Running Red-Team Simulator Agent...")
            scenario = self.simulator.generate_scenario(
                system_name, system_description, hypothesis, escalation_context
            )
            print(f"   >>> Generated Adversarial Payload Prompt:\n   ------------------------------------------------------------\n   {scenario.scenario_description}\n   ------------------------------------------------------------")
            print(f"   >>> Expected Violation: {scenario.expected_violation}")
            
            # Active Chatbot Execution
            chatbot_output = None
            if is_active_chatbot and bot:
                print("\n[STAGE 3] Executing Target Chatbot in Sandbox...")
                print(f"   Parameters: remediated={remediated}, zip={zip_code or 'none'}, device={device_type or 'none'}")
                from agents.utils import resolve_default_adc
                resolve_default_adc()
                
                try:
                    chatbot_output = bot.chat(
                        scenario.scenario_description,
                        remediated=remediated,
                        zip_code=zip_code,
                        device_type=device_type,
                        system_name=system_name,
                        system_description=system_description
                    )
                finally:
                    if not original_adc and "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
                        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
                
                print(f"   >>> Chatbot Sandbox Response:\n   ------------------------------------------------------------\n   {chatbot_output}\n   ------------------------------------------------------------")
            
            # C. Evaluator
            print("\n[STAGE 4] Running Evaluator Agent...")
            evaluation = self.evaluator.evaluate(
                system_name, system_description, claim, hypothesis, scenario, round_num, chatbot_output
            )
            
            print(f"   >>> Auditor Verdict: {evaluation.clause_status}")
            print(f"   >>> Severity Rating: {evaluation.severity.upper()}")
            print(f"   >>> Evidence Log: {evaluation.evidence}")
            if evaluation.remediation:
                print(f"   >>> Remediation Patch Proposed:\n   {evaluation.remediation}")
            print(f"   >>> Loop Decision: {evaluation.loop_decision}")
            
            # Log raw inputs/outputs for this round
            round_log = {
                "round": round_num,
                "claim": claim.model_dump(),
                "threat_hypothesis": hypothesis.model_dump(),
                "red_team_scenario": scenario.model_dump(),
                "chatbot_output": chatbot_output,
                "evaluation": evaluation.model_dump()
            }
            rounds_data.append(round_log)
            
            # Save raw log file
            safe_name = system_name.lower().replace(" ", "_").replace("/", "_")
            log_filename = f"{safe_name}_round_{round_num}.json"
            log_filepath = os.path.join(self.raw_logs_dir, log_filename)
            with open(log_filepath, "w", encoding="utf-8") as f:
                json.dump(round_log, f, indent=2)
            
            # Loop control-flow updates
            final_verdict = evaluation
            
            # Check exit conditions
            if evaluation.loop_decision == "ADVANCE" or round_num >= max_rounds:
                break
                
            # Prepare escalation for next round
            escalation_context = (
                f"Round {round_num} Evaluation marked ESCALATE. "
                f"Previous hypothesis: '{hypothesis.hypothesis}'. "
                f"Previous red-team scenario: '{scenario.scenario_description}'. "
                f"Evaluator feedback: '{evaluation.evidence}'."
            )
            round_num += 1
            
        print(f"\nAudit completed in {round_num} rounds.")
        
        # Construct summary result
        audit_summary = {
            "system_name": system_name,
            "description": system_description,
            "policy_parser_claim": claim.model_dump(),
            "rounds_completed": round_num,
            "final_evaluation": final_verdict.model_dump(),
            "detailed_rounds": rounds_data
        }
        
        # Save final report summary JSON
        summary_filename = f"{safe_name}_verdict.json"
        summary_filepath = os.path.join(self.reports_dir, summary_filename)
        with open(summary_filepath, "w", encoding="utf-8") as f:
            json.dump(audit_summary, f, indent=2)
            
        # Also generate a markdown report
        self._generate_markdown_report(audit_summary, safe_name)
        
        return audit_summary

    def _generate_markdown_report(self, audit: Dict[str, Any], safe_name: str):
        md_content = f"""# EU AI Act Compliance Audit Report: {audit['system_name']}

## 📌 Executive Summary
- **Audited System:** {audit['system_name']}
- **Policy Parser Classification:** `{audit['policy_parser_claim']['claimed_status'].upper()}`
- **Annex III Category:** `{audit['policy_parser_claim']['annex_iii_category'] or 'None'}`
- **Final Audit Verdict:** `{audit['final_evaluation']['clause_status']}`
- **Severity Level:** `{audit['final_evaluation']['severity'].upper()}`
- **Rounds of Adversarial Probing:** {audit['rounds_completed']}

---

## ⚖️ Audit Evidence
{audit['final_evaluation']['evidence']}

---

## 🛠️ Actionable Remediation Roadmap
{audit['final_evaluation']['remediation'] or 'No remediation required.'}

---

## 🔄 Adversarial Probing Log (Rounds 1-{audit['rounds_completed']})
"""
        for r in audit['detailed_rounds']:
            md_content += f"""
### 🌀 Round {r['round']}
- **Threat Modeler Hypothesis:** 
  > {r['threat_hypothesis']['hypothesis']}
- **Red-Team Simulator Test Case:**
  > {r['red_team_scenario']['scenario_description']}
- **Expected Compliance Deviation:**
  > {r['red_team_scenario']['expected_violation']}
- **Evaluator Verdict:** `{r['evaluation']['clause_status']}` (Loop Decision: `{r['evaluation']['loop_decision']}`)
"""
            
        report_path = os.path.join(self.reports_dir, f"{safe_name}_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Generated markdown report at: {report_path}")
