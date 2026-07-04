import json
import os
import sys

# Adjust import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.report_generator import ReportGenerator

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    reports_dir = os.path.join(project_root, "reports")
    verdict_path = os.path.join(reports_dir, "docuextract_resume_parser_verdict.json")
    
    if not os.path.exists(verdict_path):
        print(f"Error: Verdict file not found at {verdict_path}")
        sys.exit(1)
        
    with open(verdict_path, "r", encoding="utf-8") as f:
        audit_summary = json.load(f)
        
    generator = ReportGenerator(reports_dir=reports_dir)
    
    # Run 1
    print("Running ReportGenerator - Run 1...")
    report1 = generator.generate_compliance_report(audit_summary)
    
    # Run 2
    print("Running ReportGenerator - Run 2...")
    report2 = generator.generate_compliance_report(audit_summary)
    
    # Determinism check
    safe_name = audit_summary["system_name"].lower().replace(" ", "_").replace("/", "_")
    json_path = os.path.join(reports_dir, f"{safe_name}_final_report.json")
    md_path = os.path.join(reports_dir, f"{safe_name}_final_report.md")
    
    with open(json_path, "rb") as f:
        bytes1_json = f.read()
    with open(md_path, "rb") as f:
        bytes1_md = f.read()
        
    # Re-run generator to overwrite and check
    generator.generate_compliance_report(audit_summary)
    
    with open(json_path, "rb") as f:
        bytes2_json = f.read()
    with open(md_path, "rb") as f:
        bytes2_md = f.read()
        
    is_json_identical = bytes1_json == bytes2_json
    is_md_identical = bytes1_md == bytes2_md
    
    print("\n=======================================================")
    print("Determinism Verification Results:")
    print("=======================================================")
    print(f"JSON outputs are byte-identical: {is_json_identical}")
    print(f"Markdown outputs are byte-identical: {is_md_identical}")
    
    if is_json_identical and is_md_identical:
        print("[SUCCESS] Report Generator is fully deterministic (zero LLM calls).")
        sys.exit(0)
    else:
        print("[FAIL] Report Generator is non-deterministic.")
        sys.exit(1)

if __name__ == "__main__":
    main()
