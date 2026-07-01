import os
import google.auth

def resolve_default_adc():
    """Dynamically resolves GCP Application Default Credentials without hardcoded paths or emails."""
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        std_adc = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
        if os.path.exists(std_adc):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = std_adc
            return
        legacy_dir = os.path.expanduser("~/.config/gcloud/legacy_credentials")
        if os.path.exists(legacy_dir):
            for user_folder in os.listdir(legacy_dir):
                adc_path = os.path.join(legacy_dir, user_folder, "adc.json")
                if os.path.exists(adc_path):
                    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = adc_path
                    return

def get_gcp_project_id(fallback_project: str = None) -> str:
    """
    Dynamically resolves the Google Cloud Project ID.
    Prioritizes environment variables, then google.auth, then the fallback project.
    """
    resolve_default_adc()
    env_project = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if env_project:
        return env_project
        
    try:
        _, auth_project = google.auth.default()
        if auth_project:
            return auth_project
    except Exception:
        pass
        
    return fallback_project or "default-gcp-project"

def get_genai_client():
    """
    Returns a unified google.genai Client configured for either AI Studio (API Key) or Vertex AI (GCP / ADC).
    1. If GEMINI_API_KEY or GOOGLE_API_KEY is present in env, initializes Client(api_key=...).
    2. Otherwise, falls back to Vertex AI Client(vertexai=True, project=..., location=...).
    """
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    else:
        project_id = get_gcp_project_id()
        location = os.environ.get("GCP_LOCATION", "us-central1")
        return genai.Client(vertexai=True, project=project_id, location=location)

