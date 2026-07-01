import argparse
import sys
import os

from agents.policy_parser import PolicyParserAgent

def main():
    parser = argparse.ArgumentParser(description="NexusAudit-Gauntlet CLI")
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")
    
    # Parse subcommand
    parse_parser = subparsers.add_parser("parse", help="Parse and classify an AI system")
    parse_parser.add_argument("--name", required=True, help="Name of the AI system")
    parse_parser.add_argument("--description", required=True, help="Description of the AI system")
    parse_parser.add_argument("--kb", default="knowledge_base/eu_ai_act_kb.json", help="Path to knowledge base JSON")
    
    # Eval subcommand
    eval_parser = subparsers.add_parser("evaluate", help="Run compliance evaluation suite")
    eval_parser.add_argument("--kb", default="knowledge_base/eu_ai_act_kb.json", help="Path to knowledge base JSON")
    
    args = parser.parse_args()
    
    if args.command == "parse":
        agent = PolicyParserAgent(kb_path=args.kb)
        result = agent.parse_system(args.name, args.description)
        print(result.model_dump_json(indent=2))
        
    elif args.command == "evaluate":
        # Import and run evaluate_parser
        from eval.evaluate_parser import main as run_eval
        run_eval()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
