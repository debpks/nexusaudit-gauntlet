import os
import google.auth

def resolve_default_adc():
    """Dynamically resolves GCP Application Default Credentials without hardcoded paths or emails."""
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") and not os.environ.get("GEMINI_API_KEY"):
        try:
            from kaggle_secrets import UserSecretsClient
            client = UserSecretsClient()
            for proj_label in ["GOOGLE_CLOUD_PROJECT", "google_cloud_project", "GCP_PROJECT", "gcp_project", "PROJECT_ID", "project_id"]:
                try:
                    val = client.get_secret(proj_label)
                    if val:
                        os.environ["GOOGLE_CLOUD_PROJECT"] = val
                        break
                except Exception:
                    pass
            for key_label in ["GEMINI_API_KEY", "gemini_api_key", "GOOGLE_API_KEY", "google_api_key", "KAGGLE_API_KEY", "kaggle_api_key", "GEMINI_KEY", "gemini_key", "API_KEY", "api_key"]:
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
                        if hasattr(client, "set_tensorflow_credential"):
                            client.set_tensorflow_credential(cred)
                        if hasattr(client, "set_gcloud_credential"):
                            client.set_gcloud_credential(cred)
                        os.environ["KAGGLE_GCP_AUTH"] = "true"
                        return
                except Exception as e:
                    print(f"ℹ️ [Kaggle Auth] Could not retrieve Kaggle gcloud credential: {e}")
        except Exception:
            pass
        os.environ.setdefault("NO_GCE_CHECK", "true")

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
        
    for env_var in ["GOOGLE_APPLICATION_CREDENTIALS", "GCP_SERVICE_ACCOUNT_KEY"]:
        key_path = os.environ.get(env_var)
        if key_path and os.path.exists(key_path):
            try:
                import json
                with open(key_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("project_id"):
                        return data["project_id"]
            except Exception:
                pass
                
    legacy_dir = os.path.expanduser("~/.config/gcloud/legacy_credentials")
    if os.path.exists(legacy_dir):
        try:
            for user_folder in os.listdir(legacy_dir):
                adc_path = os.path.join(legacy_dir, user_folder, "adc.json")
                if os.path.exists(adc_path):
                    with open(adc_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data.get("client_id") and "-" in data["client_id"]:
                            return data["client_id"].split("-")[0]
        except Exception:
            pass
            
    std_adc = os.path.expanduser("~/.config/gcloud/application_default_credentials.json")
    if os.path.exists(std_adc):
        try:
            import json
            with open(std_adc, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("client_id") and "-" in data["client_id"]:
                    return data["client_id"].split("-")[0]
        except Exception:
            pass
            
    config_dir = os.path.expanduser("~/.config/gcloud/configurations")
    if os.path.exists(config_dir):
        try:
            for cfg_file in os.listdir(config_dir):
                if cfg_file.startswith("config_"):
                    with open(os.path.join(config_dir, cfg_file), "r", encoding="utf-8") as f:
                        for line in f:
                            if line.strip().startswith("project = "):
                                return line.strip().split(" = ")[1].strip()
        except Exception:
            pass

    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for filename in ["model_config.json", "config.json"]:
        cfg_path = os.path.join(pkg_dir, filename)
        try:
            if os.path.exists(cfg_path):
                import json
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
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or os.environ.get("KAGGLE_API_KEY") or os.environ.get("GEMINI_KEY") or os.environ.get("API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    else:
        project_id = get_gcp_project_id()
        location = os.environ.get("GCP_LOCATION", "us-central1")
        import google.auth
        cred = None
        try:
            cred, _ = google.auth.default()
        except Exception:
            pass
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
