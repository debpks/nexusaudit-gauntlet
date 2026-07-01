import os
import json
import sys

# To support running directly or as package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    # Provide a mock or exit gracefully if mcp is not installed locally
    print("Warning: mcp package not found. Please run 'pip install mcp[cli]' to use the FastMCP server.")
    sys.exit(1)

# Define the FastMCP server for the Agentic Gauntlet
mcp = FastMCP("AgenticGauntlet")

@mcp.resource("commerce://kb")
def get_commerce_kb() -> str:
    """
    Serve the JSON Knowledge Base for the Agentic Gauntlet pipeline.
    This allows external agents connecting to this MCP server to instantly read our regulatory rulebook.
    """
    kb_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "commerce_policy_kb.json")
    with open(kb_path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def audit_system(system_name: str, system_description: str) -> str:
    """
    Run an automated compliance audit on a Target AI system.
    
    Args:
        system_name: The name of the AI system to audit (e.g., 'NovaMart ShopBot').
        system_description: A detailed description of its functionality and database access.
        
    Returns:
        A formatted string detailing the system's compliance claim and exemption status based on the KB.
    """
    from agents.policy_parser import PolicyParserAgent
    
    kb_path = os.path.join(os.path.dirname(__file__), "..", "knowledge_base", "commerce_policy_kb.json")
    
    try:
        parser = PolicyParserAgent(kb_path=kb_path)
        claim = parser.parse_system(system_name, system_description)
        
        return (
            f"Audit Results for '{system_name}':\n"
            f"----------------------------------------\n"
            f"Status: {claim.status.upper()}\n"
            f"Category: {claim.category}\n"
            f"Exemption Basis: {claim.basis}\n"
        )
    except Exception as e:
        return f"Audit Error: {str(e)}"

if __name__ == "__main__":
    # Start the FastMCP server, allowing external clients (like Claude Desktop) to connect via stdio
    mcp.run()
