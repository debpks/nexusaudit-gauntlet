import json
import os
import sys
from typing import Dict, Any

class ReportGenerator:
    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_compliance_report(self, audit_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Pure deterministic report generator. Zero LLM calls.
        """
        system_name = audit_summary.get("system_name", "Unknown System")
        claimed_status = audit_summary.get("policy_parser_claim", {}).get("claimed_status", "unknown")
        annex_iii_category = audit_summary.get("policy_parser_claim", {}).get("annex_iii_category", "None")
        final_eval = audit_summary.get("final_evaluation", {})
        
        clause_status = final_eval.get("clause_status", "HOLDS")
        severity = final_eval.get("severity", "low")
        evidence = final_eval.get("evidence", "")
        remediation = final_eval.get("remediation", "")
        
        # Calculate Compliance Index
        # Severity weights: high = 3, medium = 2, low = 1
        severity_weights = {
            "high": 3,
            "medium": 2,
            "low": 1
        }
        
        weight = severity_weights.get(severity.lower(), 1)
        
        # Calculate score (100 is fully compliant, deduct based on violation severity)
        if clause_status == "NON_COMPLIANT":
            compliance_index = max(0, 100 - (weight * 25))
        else:
            compliance_index = 100.0
            
        # Scorecard
        scorecard = {
            "clause": annex_iii_category if annex_iii_category else "General EU AI Act Scope",
            "claimed_status": claimed_status,
            "audit_verdict": clause_status,
            "severity": severity,
            "weight": weight
        }
        
        # Actionable Remediation Roadmap
        remediation_roadmap = []
        if clause_status == "NON_COMPLIANT":
            remediation_roadmap.append({
                "clause": annex_iii_category if annex_iii_category else "General EU AI Act Scope",
                "severity": severity,
                "remediation": remediation if remediation else "Remediation details missing."
            })
            
        report_data = {
            "system_name": system_name,
            "compliance_index": compliance_index,
            "scorecard": scorecard,
            "remediation_roadmap": remediation_roadmap,
            "evidence": evidence
        }
        
        # Generate Markdown output
        md_report = self._to_markdown(report_data)
        
        # Save files
        safe_name = system_name.lower().replace(" ", "_").replace("/", "_")
        
        # JSON output
        json_path = os.path.join(self.reports_dir, f"{safe_name}_final_report.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
            
        # Markdown output
        md_path = os.path.join(self.reports_dir, f"{safe_name}_final_report.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_report)
            
        print(f"Generated final reports at:\n - {json_path}\n - {md_path}")
        
        return report_data

    def _to_markdown(self, data: Dict[str, Any]) -> str:
        status_color = "🔴" if data["compliance_index"] < 100 else "🟢"
        
        md = f"""# EU AI Act Audit Scorecard: {data['system_name']}

## 📊 Compliance Index: {status_color} {data['compliance_index']}%

### 📋 Scorecard Table
| Clause / Category | Claimed Status | Audit Verdict | Severity |
|---|---|---|---|
| {data['scorecard']['clause']} | {data['scorecard']['claimed_status'].upper()} | `{data['scorecard']['audit_verdict']}` | `{data['scorecard']['severity'].upper()}` |

---

## ⚖️ Audit Evidence
{data['evidence']}

---

## 🛠️ Actionable Remediation Roadmap
"""
        if not data["remediation_roadmap"]:
            md += "✅ No non-compliant clauses identified. The system's compliance claims hold."
        else:
            for item in data["remediation_roadmap"]:
                md += f"""### 📍 Clause: {item['clause']} (Severity: `{item['severity'].upper()}`)
* **Remediation Plan:** {item['remediation']}
"""
        return md
