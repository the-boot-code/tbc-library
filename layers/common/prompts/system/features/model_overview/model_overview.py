import json
from typing import Any
from python.helpers.files import VariablesPlugin
from python.helpers import files
from python.helpers.print_style import PrintStyle

class ModelOverview(VariablesPlugin):
    def get_variables(self, file: str, backup_dirs: list[str] | None = None, **kwargs) -> dict[str, Any]:
        # Check if model_overview feature is enabled via SystemControl
        try:
            from python.helpers.system_control import SystemControl
            system = SystemControl()
            
            if not system.is_feature_enabled("model_overview"):
                PrintStyle().hint(f"Model Overview DISABLED - Security profile: {system.get_active_profile()}")
                return {"model_overview": ""}
                
        except ImportError:
            PrintStyle().hint("SystemControl not available - model_overview enabled by default")
        except Exception as e:
            PrintStyle().hint(f"Error checking model_overview feature: {e}")
        
        # Extract agent config from kwargs (passed from extension)
        chat_model_provider = kwargs.get('chat_model_provider', 'unknown')
        chat_model_name = kwargs.get('chat_model_name', 'unknown')
        
        # Try to load model-specific persona file
        model_overview_path = f"/a0/prompts/system/features/model_overview/{chat_model_provider}/{chat_model_name}_overview.md"
        
        if files.exists(model_overview_path):
            try:
                model_overview = files.read_file(model_overview_path)
                PrintStyle().info(f"✓ Loaded model overview: {chat_model_provider}/{chat_model_name}")
            except Exception as e:
                PrintStyle().error(f"Error loading model overview '{model_overview_path}': {e}")
                model_overview = f"(Error loading model overview file: {model_overview_path})"
        else:
            PrintStyle().hint(f"Model overview file not found: {model_overview_path}")
            model_overview = f"(Model overview file not found: {model_overview_path})"

        
        return {
            "model_overview": model_overview
        }
