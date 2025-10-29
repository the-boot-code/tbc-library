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
        
        # Extract agent from kwargs and get chat model info from it
        agent = kwargs.get('agent')
        if agent and hasattr(agent, 'config'):
            chat_model_provider = agent.config.chat_model.provider
            chat_model_name = agent.config.chat_model.name
        else:
            chat_model_provider = 'unknown'
            chat_model_name = 'unknown'
        
        # Try to load model-specific persona file
        model_overview_path = f"/a0/prompts/system/features/model_overview/{chat_model_provider}/{chat_model_name}_overview.md"
        
        if files.exists(model_overview_path):
            try:
                # Use read_prompt_file for templating support (placeholders, includes, nested plugins)
                model_overview = files.read_prompt_file(
                    model_overview_path,
                    _directories=[],  # No fallback dirs needed for absolute path
                    **kwargs  # Pass through all kwargs for future templating capabilities
                )
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
