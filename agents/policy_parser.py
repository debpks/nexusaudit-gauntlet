import json
import os
import sys
from typing import Optional

# To support running directly or as package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from schemas.claim import ClaimSchema

from google import genai
from google.genai import types

class PolicyParserAgent:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.kb_data = self._load_kb()
        
        from agents.utils import get_gcp_project_id, get_genai_client, get_agent_model_config
        self.project_id = get_gcp_project_id()
        self.location = "us-central1"
        self.client = get_genai_client()
        self.model_name, self.temperature = get_agent_model_config("policy_parser", "gemini-2.5-flash", 0.0)

    def _load_kb(self) -> dict:
        if not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge base file not found at: {self.kb_path}")
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_system(self, system_name: str, system_description: str) -> ClaimSchema:
        kb_context = json.dumps(self.kb_data, indent=2)
        
        system_instruction = (
            "You are an expert compliance auditor specializing in AI governance and regulatory policy.\n"
            "Your task is to classify an AI system description based on the provided Ground Truth Knowledge Base.\n"
            "Analyze whether the system is 'high_risk' or 'exempt' according to the categories, rules, and conditions in the KB.\n\n"
            "CRITICAL RULES:\n"
            "1. Identify if the system falls under any regulated category or rule in the Knowledge Base.\n"
            "2. If it does, determine if it qualifies for an exemption or if it breaches any core compliance standards.\n"
            "3. Provide the exact category name or ID if applicable, or null if it's completely out of scope.\n"
            "4. Provide a detailed, legally robust explanation of the classification decision in the exemption_basis field.\n"
            "5. Make sure to output claimed_status exactly as 'high_risk' or 'exempt' or 'ambiguous'."
        )
        
        prompt = (
            f"Ground Truth Knowledge Base (EU AI Act):\n"
            f"```json\n{kb_context}\n```\n\n"
            f"--- Input AI System to Classify ---\n"
            f"System Name: {system_name}\n"
            f"Description: {system_description}\n\n"
            f"Please output a JSON object adhering to the specified schema."
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=self.temperature,
                response_mime_type="application/json",
                response_schema=ClaimSchema
            )
        )
        
        try:
            return ClaimSchema.model_validate_json(response.text)
        except Exception as e:
            cleaned_text = response.text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            return ClaimSchema.model_validate_json(cleaned_text.strip())
