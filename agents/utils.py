import os
import google.auth

def resolve_default_adc():
    """Dynamically resolves GCP Application Default Credentials without hardcoded paths or emails."""
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.environ.get("GEMINI_API_KEY"):
        try:
            from kaggle_secrets import UserSecretsClient
            client = UserSecretsClient()
            for key_label in ["GEMINI_API_KEY", "GOOGLE_API_KEY", "GEMINI_KEY"]:
                try:
                    val = client.get_secret(key_label)
                    if val:
                        os.environ["GEMINI_API_KEY"] = val
                        return
                except Exception:
                    pass
            if hasattr(client, "get_gcloud_credential"):
                try:
                    cred = client.get_gcloud_credential()
                    if cred:
                        import google.auth
                        google.auth.default = lambda scopes=None, request=None, quota_project_id=None: (cred, os.environ.get("GOOGLE_CLOUD_PROJECT", "default"))
                        os.environ["KAGGLE_GCP_AUTH"] = "true"
                        return
                except Exception:
                    pass
        except Exception:
            pass

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

    if not fallback_project:
        try:
            import json
            cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model_config.json")
            if os.path.exists(cfg_path):
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    if cfg.get("project_id"):
                        return cfg["project_id"]
        except Exception:
            pass
            
    return fallback_project or "default-gcp-project"

def get_genai_client():
    """
    Returns a unified google.genai Client configured for either AI Studio (API Key) or Vertex AI (GCP / ADC).
    1. If GEMINI_API_KEY or GOOGLE_API_KEY is present in env, initializes Client(api_key=...).
    2. Otherwise, falls back to Vertex AI Client(vertexai=True, project=..., location=...).
    """
    resolve_default_adc()
    from google import genai
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    else:
        project_id = get_gcp_project_id()
        location = os.environ.get("GCP_LOCATION", "us-central1")
        import google.auth
        cred, _ = google.auth.default()
        return genai.Client(vertexai=True, project=project_id, location=location, credentials=cred)

def get_agent_model_config(agent_name: str, default_model: str = "gemini-2.5-pro", default_temp: float = 0.0):
    """
    Reads model and temperature settings for a given agent from model_config.json.
    Falls back to provided default_model and default_temp if config loading fails.
    """
    try:
        import json
        cfg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "model_config.json")
        if os.path.exists(cfg_path):
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                agent_cfg = cfg.get("agents", {}).get(agent_name, {})
                model = agent_cfg.get("model", default_model)
                temp = agent_cfg.get("temperature", default_temp)
                return model, temp
    except Exception:
        pass
    return default_model, default_temp
