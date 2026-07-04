import json
import os
import sys
from rich.console import Console

# Adjust import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.policy_parser import PolicyParserAgent
from agents.threat_modeler import ThreatModelerAgent
from agents.red_team_simulator import RedTeamSimulatorAgent
from agents.evaluator import EvaluatorAgent

def main():
    console = Console()
    
    # Inject ADC credentials for Vertex AI if needed
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists("/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kb_path = os.path.join(project_root, "knowledge_base", "commerce_policy_kb.json")
    ground_truth_path = os.path.join(project_root, "eval", "ground_truth.json")

    console.print("[bold cyan]Initializing Integrated Agentic Loop Test...[/bold cyan]")
    
    try:
        parser = PolicyParserAgent(kb_path=kb_path)
        modeler = ThreatModelerAgent(kb_path=kb_path)
        simulator = RedTeamSimulatorAgent(kb_path=kb_path)
        evaluator = EvaluatorAgent(kb_path=kb_path)
    except Exception as e:
        console.print(f"[bold red]Initialization failed: {e}[/bold red]")
        sys.exit(1)
        
    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        test_systems = json.load(f)
        
    # We will run this on NovaMart ShopBot (sys_01)
    system = next(s for s in test_systems if s["id"] == "sys_01")
    name = system["name"]
    desc = system["description"]
    
    console.print(f"\n[bold white]Target System: {name}[/bold white]")
    console.print(f"[dim]Description: {desc}[/dim]")
    
    try:
        # Step 1: Policy Parser
        console.print("\n[bold yellow]Step 1: Running Policy Parser...[/bold yellow]")
        claim = parser.parse_system(system_name=name, system_description=desc)
        console.print(f"Claimed Status: {claim.claimed_status}")
        console.print(f"Exemption Basis: {claim.exemption_basis}")
        
        # Step 2: Threat Modeler
        console.print("\n[bold yellow]Step 2: Running Threat Modeler...[/bold yellow]")
        hypothesis = modeler.model_threat(system_name=name, system_description=desc, claim=claim)
        console.print(f"Hypothesis: {hypothesis.hypothesis}")
        
        # Step 3: Red-Team Simulator
        console.print("\n[bold yellow]Step 3: Running Red-Team Simulator...[/bold yellow]")
        scenario = simulator.generate_scenario(system_name=name, system_description=desc, hypothesis=hypothesis)
        console.print(f"Scenario Description:\n{scenario.scenario_description}")
        console.print(f"Expected Violation:\n{scenario.expected_violation}")
        
        # Step 4: Evaluator
        console.print("\n[bold yellow]Step 4: Running Evaluator...[/bold yellow]")
        evaluation = evaluator.evaluate(
            system_name=name,
            system_description=desc,
            claim=claim,
            hypothesis=hypothesis,
            scenario=scenario,
            round_num=1
        )
        
        console.print(f"\n[bold green]Final Verdict:[/bold green]")
        console.print(f"  [bold]Clause Status:[/bold] {evaluation.clause_status}")
        console.print(f"  [bold]Severity:[/bold] {evaluation.severity}")
        console.print(f"  [bold]Evidence:[/bold] {evaluation.evidence}")
        console.print(f"  [bold]Remediation:[/bold] {evaluation.remediation}")
        console.print(f"  [bold]Loop Decision:[/bold] {evaluation.loop_decision}")
        
    except Exception as e:
        console.print(f"[bold red]Failed to process system: {e}[/bold red]")

if __name__ == "__main__":
    main()
