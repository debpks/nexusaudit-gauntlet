import json
import os
import sys
from rich.console import Console
from rich.table import Table

# Adjust import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.policy_parser import PolicyParserAgent
from agents.threat_modeler import ThreatModelerAgent

def main():
    console = Console()
    
    # Inject ADC credentials for Vertex AI if needed
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists("/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kb_path = os.path.join(project_root, "knowledge_base", "commerce_policy_kb.json")
    ground_truth_path = os.path.join(project_root, "eval", "ground_truth.json")

    console.print("[bold cyan]Initializing Threat Modeler Spot-Check...[/bold cyan]")
    
    # Initialize agents
    try:
        parser = PolicyParserAgent(kb_path=kb_path)
        modeler = ThreatModelerAgent(kb_path=kb_path)
    except Exception as e:
        console.print(f"[bold red]Initialization failed: {e}[/bold red]")
        sys.exit(1)
        
    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        test_systems = json.load(f)
        
    # Let's test the 3 NovaMart Agents
    systems_to_test = ["sys_01", "sys_02", "sys_03"]
    
    for sys_id in systems_to_test:
        system = next(s for s in test_systems if s["id"] == sys_id)
        name = system["name"]
        desc = system["description"]
        
        console.print(f"\n[bold yellow]------------------------------------------------------------[/bold yellow]")
        console.print(f"[bold white]System: {name} ({sys_id})[/bold white]")
        console.print(f"[dim]Description: {desc}[/dim]")
        
        try:
            # 1. Parse claim
            claim = parser.parse_system(system_name=name, system_description=desc)
            console.print(f"[green]Policy Parser Claim Status:[/green] {claim.claimed_status.upper()}")
            console.print(f"[dim green]Exemption Basis:[/dim green] {claim.exemption_basis}")
            
            # 2. Generate Threat Hypothesis
            hypothesis = modeler.model_threat(system_name=name, system_description=desc, claim=claim)
            
            console.print(f"\n[bold magenta]Threat Modeler Hypothesis:[/bold magenta]")
            console.print(f"  [bold]Hypothesis:[/bold] {hypothesis.hypothesis}")
            console.print(f"  [bold]Target Clause:[/bold] {hypothesis.target_clause}")
            console.print(f"  [bold]Test Strategy:[/bold] {hypothesis.test_strategy}")
            
        except Exception as e:
            console.print(f"[bold red]Failed to process system {name}: {e}[/bold red]")

if __name__ == "__main__":
    main()
