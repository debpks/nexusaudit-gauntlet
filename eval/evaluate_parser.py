import json
import os
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Adjust import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.policy_parser import PolicyParserAgent

def normalize_status(status_str: str) -> str:
    return status_str.lower().replace("-", "_").strip()

def main():
    console = Console()
    
    # Inject ADC credentials for Vertex AI if needed
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists("/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"

    # Paths
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kb_path = os.path.join(project_root, "knowledge_base", "commerce_policy_kb.json")
    ground_truth_path = os.path.join(project_root, "eval", "ground_truth.json")
    
    console.print("[bold cyan]Initializing Aligned E-Commerce Policy Parser Evaluation Loop...[/bold cyan]")
    
    try:
        agent = PolicyParserAgent(kb_path=kb_path)
    except Exception as e:
        console.print(f"[bold red]Failed to initialize PolicyParserAgent: {e}[/bold red]")
        sys.exit(1)
        
    if not os.path.exists(ground_truth_path):
        console.print(f"[bold red]Ground truth file not found at: {ground_truth_path}[/bold red]")
        sys.exit(1)
        
    with open(ground_truth_path, 'r', encoding='utf-8') as f:
        test_systems = json.load(f)
        
    table = Table(title="Aligned EU AI Act Policy Parser - Evaluation Results")
    table.add_column("System Name", style="white", no_wrap=True)
    table.add_column("Expected Status", style="bold yellow")
    table.add_column("Predicted Status", style="bold green")
    table.add_column("Confidence", style="magenta")
    table.add_column("Category Match", style="cyan")
    table.add_column("Result", style="bold")
    
    success_count = 0
    failures = []
    
    for test in test_systems:
        sys_id = test["id"]
        name = test["name"]
        desc = test["description"]
        expected = test["expected"]
        
        console.print(f"\n[bold yellow]Evaluating system:[/bold yellow] [bold white]{name}[/bold white] ({sys_id})")
        console.print(f"[dim]Description: {desc}[/dim]")
        
        try:
            prediction = agent.parse_system(system_name=name, system_description=desc)
            
            console.print(f"[dim green]Agent JSON Response:[/dim green] {prediction.model_dump_json(indent=2)}")
            
            expected_status = normalize_status(expected["claimed_status"])
            predicted_status = normalize_status(prediction.claimed_status)
            
            is_match = expected_status == predicted_status
            result_str = "[green]PASS[/green]" if is_match else "[red]FAIL[/red]"
            
            category_display = prediction.annex_iii_category if prediction.annex_iii_category else "None"
            
            table.add_row(
                name,
                expected_status.upper(),
                predicted_status.upper(),
                f"{prediction.confidence:.2f}",
                category_display,
                result_str
            )
            
            if is_match:
                success_count += 1
            else:
                failures.append({
                    "id": sys_id,
                    "name": name,
                    "expected": expected_status,
                    "predicted": predicted_status,
                    "exemption_basis": prediction.exemption_basis
                })
                
        except Exception as e:
            console.print(f"[bold red]Error parsing system {name}: {e}[/bold red]")
            table.add_row(
                name,
                expected["claimed_status"].upper(),
                "ERROR",
                "0.00",
                "N/A",
                "[bold red]ERROR[/bold red]"
            )
            failures.append({
                "id": sys_id,
                "name": name,
                "error": str(e)
            })

    console.print("\n")
    console.print(table)
    console.print("\n")
    
    total = len(test_systems)
    console.print(f"[bold]Total Evaluated:[/bold] {total}")
    console.print(f"[bold green]Passed:[/bold green] {success_count} / {total}")
    if failures:
        console.print(f"[bold red]Failed:[/bold red] {len(failures)} / {total}")
        for fail in failures:
            if "error" in fail:
                console.print(f"[red]- {fail['name']} failed with error: {fail['error']}[/red]")
            else:
                console.print(f"[red]- {fail['name']}: Expected {fail['expected']}, got {fail['predicted']}[/red]")
                console.print(f"  [dim]Exemption basis provided: {fail['exemption_basis']}[/dim]")
        sys.exit(1)
    else:
        console.print("[bold green]All evaluations matched expected ground truth status successfully![/bold green]")
        sys.exit(0)

if __name__ == "__main__":
    main()
