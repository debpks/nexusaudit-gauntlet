import os
import sys
import json
import time
from rich.console import Console
from rich.table import Table

# Adjust sys.path to access agents and schemas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.adk_hybrid_router import ADKGauntletWorkflow

def main():
    console = Console()
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    kb_path = os.path.join(project_root, "knowledge_base", "commerce_policy_kb.json")
    ground_truth_path = os.path.join(project_root, "eval", "dropdown_policies_ground_truth.json")
    reports_dir = os.path.join(project_root, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    console.print("[bold cyan]=====================================================================[/bold cyan]")
    console.print("[bold cyan]🛡️ Launching Exhaustive Evaluation for All 12 Dropdown Policies...[/bold cyan]")
    console.print("[bold cyan]=====================================================================[/bold cyan]")

    if not os.path.exists(ground_truth_path):
        console.print(f"[bold red]Ground truth file not found at {ground_truth_path}[/bold red]")
        sys.exit(1)

    with open(ground_truth_path, "r", encoding="utf-8") as f:
        policies = json.load(f)

    try:
        workflow = ADKGauntletWorkflow(kb_path=kb_path, auto_approve_hitl=True)
        console.print("✅ Initialized Native Google ADK Sequential Workflow.")
    except Exception as e:
        console.print(f"[bold red]Failed to initialize workflow: {e}[/bold red]")
        sys.exit(1)

    results = []
    passed_count = 0

    table = Table(title="NexusAudit Dropdown Policies Benchmark Results")
    table.add_column("Policy ID", style="cyan", no_wrap=True)
    table.add_column("Scenario Name", style="white")
    table.add_column("Expected Status", style="yellow")
    table.add_column("Predicted Status", style="magenta")
    table.add_column("Severity", style="blue")
    table.add_column("Match", style="bold")

    for idx, item in enumerate(policies, 1):
        p_id = item["id"]
        p_name = item["name"]
        p_desc = item["description"]
        expected = item["expected"]

        console.print(f"\n[bold yellow]({idx}/{len(policies)}) Evaluating Policy: {p_id} - {p_name}...[/bold yellow]")
        try:
            verdict = workflow.execute_audit(p_name, p_desc)
            pred_status = verdict.clause_status
            pred_sev = verdict.severity
            evidence = verdict.evidence
            remediation = verdict.remediation

            status_match = (pred_status.upper() == expected["clause_status"].upper())
            if status_match:
                passed_count += 1
                match_str = "[green]PASS[/green]"
            else:
                match_str = "[red]FAIL[/red]"

            table.add_row(p_id, p_name[:30], expected["clause_status"], pred_status, pred_sev.upper(), match_str)

            results.append({
                "policy_id": p_id,
                "name": p_name,
                "description": p_desc,
                "expected_status": expected["clause_status"],
                "predicted_status": pred_status,
                "predicted_severity": pred_sev,
                "status_match": status_match,
                "evidence": evidence,
                "remediation": remediation
            })

            console.print(f" -> Result: {match_str} | Status: {pred_status} | Severity: {pred_sev.upper()}")

        except Exception as e:
            console.print(f"[bold red]Error evaluating {p_id}: {e}[/bold red]")
            table.add_row(p_id, p_name[:30], expected["clause_status"], "ERROR", "N/A", "[red]ERROR[/red]")
            results.append({
                "policy_id": p_id,
                "name": p_name,
                "error": str(e),
                "status_match": False
            })

        # Brief pause to avoid API rate spikes
        time.sleep(1)

    console.print("\n")
    console.print(table)
    console.print(f"\n[bold white]Total Policies Evaluated: {len(policies)} | Passed: {passed_count} / {len(policies)}[/bold white]")

    # Save JSON Report
    json_report_path = os.path.join(reports_dir, "dropdown_policies_eval_report.json")
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_evaluated": len(policies),
            "passed": passed_count,
            "pass_rate": f"{(passed_count / len(policies)) * 100:.1f}%",
            "results": results
        }, f, indent=2)

    # Save Markdown Report
    md_report_path = os.path.join(reports_dir, "dropdown_policies_eval_report.md")
    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("# 🛡️ NexusAudit-Gauntlet: Exhaustive Dropdown Policies Evaluation Report\n\n")
        f.write(f"- **Date Generated:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
        f.write(f"- **Total Policies Tested:** {len(policies)}\n")
        f.write(f"- **Benchmark Pass Rate:** **{passed_count} / {len(policies)} ({(passed_count / len(policies)) * 100:.1f}%)**\n\n")
        f.write("## 📊 Executive Summary Table\n\n")
        f.write("| Policy ID | Scenario Name | Expected Status | Predicted Status | Severity | Result |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
        for r in results:
            match_icon = "✅ PASS" if r.get("status_match") else "❌ FAIL"
            f.write(f"| `{r.get('policy_id')}` | {r.get('name')} | `{r.get('expected_status', 'N/A')}` | `{r.get('predicted_status', 'ERROR')}` | {r.get('predicted_severity', 'N/A').upper()} | **{match_icon}** |\n")
        
        f.write("\n## 🔍 Detailed Evidence & Remediation Breakdown\n\n")
        for r in results:
            if "error" in r:
                f.write(f"### ❌ {r.get('policy_id')}: {r.get('name')}\n")
                f.write(f"- **Error:** `{r.get('error')}`\n\n")
            else:
                icon = "✅" if r.get("status_match") else "❌"
                f.write(f"### {icon} `{r.get('policy_id')}` — {r.get('name')}\n")
                f.write(f"- **Predicted Status:** `{r.get('predicted_status')}` (Expected: `{r.get('expected_status')}`)\n")
                f.write(f"- **Risk Severity:** **{r.get('predicted_severity').upper()}**\n")
                f.write(f"- **Evidence:** {r.get('evidence')}\n")
                f.write(f"- **Remediation Advice:** *{r.get('remediation')}*\n\n")

    console.print(f"[bold green]✅ Reports saved to:\n  - {json_report_path}\n  - {md_report_path}[/bold green]")

if __name__ == "__main__":
    main()
