import os
import sys
import argparse

# Support running directly or as package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.loop_agent import LoopAgent
from agents.report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="NexusAudit-Gauntlet Dynamic CLI Auditor")
    parser.add_argument("--name", type=str, required=True, help="Name of the AI system to audit")
    parser.add_argument("--desc", type=str, required=True, help="Detailed system description")
    parser.add_argument("--kb", type=str, default="knowledge_base/commerce_policy_kb.json", help="Path to regulatory rules KB JSON")
    parser.add_argument("--remediated", action="store_true", help="Enable target bot remediation shield")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.kb):
        print(f"Error: Knowledge base file not found at {args.kb}")
        sys.exit(1)
        
    loop_agent = LoopAgent(kb_path=args.kb)
    report_gen = ReportGenerator()
    
    print(f"\n==================================================")
    print(f"RUNNING DYNAMIC COMPLIANCE AUDIT")
    print(f"Target System Name: {args.name}")
    print(f"Rules Registry: {args.kb}")
    print(f"==================================================")
    
    audit_summary = loop_agent.run_system_audit(
        system_name=args.name,
        system_description=args.desc,
        remediated=args.remediated
    )
    
    report = report_gen.generate_compliance_report(audit_summary)
    
    print(f"\n==================================================")
    print(f"AUDIT SCORECARD SUMMARY")
    print(f"==================================================")
    print(f"Compliance Index Score: {report['compliance_index']}%")
    print(f"Audit Verdict: {report['scorecard']['audit_verdict']}")
    print(f"Evidence Summary: {report['evidence']}")
    if report.get('remediation_roadmap') and len(report['remediation_roadmap']) > 0:
        print(f"Remediation Patch Proposed: {report['remediation_roadmap'][0]['remediation']}")
    print(f"==================================================\n")

if __name__ == "__main__":
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and os.path.exists("/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/vscode/.config/gcloud/legacy_credentials/purnideb@gmail.com/adc.json"
    main()
